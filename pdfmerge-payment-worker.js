// ═══════════════════════════════════════════════════════════════
// PDFMerge Payment Worker — USDT TRC-20 Verification
// Cloudflare Worker (free tier)
// Env vars: TARGET_ADDRESS, BOT_TOKEN, CHAT_ID
// KV binding: PDFMERGE_KV
// ═══════════════════════════════════════════════════════════════

export default {
  async fetch(request, env) {
    // ═══════ CORS ═══════
    const corsHeaders = {
      'Access-Control-Allow-Origin': '*',
      'Access-Control-Allow-Methods': 'POST, OPTIONS',
      'Access-Control-Allow-Headers': 'Content-Type',
      'Content-Type': 'application/json'
    };

    if (request.method === 'OPTIONS') {
      return new Response(null, { status: 204, headers: corsHeaders });
    }

    if (request.method !== 'POST') {
      return jsonResponse({ verified: false, message: 'Method not allowed' }, 405, corsHeaders);
    }

    // ═══════ RATE LIMIT (5 req/min per IP) ═══════
    const clientIP = request.headers.get('CF-Connecting-IP') || 'unknown';
    const now = Date.now();
    const rateKey = `rate:${clientIP}`;

    const rateData = await env.PDFMERGE_KV?.get(rateKey);
    if (rateData) {
      const { count, windowStart } = JSON.parse(rateData);
      if (now - windowStart < 60_000 && count >= 5) {
        return jsonResponse({ verified: false, message: 'Rate limit exceeded. Try again in a minute.' }, 429, corsHeaders);
      }
    }

    // ═══════ PARSE BODY ═══════
    let body;
    try {
      body = await request.json();
    } catch {
      return jsonResponse({ verified: false, message: 'Invalid JSON' }, 400, corsHeaders);
    }

    const { txId, amount: requestedAmount } = body;

    if (!txId || !/^[a-fA-F0-9]{64}$/.test(txId)) {
      return jsonResponse({ verified: false, message: 'Invalid TXID format. Expected 64 hex characters.' }, 400, corsHeaders);
    }

    // ═══════ PLAN SELECTION ($5 Unlimited / $9 Pro) ═══════
    const requested = parseFloat(requestedAmount) || 5;
    const plan = requested >= 8 ? 'pro' : 'unlimited';
    const PLAN_PRICE = plan === 'pro' ? 9 : 5;
    const MIN_AMOUNT = PLAN_PRICE - 0.5; // Allow slight underpayment (network fees, rounding)

    // ═══════ CHECK TRONSCAN ═══════
    const tronScanUrl = `https://apilist.tronscan.org/api/transaction-info?hash=${txId}`;

    let txData;
    try {
      const tronResponse = await fetch(tronScanUrl, {
        headers: { 'Accept': 'application/json' }
      });

      if (!tronResponse.ok) {
        return jsonResponse({ verified: false, message: 'TronScan API error. Try again later.' }, 502, corsHeaders);
      }

      txData = await tronResponse.json();
    } catch (e) {
      return jsonResponse({ verified: false, message: 'Network error. Try again later.' }, 502, corsHeaders);
    }

    if (!txData || txData.code !== 0 || !txData.data) {
      return jsonResponse({ verified: false, message: 'Transaction not found on blockchain. Wait 30-60 seconds after sending, then try again.' }, 404, corsHeaders);
    }

    const tx = txData.data;

    // ═══════ VALIDATE RECIPIENT ═══════
    const TARGET_ADDRESS = (env.TARGET_ADDRESS || '').trim();
    if (!TARGET_ADDRESS) {
      return jsonResponse({ verified: false, message: 'Server config error: no target address.' }, 500, corsHeaders);
    }

    const tokenInfo = tx.tokenTransferInfo || {};
    const recipient = (tokenInfo.to_address || tx.toAddress || '').toLowerCase();
    const expectedAddress = TARGET_ADDRESS.toLowerCase();

    if (recipient !== expectedAddress) {
      return jsonResponse({
        verified: false,
        message: 'This transaction was sent to a different address.'
      }, 400, corsHeaders);
    }

    // ═══════ VALIDATE AMOUNT ═══════
    const decimals = tokenInfo.decimals || 6;
    const amountRaw = parseFloat(tokenInfo.amount_str || tokenInfo.amount || 0);
    const amountUSDT = amountRaw / Math.pow(10, decimals);

    if (amountUSDT < MIN_AMOUNT) {
      return jsonResponse({
        verified: false,
        amount: amountUSDT,
        message: `Amount too small: ${amountUSDT.toFixed(2)} USDT. Minimum for ${plan}: ${PLAN_PRICE} USDT.`
      }, 400, corsHeaders);
    }

    // ═══════ VALIDATE TIME (< 24 hours) ═══════
    const txTimestamp = tx.timestamp || tx.tokenTransferInfo?.timestamp || 0;
    const hoursDiff = (now - txTimestamp) / (1000 * 60 * 60);

    if (hoursDiff > 24) {
      return jsonResponse({
        verified: false,
        message: 'Transaction too old. Must be within 24 hours.'
      }, 400, corsHeaders);
    }

    // ═══════ CHECK DUPLICATE ═══════
    const usedKey = `tx:${txId.toLowerCase()}`;
    const alreadyUsed = await env.PDFMERGE_KV?.get(usedKey);
    if (alreadyUsed) {
      return jsonResponse({
        verified: false,
        message: 'This transaction has already been used.'
      }, 400, corsHeaders);
    }

    // Mark as used (store for 30 days)
    await env.PDFMERGE_KV?.put(usedKey, '1', { expirationTtl: 30 * 24 * 60 * 60 });

    // Update rate limit
    const rateWindow = rateData ? JSON.parse(rateData).windowStart : now;
    const rateCount = rateData ? JSON.parse(rateData).count + 1 : 1;
    await env.PDFMERGE_KV?.put(rateKey, JSON.stringify({ count: rateCount, windowStart: rateWindow }), { expirationTtl: 60 });

    // ═══════ TELEGRAM NOTIFICATION ═══════
    await sendTelegramMessage(env, {
      verified: true,
      amount: amountUSDT,
      txId: txId,
      recipient: recipient,
      timestamp: new Date().toISOString()
    });

    // ═══════ LOG TO KV ═══════
    await logPayment(env, {
      txId: txId,
      amount: amountUSDT,
      recipient: recipient,
      timestamp: now,
      clientIP: clientIP
    });

    // ═══════ SUCCESS ═══════
    return jsonResponse({
      verified: true,
      amount: amountUSDT,
      plan: plan,
      txId: txId,
      message: plan === 'pro'
        ? 'Payment verified! Pro Batch activated (up to 30 files + ZIP).'
        : 'Payment verified! Unlimited merges activated.'
    }, 200, corsHeaders);
  }
};

