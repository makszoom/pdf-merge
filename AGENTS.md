---
name: pdf-merge
version: 2.0.0
updated: 2026-09-08
---

# AGENTS.md — pdf-merge

> Browser-side PDF Toolkit (merge + split + compress + rotate + remove pages). No upload, 100% local. $5 Unlimited / $9 Pro Batch. Custom domain + payment integrated.

## Basic Data

| Key | Value |
|-----|-------|
| Domain | https://pdfmerge.dev |
| Repo | makszoom/pdf-merge |
| Hosting | GitHub Pages + Cloudflare DNS |
| Payment | Cloudflare Worker + USDT TRC-20 + TronScan API |
| GSC | Verified, sitemap submitted |
| Analytics | Cloudflare Web Analytics (RUM) |

## Architecture

```
pdf-merge/
├── index.html              # Main tool (merge) + paywall modal ($5/$9 plan-grid)
├── css/
│   └── style.css           # Vercel-style + Apple Design CSS + plan-grid/tool-options
├── js/
│   ├── app.js              # Merge logic + paywall 2 плана + payment verify
│   └── toolkit.js          # PDF Toolkit engine: split/compress/rotate/remove (v2)
├── merge-pdf.html          # Единственный SEO-лендинг склейки (content page)
├── split-pdf.html          # Toolkit: split (data-tool="split")
├── compress-pdf.html       # Toolkit: compress (pdf.js lazy CDN)
├── rotate-pdf.html         # Toolkit: rotate
├── remove-pages.html       # Toolkit: remove pages
├── combine-pdf.html        # REDIRECT → /merge-pdf (meta-refresh, noindex, canonical)
├── pdf-merger-online.html  # REDIRECT → /merge-pdf
├── merge-pdf-files.html    # REDIRECT → /merge-pdf
├── join-pdf.html           # REDIRECT → /merge-pdf
├── scripts/
│   ├── gen_toolkit_pages.py # Генератор 4 toolkit-страниц
│   └── gen_redirects.py     # Генератор redirect-страниц
├── sitemap.xml             # 6 URLs: / + merge-pdf + 4 toolkit
├── robots.txt              # Allow: / + Sitemap directive
├── manifest.json           # PWA
├── CNAME                   # pdfmerge.dev
└── pdfmerge-payment-worker.js  # Worker v2: plan pro (amount>=8) — НЕ задеплоен в CF
```

## Stack

| Layer | Tech | Cost |
|-------|------|------|
| Frontend | HTML + CSS + vanilla JS | $0 |
| PDF engine | pdf-lib (CDN) | $0 |
| Hosting | GitHub Pages | $0 |
| Domain | Cloudflare Registrar | ~$12/yr |
| Payment | Cloudflare Worker + KV + TronScan | $0 |
| Analytics | Cloudflare Web Analytics | $0 |
| Notifications | Telegram Bot API | $0 |

## Key Decisions

- **Browser-side merge** — pdf-lib CDN, no server upload. Privacy USP.
- **Cloudflare Worker for payment** — free tier, KV for TXID dedup, TronScan API verification.
- **PDF Toolkit v2 (2026-09-08)** — 5 уникальных инструментов вместо 5 дубликатов-лендингов. Причина: каннибализация (все 5 лендингов боролись за «pdf merge») → Google держал их в «Discovered, not indexed». Каждый инструмент = свой ключ (split/compress/rotate/remove pages) + Schema HowTo/FAQ.
- **Пейволл 2 плана** — $5 Unlimited (pdfmerge_unlocked) / $9 Pro Batch 30 файлов+ZIP (pdfmerge_unlocked_pro). Worker v2 определяет план по сумме (amount >= 8 → pro).
- **Общий счётчик операций** — pdfmerge_merges_used общий для merge+toolkit: 5 free ops на все тулзы.
- **Apple Design CSS from Day 1** — glassmorphism, scale-in modal, reduced motion support.
- **No cross-navigation между лендингами** — но тулзы перелинкованы (related-grid + footer).

## Development Conventions

- Deploy via Python requests + GitHub REST API (not gh CLI — auth issues on Windows/Git Bash).
- Token stored in `~/.hermes/.env` as `GITHUB_TOKEN=` or extracted from `.git/config`.
- CSS-only enhancements. Never add JS animation libraries.
- Test Worker with fake TXID → "Transaction not found" (expected).
- Backup before deploy: `backup-YYYY-MM-DD/` folder.

## Status

| Component | Status |
|-----------|--------|
| MVP (merge, drag-drop, reorder) | ✅ Live |
| PDF Toolkit v2 (split/compress/rotate/remove) | ✅ Live (деплой 2026-09-08, E2E-тесты PASS) |
| Paywall 2 плана ($5 Unlimited / $9 Pro) | ✅ Live — plan-grid в modal, QR per plan |
| Payment Worker | ✅ v2 ($9 SKU, amount>=8→pro) задеплоен 2026-09-09 через CF REST API (multipart PUT, без wrangler). Live-код == локальный v2. Тест fake TXID → «Transaction not found» PASS. ⚠️ TronScan троттлит egress CF Workers после burst-тестов (все 4 Worker'а аккаунта); фолбэк — TronGrid |
| Redirects (4 дубликата → /merge-pdf) | ✅ Live (meta-refresh, noindex, canonical) |
| Sitemap (6 URL) + robots.txt | ✅ Live (2026-09-08) |
| GSC | ✅ Domain property; Request Indexing ×10 отправлен 2026-09-08 |
| Индексация | ⏳ Главная indexed 15.08; лендинги были «Discovered, not indexed» (каннибализация + 0 backlinks). Toolkit v2 = фикс. Проверить Coverage через 2-3 дня, показы по split/compress через 14 дней |
| Backlinks | ❌ 0 реальных — приоритет №1 |

## Тестирование Toolkit (проверено 2026-09-08)

- E2E в headless Chrome: split (3→2 стр), compress, rotate, remove — все PASS.
- **PDF.js render висит в hidden-вкладке** — известный артефакт headless-тестов. Фикс теста: CDP `Target.getTargets` → `Target.activateTarget` перед render. У живого пользователя вкладка видима — не баг продакшена.
- Локальный smoke: `python -m http.server` в одной browser_exec (сервер-поток умирает между вызовами).

## Documentation Update Rule

**After significant changes — update this file and relevant skill before ending session.**

Significant changes:
- Files/directories added or removed
- Stack changed (new service, removed old one)
- Key URLs/IDs/versions changed
- Architecture changed
- Payment configuration changed (address, Worker URL)

Not significant (don't update for):
- Individual content pages (lessons, articles)
- Temporary fixes
- Cosmetic CSS edits
