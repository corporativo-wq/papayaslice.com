// Pre-render del menú (camino A): ejecuta en Node el MISMO JavaScript del menú con un DOM mínimo
// y escribe el HTML resultante (idioma ES) dentro de <nav id="nav"> y <main id="menu"> del archivo.
// Así el menú completo queda como texto en el HTML de origen y el navegador lo vuelve a pintar igual.
const fs = require('fs');
const file = process.argv[2];
let html = fs.readFileSync(file, 'utf8');
const start = html.indexOf('<script>\nconst IMG = ');
const end = html.indexOf('</script>', start);
if (start < 0 || end < 0) { console.error('SSR: no encontré el script del menú'); process.exit(1); }
const code = html.slice(start + 8, end);
const els = {};
const mkEl = id => els[id] || (els[id] = { id, innerHTML: '', style: {}, hidden: false, attrs: {}, dataset: {},
  setAttribute(k, v) { this.attrs[k] = v; }, getAttribute(k) { return this.attrs[k]; },
  classList: { add() {}, remove() {}, toggle() {}, contains() { return false; } },
  appendChild() {}, addEventListener() {}, querySelector() { return null; }, querySelectorAll() { return []; },
  getBoundingClientRect() { return { top: 0, height: 0, left: 0, width: 0 }; } });
const document = { documentElement: mkEl('html'), body: mkEl('body'), getElementById: mkEl,
  querySelector: () => null, querySelectorAll: () => [], addEventListener() {}, createElement: () => mkEl('_tmp' + Math.random()) };
class IO { observe() {} unobserve() {} disconnect() {} }
const sandbox = { document, window: { addEventListener() {}, scrollY: 0, innerHeight: 800 }, IntersectionObserver: IO,
  requestAnimationFrame() {}, setTimeout() {}, addEventListener() {}, localStorage: { getItem: () => null, setItem() {} },
  location: { search: '', hash: '' }, matchMedia: () => ({ matches: false, addEventListener() {} }), innerHeight: 800, scrollY: 0 };
const fn = new Function(...Object.keys(sandbox), code + '\n;return 1;');
fn(...Object.values(sandbox));
const nav = els.nav && els.nav.innerHTML, menu = els.menu && els.menu.innerHTML;
if (!nav || !menu) { console.error('SSR: el render no produjo nav/menu'); process.exit(1); }
const put = (re, inner) => { if (!re.test(html)) { console.error('SSR: no encontré ' + re); process.exit(1); } html = html.replace(re, m => m.replace(/></, '>' + inner + '<')); };
put(/<div class="wrap" id="nav"><\/div>/, nav);
put(/<main id="menu" style="transition:opacity 150ms ease"><\/main>/, menu);
html = html.replace('<main id="menu" style="transition:opacity 150ms ease">', '<main id="menu" data-ssr="es" style="transition:opacity 150ms ease">');
fs.writeFileSync(file, html);
console.log('SSR menú: ' + Math.round(menu.length / 1024) + ' KB de HTML pre-renderizado');
