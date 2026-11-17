# Site profile — pdfmerge.dev

Читать в начале каждой сессии. Обновлять, когда владелец что-то решает.

## Product

- **Name:** PDF Toolkit (домен pdfmerge.dev)
- **Site:** https://pdfmerge.dev
- **What it does, in one line:** браузерный набор PDF-инструментов — склейка, разделение, сжатие, поворот, удаление страниц; файлы не покидают компьютер.
- **Language of the site:** английский. Коммуникация с владельцем — русский.
- **Markets that matter:** весь мир, англоязычный спрос. Преобладание US/IN/EU.

## Who pays

Модель: **5 бесплатных операций**, дальше разовая оплата — **$5 Unlimited** или **$9 Pro Batch**.
Счётчик `pdfmerge_merges_used` общий для всех инструментов (не отдельно на каждый).

Кто пользователь: человек, которому нужно склеить или сжать PDF разово — работа, учёба,
документы. Не платит за подписку, платит $5 один раз, если лимит исчерпан. Первая оплата
получена 25.08.2026.

## Topics

Согласовано с владельцем: 01.11.2026, уточнено 18.11.2026

**Pile A: продукт и есть ответ** (работать здесь)

| Тема | Главные запросы | Страница |
|---|---|---|
| Склейка без загрузки | merge pdf offline (10 подсказок Suggest), pdf merge no signup (5), merge pdf without uploading (3) | `/merge-pdf-offline`, `/merge-pdf-without-uploading`, `/pdf-merge-no-signup` |
| Склейка без Adobe | merge pdf without adobe | `/merge-pdf-without-adobe` |
| Сжатие без загрузки | compress pdf offline (10) против compress pdf without uploading (2) — «offline» сильнее | `/compress-pdf-offline` |
| Базовые операции | split pdf, rotate pdf, remove pages | `/split-pdf`, `/rotate-pdf`, `/remove-pages` |

**Pile B: только трафик, отложено**

| Тема | Почему отложено |
|---|---|
| «how to merge pdf» и подобные общие гайды | В топе Adobe, Smallpdf, iLovePDF — DR 85+. Статьёй не обойти, нужен продукт-ответ, а он уже есть на своих страницах |
| «best pdf merger free» (сравнения) | Требует честного разбора десятка конкурентов и постоянного обновления цен. Отдача ниже, чем у офлайн-угла, где мы реально отличаемся |

## Standing decisions

- **Никогда не обещать обработку на сервере.** Всё в браузере, это и есть wedge.
- **Про сжатие писать честно:** наш компрессор растеризует страницы, текст перестаёт выделяться. Для документов с текстом лучше Mac Export или Ghostscript — так и написано на странице.
- **Не заявлять «единственные browser-side».** Конкуренты тоже есть.
- **Реклама**: Cloudflare Web Analytics стоит; AdSense неприменим (RU-аккаунты деактивированы авг 2024).

## Where things live

- **Продукт:** HTML в корне репозитория (не в `site/`). Деплой `scripts/deploy_seo.py`.
- **Аналитика:** Cloudflare Web Analytics (cookieless).
- **Search Console:** `sc-domain:pdfmerge.dev`, сервисный аккаунт gsc-bot (Full).
- **Тесты:** `tests/test-seo.js` (90 проверок).
- **Расширение Chrome:** `~/Projects/pdf-merge-extension/`, готово к сабмиту в CWS.

**Дата последней сверки фактов продукта:** 2026-11-18