async function sendTelegramMessage(env, data) {
  const BOT_TOKEN = env.BOT_TOKEN;
  const CHAT_ID = env.CHAT_ID;

  if (!BOT_TOKEN || !CHAT_ID) return;

  const txIdShort = data.txId.substring(0, 8) + '...' + data.txId.substring(60);
  const amount = data.amount.toFixed(2);
  const date = new Date().toLocaleString('ru-RU', { timeZone: 'Europe/Moscow' });

  const text = `🎉 *PDFMerge — NEW PAYMENT!*\n\n💰 *Amount:* ${amount} USDT\n📦 *Plan:* ${data.plan || 'unlimited'}\n🔗 *TXID:* \`${txIdShort}\`\n📅 *Date:* ${date} MSK\n📬 *Recipient:* \`${data.recipient?.substring(0, 12)}...\`\n✅ *Status:* Verified\n\n💵 *All time:* ${amount} USDT received`;

  try {
    await fetch(`https://api.telegram.org/bot${BOT_TOKEN}/sendMessage`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        chat_id: CHAT_ID,
        text: text,
        parse_mode: 'Markdown',
        disable_web_page_preview: true
      })
    });
  } catch (e) {
    console.error('Telegram notification failed:', e);
  }
}

async function logPayment(env, data) {
  if (!env.PDFMERGE_KV) return;

  const date = new Date(data.timestamp).toISOString().split('T')[0];
  const logKey = `payment:${date}:${data.txId}`;

  await env.PDFMERGE_KV.put(logKey, JSON.stringify(data), {
    expirationTtl: 90 * 24 * 60 * 60
  });

  const counterKey = `daily:${date}`;
  const current = await env.PDFMERGE_KV.get(counterKey);
  const count = current ? parseInt(current) + 1 : 1;
  await env.PDFMERGE_KV.put(counterKey, count.toString(), {
    expirationTtl: 90 * 24 * 60 * 60
  });
}

function jsonResponse(data, status, extraHeaders) {
  return new Response(JSON.stringify(data), {
    status,
    headers: { ...extraHeaders }
  });
}