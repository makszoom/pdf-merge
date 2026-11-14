# PLAN.md — PDF Toolkit на pdfmerge.dev
**Дата:** 2026-09-08 | **Статус:** черновик, ждём «давай»
**Цель:** выйти из «Discovered - currently not indexed» через уникальные функции + поднять цену с $5 до $15-30 на batch-режиме.

---

## Диагноз (почему делаем)

| Проблема | Факт | Решение в этом плане |
|---|---|---|
| 5 лендингов каннибализируют один запрос «pdf merge» | 2× Discovered, 2× unknown, 0 показов по целевым запросам | Каждый лендинг → своя уникальная функция |
| Нет контента для индексации | Главная = JS-тулза, ~300 слов | FAQ + how-to + уникальные тексты на каждой странице |
| 0 backlinks | referring = 1 спам-каталог | Вне скоупа кода — отдельно (см. Фаза 3) |
| $5 lifetime съедает B2B | batch просят офисы (superuser-кейсы из крона) | Batch Pro за $19 |

---

## Архитектура: 5 одинаковых → 4 уникальных + 1

**Сейчас:** merge-pdf / combine-pdf / pdf-merger-online / merge-pdf-files / join-pdf — все про «склей».

**Станет:**

| URL | Было | Станет | Ключ |
|---|---|---|---|
| `/merge-pdf` | дубликат главной | ✅ остаётся, единственный SEO-лендинг склейки (canonical контент-страница) | merge pdf files |
| `/split-pdf` | — | **NEW**: разделить PDF (по диапазону страниц) | split pdf |
| `/compress-pdf` | — | **NEW**: сжатие через рендер страниц в JPEG + пересборка pdf-lib | compress pdf |
| `/rotate-pdf` | — | **NEW**: повернуть страницы 90/180/270 | rotate pdf |
| `/remove-pages` | — | **NEW**: удалить выбранные страницы | remove pages from pdf |
| `/combine-pdf` и др. (4 шт.) | дубликаты | **301 редирект** на `/merge-pdf` (GitHub Pages не умеет 301 → html-meta refresh + canonical, см. Риски) | — |

Почему split/compress/rotate/remove: крон валидировал спрос (57.5 / 66.4 / 39.7 / 92 score из истории), все 4 уже размечены как ТЗ в истории ниш, pdf-lib умеет всё из коробки — **0 новых зависимостей**.

---

## Фаза 1 — Тулза (дни 1-3)

1. **`js/toolkit.js`** (новый файл, ~250 строк):
   - `splitPdf(file, ranges)` — pdf-lib `copyPages` по диапазонам
   - `compressPdf(file, quality)` — pdf.js рендер страницы → Canvas → JPEG → пересборка через pdf-lib embedJpg
   - `rotatePdf(file, angle, pages)` — `page.setRotation(degrees(angle))`
   - `removePages(file, removeSet)` — копирование всех страниц кроме выбранных
   - Общая обвязка: drag-drop (переиспользуем CSS), counter (`pdfmerge_merges_used` — общий с merge, localStorage)
2. **Страницы**: каждая = копия структуры merge-pdf.html (Schema.org HowTo + FAQPage), уникальный title/description/H1/FAQ (по 4-6 вопросов, ~500 слов текста — это то, чего Google'у не хватало)
3. **Paywall**: 5 бесплатных операций суммарно на все тулзы (один счётчик) → modal $5 unlimited single / $19 Pro batch
4. **Batch Pro**: JSZip, CSV-режим не в v1 (не перегружаем) — batch = «до 30 файлов за раз» на split/compress/rotate

## Фаза 2 — Перелинковка и деплой (день 4)

1. Главная: секция «More PDF Tools» → реальные 4 инструмента (вместо 5 дублей), footer обновить
2. `/merge-pdf` остаётся лендингом склейки, 4 старых лендинга → meta-refresh redirect + canonical на /merge-pdf (GitHub Pages не поддерживает .htaccess/_redirects)
3. sitemap.xml: 6 URL (главная + 5 инструментов)
4. Деплой: **backup-2026-09-08/** → deploy через существующий паттерн (Python + GitHub REST, токен из plainqr/.git/config) → **показать diff до пуша**
5. Request Indexing всех новых URL

## Фаза 3 — Вне скоупа кода (следующая сессия)

- Backlink: DR92-цель + 2-3 живых ссылки (dev-каталоги, ProductHunt alternative, Reddit r/pdf в комментарии — не спам)
- GSC-мониторинг через 7 дней: gsc-monitor.py 28

---

## Монетизация

| Тариф | Цена | Что даёт |
|---|---|---|
| Free | $0 | 5 операций, 1 файл за раз, до 50 MB |
| Unlimited | $5 (существующий SKU) | Безлимит single-операций |
| **Pro** | **$19 lifetime** | Batch до 30 файлов + ZIP + приоритетная поддержка Worker |

Оплата: существующий Worker `pdfmerge-payment.makszoom85.workers.dev` + KV dedup. **Для $19 нужен второй SKU в Worker** (amount=19, отдельный ключ KV `pdfmerge_unlocked_pro`) — правка Worker отдельным шагом с показом diff.

## Риски

1. **GitHub Pages без 301** → meta-refresh redirect признан Google (проверено на csv-to-json.com); риск дублирования снят canonical
2. **pdf.js добавит ~1 MB CDN** (для compress) → лениво грузить только на /compress-pdf
3. **Каннибализация merge-pdf ↔ главная** → merge-pdf = контент-страница (guides, FAQ), главная = тулза. Разные интенты
4. **Откат**: backup-2026-09-08/ + deploy.py откатывает один файл за раз (REST API PUT поверх)
5. **Worker правка** → сначала тест на fake TXID («Transaction not found» ожидаемо), только потом прод

## Что НЕ делаем

- Не трогаем csv-to-json.com (растёт сам: главная pos 23.7 → 5.5)
- Не трогаем дизайн/библиотеки (CSS-only, pdf-lib уже есть)
- Не покупаем домены
- Не пишем новых лендингов-дубликатов

## Оценка

- Срок: 4 дня MVP (по вечерам) — быстрее, чем 1 «новая ниша»
- Стоимость: $0 (всё на существующей инфре)
- Метрика успеха: через 14 дней — показы по «split pdf / compress pdf / rotate pdf» в GSC > 0