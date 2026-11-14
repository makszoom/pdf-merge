# PLAN.md — PDF Merge (Browser-Side PDF Merger)
## Микро-SaaS по методологии Игоря Зуева

*Обновлено: 20 июля 2026*

---

## ✅ Этап 1: MVP — ЗАВЕРШЁН

| День | Задача | Статус |
|------|--------|--------|
| 1 | Core UI (drag-drop, список файлов) | ✅ |
| 2 | pdf-lib интеграция (merge → download) | ✅ |
| 3 | UX (сортировка ↑↓, удаление, прогресс) | ✅ |
| 4 | Paywall (счётчик 5 free → модалка) | ✅ |
| 5 | SEO landing pages (5 штук + Schema.org) | ✅ |
| 6 | Дизайн Vercel-style + PWA manifest | ✅ |
| 7 | Деплой на GitHub Pages | ✅ |

**Live:** https://makszoom.github.io/pdf-merge/
**Репо:** https://github.com/makszoom/pdf-merge

---

## ✅ Этап 1.5: Интеграция оплаты — ЗАВЕРШЁНА

*Архитектура A — полностью отдельная инфраструктура (Зуев-принцип)*

| Компонент | Значение | Статус |
|-----------|----------|--------|
| Telegram бот | `pdfmergepay_bot` (токен в .env) | ✅ |
| CHAT_ID | `659856721` | ✅ |
| TronLink кошелёк | `TCQTHvLP1ZctspY8UEgsWjy8xqe5tUTtFc` | ✅ |
| Cloudflare Worker | `pdfmerge-payment.makszoom85.workers.dev` | ✅ живой |
| KV namespace | `PDFMERGE_KV` (привязан) | ✅ |
| Variables | TARGET_ADDRESS, BOT_TOKEN, CHAT_ID | ✅ |
| Worker код | TronScan + Telegram + KV dedup + rate limit | ✅ залит |
| Frontend modal | QR + адрес + TXID + Verify | ✅ деплоен |
| Debug-обход | Убран (`confirm('Developer: unlock now?')`) | ✅ |
| Worker тест (curl) | `{"verified":false,"message":"Transaction not found..."}` | ✅ |
| Payment modal визуально | Подтверждён скриншотом | ✅ |

**Worker файл:** `pdfmerge-payment-worker.js`
**Платёжный конфиг в app.js:** `PAYMENT_CONFIG` (WORKER_URL, TRC20_ADDRESS, PRICE)

---

## ⏳ Этап 2: Тестирование

| Тест | Статус | Как проверить |
|------|--------|---------------|
| Merge 2 PDF × 5 страниц | ✅ | Базовый тест — работает |
| Merge 10 PDF × 50 страниц | ⏳ | Загрузить 10 файлов, проверить скорость |
| Merge 1 PDF × 500 страниц | ⏳ | Большой файл, проверить memory |
| Битый PDF → понятное сообщение | ⏳ | Загрузить повреждённый файл |
| Paywall: 5 free → блокировка → unlock | ✅ | Визуально подтверждён |
| **Реальный платёж $5 USDT** | ⏳ | Отправить USDT → вставить TXID → Verify |
| Mobile (Chrome Android) | ⏳ | Открыть на телефоне |
| Mobile (Safari iOS) | ⏳ | Открыть на iPhone |
| SEO-страницы: title, meta, Schema.org | ✅ | Деплоены, нужно проверить в Google |

---

## 🎯 Этап 3: Домен + Запуск (СЛЕДУЮЩИЙ)

### 3.1 Кастомный домен ✅
- [x] Купить домен `pdfmerge.dev` на Cloudflare Registrar ($12.20/год, Visa через oplatym.ru)
- [x] Создать CNAME файл в репо → задеплоен на GitHub
- [x] DNS: 4 A-записи (185.199.108-111.153) + CNAME www → makszoom.github.io
- [x] Все записи DNS only (серое облако)
- [x] Canonical URLs обновлены во всех HTML → `https://pdfmerge.dev/`
- [x] HTTP работает: `http://pdfmerge.dev/` → 200 OK
- [ ] HTTPS: ждём Let's Encrypt сертификат (5-15 мин)
- [ ] Enforce HTTPS: включить после выпуска сертификата

