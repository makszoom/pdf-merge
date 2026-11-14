# PLAN: Интеграция реальной оплаты USDT TRC-20 в PDF Merge

**Дата:** 20 июля 2026
**Архитектура:** A — полностью отдельная инфраструктура

---

## 🎯 Цель

Заменить заглушку `YOUR_TRC20_ADDRESS` на реальный платёжный флоу:
пользователь отправляет $5 USDT TRC-20 → вставляет TXID → Worker проверяет → разблокировка.

---

## 📋 Этапы

### Этап 1: Инфраструктура (ручные шаги пользователя)

| # | Действие | Где | Что получим |
|---|----------|-----|-------------|
| 1.1 | Создать Telegram бот | @BotFather → /newbot → `PDFMerge Payments` / `pdfmergepay_bot` | `BOT_TOKEN` |
| 1.2 | Узнать CHAT_ID | @userinfobot → /start | `CHAT_ID` (число) |
| 1.3 | Создать TronLink кошелёк | TronLink → Add wallet → NEW | `TRC20_ADDRESS` (T...) |
| 1.4 | Создать Cloudflare Worker | dash.cloudflare.com → Workers → Create → `pdfmerge-payment` | Worker URL |
| 1.5 | Создать KV namespace | Cloudflare → KV → Create → `PDFMERGE_KV` | KV bound |
| 1.6 | Добавить переменные | Worker → Settings → Variables | `TARGET_ADDRESS`, `BOT_TOKEN`, `CHAT_ID` |
| 1.7 | Привязать KV | Worker → Settings → Bindings → KV → `PDFMERGE_KV` | Binding done |
| 1.8 | Залить Worker код | Worker → Edit code → paste → Deploy | Worker live |

### Этап 2: Frontend — HTML (index.html)

- [ ] Заменить paywall modal на full payment modal:
  - QR-код (api.qrserver.com → `tron:ADDRESS?amount=5`)
  - Адрес TRC-20 с кнопкой Copy
  - Поле ввода TXID (64 hex)
  - Кнопка "Verify Payment"
  - Status area (success / error)
  - Спиннер при проверке

### Этап 3: Frontend — CSS (style.css)

- [ ] Стили для payment modal:
  - `.payment-qr` — QR image
  - `.address-box` — input + copy button
  - `.txid-input-group` — TXID field + verify button
  - `.payment-status` — success/error states
  - `.payment-spinner` — loading state
  - Адаптив для mobile

### Этап 4: Frontend — JS (app.js)

- [ ] Конфиг: `WORKER_URL`, `TRC20_ADDRESS`, `PRICE = 5`
- [ ] `showPaywall()` → открывает payment modal
- [ ] `copyAddress()` → clipboard copy
- [ ] `verifyPayment()` → POST к Worker, обработка ответа
- [ ] On `verified: true` → `localStorage.setItem('pdfmerge_unlocked','true')` + UI update
- [ ] Убрать debug-обход `confirm('Developer: unlock now?')`

### Этап 5: Worker код (pdfmerge-payment-worker.js)

На основе OGfy Worker с изменениями:
- Проект: `PDFMerge` (в Telegram сообщениях)
- MIN_AMOUNT: 4.5 USDT (допуск округления)
- KV namespace: `PDFMERGE_KV`
- Rate limit: 5 req/min/IP
- TXID dedup: 30 дней
- Логи: 90 дней

### Этап 6: Деплой

- [ ] Деплой обновлённого index.html, style.css, app.js на GitHub Pages
- [ ] Тест: открыть сайт → сделать 5 мержей → paywall → проверить UI
- [ ] Тест Worker: `curl -X POST WORKER_URL -d '{"txId":"fake64hex..."}'` → `"Transaction not found"` (норма)
- [ ] Реальный тест: отправить $5 USDT → вставить TXID → verify → unlock

---

## ⚠️ Риски и митигация

| Риск | Митигация |
|------|-----------|
| TronScan API лаг (TX не сразу виден) | Текст: "Wait 30-60s after sending" |
| KV не привязан → Worker crash | Чек-лист: Binding перед Deploy |
| Bot token обрезан в Cloudflare UI | Ctrl+A → Delete → Ctrl+V |
| Пользователь отправляет на wrong network | Текст: "USDT TRC-20 (Tron) only" |
| Повторное использование TXID | KV dedup `tx:{txId}` на 30 дней |
| Спам запросов к Worker | Rate limit 5/min/IP |

---

## 📦 Файлы для изменения

| Файл | Что меняем |
|------|-----------|
| `index.html` | Paywall modal → payment modal с QR/TXID |
| `css/style.css` | +стили payment modal |
| `js/app.js` | Конфиг + verifyPayment() + убираем debug |
| `pdfmerge-payment-worker.js` (новый) | Worker код для Cloudflare |

---

## ✅ Критерий успеха

1. Пользователь делает 5 мержей → видит paywall с QR и адресом
2. Копирует адрес → отправляет $5 USDT TRC-20
3. Вставляет TXID → Verify → "Payment verified!"
4. Мержи разблокированы навсегда (localStorage)
5. Telegram-уведомление приходит на телефон
6. TXID повторно не принимается

---

*План создан 20 июля 2026. Ждём одобрения.*