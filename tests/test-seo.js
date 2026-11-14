/* SEO- и UI-контракт страниц pdfmerge.dev.
 *
 * Причина появления (14.11.2026): кнопка .cta-inline внутри .seo-content рендерилась
 * чёрным текстом на чёрном фоне. Правило `.seo-content a` (специфичность 0,1,1)
 * перебивало `.cta-inline` (0,1,0), поэтому цвет текста становился var(--fg) = чёрный
 * на чёрной кнопке. Пользователь увидел на мобильном пустой чёрный прямоугольник.
 * На десктопе и в моих проверках этого не было видно, потому что проверялась только
 * кнопка в hero (она вне .seo-content и работала).
 *
 * Тест статический: читает CSS и HTML, браузер не нужен.
 */
const fs = require('fs');
const path = require('path');

const ROOT = path.resolve(__dirname, '..');
let passed = 0, failed = 0;
const fail = [];
function ok(name, cond, extra) {
    if (cond) { passed++; }
    else { failed++; fail.push(name); console.log('  \u2717', name, extra === undefined ? '' : String(extra).slice(0, 300)); }
}

const read = (f) => fs.readFileSync(path.join(ROOT, f), 'utf8');

// --- 1. Кнопка не может быть невидимой внутри текста -------------------------
const css = read('css/style.css');
ok('CSS: .cta-inline объявлен глобально', /\.cta-inline\s*[,{]/.test(css));
ok('CSS: есть вариант с повышенной специфичностью для .seo-content',
    /\.seo-content\s+a\.cta-inline/.test(css),
    'без него .seo-content a перебивает цвет кнопки и текст исчезает');
ok('CSS: .cta-inline отменяет подчёркивание ссылки',
    /\.cta-inline[\s\S]{0,400}?text-decoration:\s*none/.test(css));
ok('CSS: .seo-content имеет ограничение ширины (текст не растянут на весь экран)',
    /\.seo-content\s*\{[\s\S]{0,200}?max-width/.test(css));

// --- 2. Сниппеты -------------------------------------------------------------
const PAGES = fs.readdirSync(ROOT).filter((f) => f.endsWith('.html') && !f.startsWith('backup'));
for (const f of PAGES) {
    const s = read(f);
    const title = (s.match(/<title[^>]*>([\s\S]*?)<\/title>/) || [])[1] || '';
    const t = title.replace(/\s+/g, ' ').trim();
    const d = (s.match(/<meta[^>]*name="description"[^>]*content="([^"]*)"/) || [])[1] || '';
    ok(`${f}: title \u226460`, t.length > 0 && t.length <= 60, `${t.length}: ${t}`);
    ok(`${f}: description \u2264160`, d.length > 0 && d.length <= 160, `${d.length} симв.`);
    ok(`${f}: canonical на себя`, /rel="canonical"[^>]*href="https:\/\/pdfmerge\.dev/.test(s));
}

// --- 3. FAQ: разметка обязана совпадать с видимым текстом --------------------
for (const f of PAGES) {
    const s = read(f);
    const visible = [...s.matchAll(/<h3>([\s\S]*?)<\/h3>\s*<p>/g)].map((m) => m[1].replace(/<[^>]+>/g, '').trim());
    let schema = [];
    for (const m of s.matchAll(/<script type="application\/ld\+json">([\s\S]*?)<\/script>/g)) {
        let j;
        try { j = JSON.parse(m[1]); } catch (e) { ok(`${f}: JSON-LD парсится`, false, String(e).slice(0, 100)); continue; }
        if (j['@type'] === 'FAQPage') schema = (j.mainEntity || []).map((q) => String(q.name).trim());
    }
    if (schema.length) {
        const inVisible = schema.filter((q) => visible.includes(q));
        ok(`${f}: все вопросы схемы видны на странице`, inVisible.length === schema.length,
            `${inVisible.length} из ${schema.length}`);
    }
}

// --- 4. Статьи: структура и призыв к действию -------------------------------
const ARTICLES = ['merge-pdf-offline', 'merge-pdf-without-uploading', 'merge-pdf-without-adobe',
                  'compress-pdf-offline', 'pdf-merge-no-signup'];
for (const slug of ARTICLES) {
    const f = slug + '.html';
    if (!fs.existsSync(path.join(ROOT, f))) { ok(`${f}: существует`, false); continue; }
    const s = read(f);
    const cta = (s.match(/class="cta-inline"/g) || []).length;
    ok(`${f}: минимум две кнопки (hero + в тексте)`, cta >= 2, `${cta}`);
    ok(`${f}: есть Article-разметка`, s.includes('"@type": "Article"'));
    ok(`${f}: есть блок related со ссылками на другие статьи`,
        /class="related-grid"[\s\S]*?merge-pdf-offline|class="related-grid"[\s\S]*?compress-pdf-offline/.test(s));
    const words = s.replace(/<script[\s\S]*?<\/script>/g, ' ').replace(/<style[\s\S]*?<\/style>/g, ' ')
        .replace(/<[^>]+>/g, ' ').replace(/\s+/g, ' ').trim().split(' ').filter(Boolean).length;
    ok(`${f}: не меньше 600 слов`, words >= 600, `${words}`);
}

// --- 5. Sitemap --------------------------------------------------------------
const sm = read('sitemap.xml');
const locs = [...sm.matchAll(/<loc>([^<]+)<\/loc>/g)].map((m) => m[1]);
const mods = [...sm.matchAll(/<lastmod>([^<]+)<\/lastmod>/g)].map((m) => m[1]);
ok('sitemap: у каждого URL есть lastmod', locs.length === mods.length, `${locs.length} / ${mods.length}`);
ok('sitemap: формат lastmod YYYY-MM-DD', mods.every((d) => /^\d{4}-\d{2}-\d{2}$/.test(d)));
for (const slug of ARTICLES) {
    ok(`sitemap: ${slug} присутствует`, locs.some((l) => l.endsWith('/' + slug)));
}
ok('sitemap: noindex-страницы (старые дубли) не включены',
    !locs.some((l) => /combine-pdf|join-pdf|merge-pdf-files|pdf-merger-online|privacy/.test(l)));

console.log(`\nPDFMERGE: ${passed}/${passed + failed} PASS` + (failed ? `, ${failed} FAIL` : ''));
if (failed) console.log('провалы: ' + fail.join(' | '));
process.exit(failed ? 1 : 0);