### 3.2 Google Search Console ✅
- [x] Добавить домен `pdfmerge.dev` в GSC (доменный ресурс)
- [x] Подтвердить владение (DNS TXT record через Cloudflare)
- [x] Отправить sitemap.xml → **Успешно, 6 страниц найдено**
- [x] Запросить индексацию через проверку URL
- [ ] Отслеживать индексацию (3-7 дней)

### 3.3 Sitemap
- [ ] Создать `sitemap.xml` со всеми страницами:
  - `/` (main tool)
  - `/merge-pdf`
  - `/combine-pdf`
  - `/pdf-merger-online`
  - `/merge-pdf-files`
  - `/join-pdf`
- [ ] Задеплоить на GitHub Pages

### 3.4 Аналитика ✅
- [x] Cloudflare Web Analytics (RUM) включена глобально
- [x] Без cookies — GDPR-friendly
- [x] Без snippet в HTML — работает через Cloudflare инфраструктуру
- [x] Отслеживает: визиты, просмотры, рефереры, страны, браузеры, Core Web Vitals

---

## 📈 Этап 4: Масштабирование (по метрикам)

| Триггер | Действие |
|---------|----------|
| 100 посетителей/день | Добавить Split PDF ($10 upsell) |
| 500 посетителей/день | Добавить Compress PDF |
| 1000 посетителей/день | Перейти на Vercel/VPS |
| 3000 посетителей/день | Поднять цену $5 → $8 |

---

## 🔄 Маршрут вывода денег

```
Пользователь платит $5 USDT TRC-20
  ↓
TronLink PDFMerge: TCQTHvLP1ZctspY8UEgsWjy8xqe5tUTtFc
  ↓ (копишь, пока не накопится $20-50)
TronLink → Send → Bybit (TRC-20)
  ↓
Bybit → P2P → продажа за рубли
  ↓
Сбербанк / Тинькофф
```

**Рекомендация:** выводить когда накопится $20-50, чтобы комиссия (~1 USDT) была незначительной.

---

## 📦 Файлы проекта

| Файл | Назначение |
|------|-----------|
| `index.html` | Главная (merge tool + payment modal) |
| `css/style.css` | Стили (Vercel-style + payment modal) |
| `js/app.js` | Логика (merge + paywall + verifyPayment) |
| `manifest.json` | PWA |
| `icon.svg` | Favicon |
| `merge-pdf.html` | SEO landing #1 |
| `combine-pdf.html` | SEO landing #2 |
| `pdf-merger-online.html` | SEO landing #3 |
| `merge-pdf-files.html` | SEO landing #4 |
| `join-pdf.html` | SEO landing #5 |
| `pdfmerge-payment-worker.js` | Cloudflare Worker код |
| `.env` | Токены и адреса (в .gitignore!) |
| `deploy_final.py` | Скрипт деплоя на GitHub Pages |
| `PLAN.md` | Этот файл |
| `PLAN_PAYMENT.md` | Архив: план интеграции оплаты |

---

## ⚠️ Риски

| Риск | Митигация |
|------|-----------|
| TronScan API лаг | Текст: "Wait 30-60s after sending" |
| KV не привязан | ✅ Проверено |
| Bot token обрезан | ✅ Ctrl+A → Delete → Ctrl+V |
| pdf-lib не тянет 100+ МБ | Ограничить 50 МБ на файл |
| Битые/зашифрованные PDF | Try/catch + понятное сообщение |
| Smallpdf добавит client-side merge | Быть первым + SEO + простота UI |
| GitHub Pages кэш | Cache-buster при тестах |

---

## 📊 Прогноз (консервативный)

| Метрика | Месяц 1 | Месяц 3 | Месяц 6 | Месяц 12 |
|---------|---------|---------|---------|----------|
| Трафик | 200/мес | 800/мес | 2,000/мес | 5,000/мес |
| Конверсия | 2% | 3% | 4% | 5% |
| Продажи | 4 | 24 | 80 | 250 |
| Доход ($5 lifetime) | $20 | $120 | $400 | $1,250 |
| Итого/мес | **$20** | **$120** | **$600** | **$2,050** |

---

*Методология: Игорь Зуев (utility-first, anti-freemium, lifetime $3–50)*
*Статус: MVP + оплата готовы. Следующий шаг — домен + Google Search Console*