# -*- coding: utf-8 -*-
"""Genera las landings por sucursal (body HTML) en build/loc-<slug>.html.
Reutiliza el CSS ya compilado de la portada (build/papaya-slice-landing.html) para que el diseño sea idéntico.
Los datos reales (dirección, horarios, teléfonos, links y textos de cada landing) viven en contenido.json → "sucursales".
"""
import json, re, sys, os, html, importlib.util
here = os.path.dirname(os.path.abspath(__file__))
root = os.path.abspath(os.path.join(here, '..', '..'))
os.chdir(root)

# ---- datos de sucursales (fuente única: contenido.json → "sucursales" y "portada") ----
C = json.load(open('contenido.json', encoding='utf-8'))
D = {'dishes': C['portada']['dishes']}; WATI = C['sitio']['wati']
BR = {k: {x: y for x, y in v.items() if x not in ('landing', 'schema')} for k, v in C['sucursales'].items()}


DAYS_ES = ['Domingo','Lunes','Martes','Miércoles','Jueves','Viernes','Sábado']
DAYS_EN = ['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']

def hours_rows(h, es=True):
    rows = []
    for d in [1,2,3,4,5,6,0]:  # Lun..Dom
        today = h[str(d)] if str(d) in h else (h[d] if d in h else h['default'])
        name = (DAYS_ES if es else DAYS_EN)[d]
        if today is None:
            val = 'Cerrado' if es else 'Closed'
        else:
            o, c = today; c = '00:00' if c == '24:00' else c
            val = f'{o} – {c}'
        rows.append(f'<tr><th scope="row">{name}</th><td>{val}</td></tr>')
    return '\n'.join(rows)

def hours_summary(h, es=True):
    """Resumen legible: agrupa días consecutivos con el mismo horario."""
    order = [1,2,3,4,5,6,0]
    def val(d):
        t = h[str(d)] if str(d) in h else (h[d] if d in h else h['default'])
        return None if t is None else tuple(t)
    groups = []
    for d in order:
        v = val(d)
        if groups and groups[-1][1] == v: groups[-1][0].append(d)
        else: groups.append([[d], v])
    names = DAYS_ES if es else DAYS_EN
    out = []
    for days, v in groups:
        lab = names[days[0]] if len(days) == 1 else f'{names[days[0]]} a {names[days[-1]]}' if es else f'{names[days[0]]} to {names[days[-1]]}'
        if len(days) == 7: lab = 'Todos los días' if es else 'Every day'
        if v is None: out.append(f'{lab}: {"cerrado" if es else "closed"}')
        else:
            c = '00:00' if v[1] == '24:00' else v[1]
            out.append(f'{lab}: {v[0]} – {c}')
    return ' · '.join(out)

e = html.escape

PAGES = {k: v['landing'] for k, v in C['sucursales'].items()}

landing = open('build/papaya-slice-landing.html', encoding='utf-8').read()
head_lines = '\n'.join(l for l in landing.split('\n')[:14] if l.startswith('<meta') or l.startswith('<link') or l.startswith('<style>@font-face'))
_i = landing.find('<style>\n') if '<style>\n' in landing else [m.start() for m in re.finditer('<style>', landing) if not landing.startswith('<style>@font-face', m.start())][0]
style = landing[_i:landing.find('</style>', _i)+8]
EXTRA_CSS = '''<style>
.guia p{max-width:62ch;margin:12px 0 0;font-size:17px;line-height:1.55}
.mapcard{margin-top:14px;border-radius:14px;overflow:hidden;border:2px solid var(--ink);background:#FFF6EC}
.mapcard .mapph{display:flex;align-items:center;gap:12px;padding:18px;font-weight:600;background:repeating-linear-gradient(45deg,#FFE7D6 0 12px,#FFF6EC 12px 24px)}
.mapcard .mapbtns{display:flex;flex-wrap:wrap;gap:10px;padding:14px}
.mapcard iframe{display:block;width:100%;height:300px;border:0}
[hidden]{display:none!important}
.lhero{padding:44px 0 36px;background:var(--cream)}
.lhero h1{font-family:var(--wide);font-weight:400;font-size:clamp(34px,9vw,84px);line-height:.98;letter-spacing:-.01em;color:var(--ink);margin-top:8px}
.lhero .sub{font-size:clamp(17px,4.4vw,21px);font-weight:500;max-width:60ch;margin:18px 0 0;color:var(--muted)}
.lhero .cta{display:flex;gap:10px;flex-wrap:wrap;margin-top:24px}
.lhero .cta .btn{flex:1 1 150px}
.lgrid{display:grid;gap:18px;margin-top:26px}
@media(min-width:760px){.lgrid{grid-template-columns:1fr 1fr}}
.card{border:2px solid var(--line);border-radius:24px;padding:22px 20px;background:#fff;color:var(--ink)}
.card h3{font-family:var(--display);font-weight:900;text-transform:uppercase;font-size:30px;letter-spacing:.01em;margin-bottom:10px}
.card p{margin:0 0 10px;color:var(--ink)}
.card a{color:var(--turq-ink);font-weight:600}
.hrs{width:100%;border-collapse:collapse;font-size:16px}
.hrs th{text-align:left;font-weight:600;padding:7px 0;border-bottom:1px solid var(--line)}
.hrs td{text-align:right;padding:7px 0;border-bottom:1px solid var(--line);font-variant-numeric:tabular-nums}
.hrs tr:last-child th,.hrs tr:last-child td{border-bottom:0}
.lphoto{border-radius:28px;overflow:hidden;margin-top:26px;aspect-ratio:4/3;background:var(--sun)}
.lphoto img{width:100%;height:100%;object-fit:cover}
.faq details{border-bottom:1px solid rgba(255,255,255,.35);padding:14px 0}
.faq summary{cursor:pointer;font-weight:700;font-size:18px;list-style:none;display:flex;justify-content:space-between;gap:12px}
.faq summary::after{content:"+";font-family:var(--display);font-size:26px;line-height:1}
.faq details[open] summary::after{content:"–"}
.faq p{margin:10px 0 0;max-width:62ch}
.crumbs{font-size:13px;font-weight:600;color:var(--muted);margin:0}
.crumbs a{color:var(--muted);text-decoration:none}
.field.white .btn.ghost{border-color:var(--ink)}
.dishes{display:grid;gap:12px;margin-top:22px}
@media(min-width:640px){.dishes{grid-template-columns:repeat(3,1fr)}}
.dish{background:rgba(255,255,255,.14);border-radius:18px;padding:16px;color:#fff}
.dish b{display:block;font-family:var(--display);font-weight:900;text-transform:uppercase;font-size:24px}
.dish span{display:block;opacity:.9;margin-top:4px}
.dish em{display:block;font-style:normal;font-family:var(--display);font-weight:900;font-size:22px;margin-top:8px}
</style>'''

def bi(es, en, tag='span', cls='', extra=''):
    c = f' class="{cls}"' if cls else ''
    return f'<{tag}{c}{extra} data-es>{es}</{tag}><{tag}{c}{extra} data-en hidden>{en}</{tag}>'

def page(key):
    b = BR[key]; P = PAGES[key]; o = BR[P['other']]; OP = PAGES[P['other']]
    slug = P['slug']; tel_href = 'tel:' + b['tel'].replace(' ', '')
    dishes = D['dishes'][:3]
    T = lambda v, l: v if isinstance(v, str) else v[l]
    dish_html = ''.join(
        f'<div class="dish"><span data-es style="opacity:.8;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase">{e(T(d["kind"],"es"))}</span><span data-en hidden style="opacity:.8;font-size:13px;font-weight:700;letter-spacing:.12em;text-transform:uppercase">{e(T(d["kind"],"en"))}</span><b data-es>{e(T(d["n"],"es"))}</b><b data-en hidden>{e(T(d["n"],"en"))}</b><span data-es>{e(T(d["d"],"es"))}</span><span data-en hidden>{e(T(d["d"],"en"))}</span><em>${d["p"]} MXN</em></div>'
        for d in dishes)
    SV = C['sitio']['servicios']
    park_es = b['estacionamiento']['es'] + ((' ' + b['valet']['es']) if b.get('valet', {}).get('activo') else '')
    park_en = b['estacionamiento']['en'] + ((' ' + b['valet']['en']) if b.get('valet', {}).get('activo') else '')
    hr_es, hr_en = hours_summary(b['hours'], True), hours_summary(b['hours'], False)
    guia_html = ''.join(bi(g['es'], g['en'], 'p') for g in P['guia']) + bi(
        f"Horario: {hr_es}. {park_es} {b['desde']['es']}", f"Hours: {hr_en}. {park_en} {b['desde']['en']}", 'p')
    deliv_es = 'Sí, por Rappi' + (' y Uber Eats' if b.get('uber') else '') + '. También puedes pedir por WhatsApp para recoger en el local.'
    deliv_en = 'Yes, on Rappi' + (' and Uber Eats' if b.get('uber') else '') + '. You can also order on WhatsApp for pickup.'
    QA = [(('¿Cuál es el horario?','What are your hours?'), (hr_es + '.', hr_en + '.')),
          (('¿Aceptan reservaciones?','Do you take reservations?'), (SV['reservas']['es'], SV['reservas']['en'])),
          (('¿Tienen servicio a domicilio?','Do you deliver?'), (deliv_es, deliv_en)),
          (('¿Puedo pedir para llevar?','Can I order takeout?'), (SV['para_llevar']['es'], SV['para_llevar']['en'])),
          (('¿Hacen eventos, catering o pedidos grandes?','Do you do events, catering or large orders?'), (SV['eventos']['es'], SV['eventos']['en'])),
          (('¿Hay estacionamiento?','Is there parking?'), (park_es, park_en)),
          (('¿Cómo pido mi factura?','How do I get an invoice?'), (SV['factura']['es'], SV['factura']['en'])),
          (('¿Tienen opciones vegetarianas?','Do you have vegetarian options?'), (SV['vegetariano']['es'], SV['vegetariano']['en'])),
          (('¿Puedo llevar a mi mascota?','Can I bring my pet?'), (SV['mascotas']['es'], SV['mascotas']['en'])),
          (('¿Cobran descorche?','Do you charge corkage?'), (SV['descorche']['es'], SV['descorche']['en'])),
          (('¿Tienen promoción de cumpleaños?','Do you have a birthday deal?'), (SV['cumpleanos']['es'], SV['cumpleanos']['en'])),
          (('¿Venden por rebanada?','Do you sell by the slice?'), ('Sí. Rebanadas estilo Nueva York y charola Detroit, además de pizzas completas para 4 a 6 personas.','Yes. New York style slices and Detroit pans, plus whole pizzas for 4 to 6 people.')),
          (('¿Qué es la masa madre de 72 horas?','What is 72-hour sourdough?'), ('Nuestra masa fermenta tres días antes de entrar al horno. Por eso la orilla infla, cruje y se siente ligera.','Our dough ferments for three days before it meets the oven. That is why the crust puffs, crackles and feels light.'))]
    faq_html = '\n'.join(f"    <details><summary>{bi(q[0], q[1])}</summary>{bi(a[0], a[1], 'p')}</details>" for q, a in QA)
    from urllib.parse import quote
    map_embed = 'https://www.google.com/maps?q=' + quote('Papaya Slice, ' + C['sucursales'][key]['schema']['calle_ld'] + ', ' + C['sucursales'][key]['schema']['cp'] + ' ' + C['sucursales'][key]['schema']['localidad']) + '&output=embed'
    uber = f'<a class="btn white" data-ev="order_uber" data-branch="{slug}" href="{b["uber"]}" target="_blank" rel="noopener">Uber Eats</a>' if b.get('uber') else ''
    body = f'''<title>Papaya Slice · {e(b['city'])}</title>
{head_lines}
{style}
{EXTRA_CSS}
<a class="skip" href="#contenido">Saltar al contenido</a>
<header class="top"><div class="wrap">
  <a href="/" aria-label="Papaya Slice · inicio"><img src="/img/da6e6e826c.png" alt="Papaya Slice" width="113" height="34" translate="no"></a>
  <nav aria-label="Secciones">
    <a href="/menu" data-es>Menú</a><a href="/menu" data-en hidden>Menu</a>
    <a href="#pedir" data-es>Pedir</a><a href="#pedir" data-en hidden>Order</a>
    <a href="#horario" data-es>Horario</a><a href="#horario" data-en hidden>Hours</a>
    <a href="/{OP['slug']}" data-es>{e(o['city'])}</a><a href="/{OP['slug']}" data-en hidden>{e(o['city'])}</a>
  </nav>
  <div class="lang" role="group" aria-label="Idioma / Language">
    <button id="lang-es" aria-pressed="true" onclick="setLang('es')">ES</button>
    <button id="lang-en" aria-pressed="false" onclick="setLang('en')">EN</button>
  </div>
</div></header>

<main id="contenido">
<section class="lhero">
  <div class="wrap">
    <p class="crumbs"><a href="/">Papaya Slice</a> › {e(b['city'])} · {e(b['name'])}</p>
    <span class="eyebrow" style="color:var(--coral-ink)">{e(b['label']['es'])}</span>
    <h1><span data-es>{P['h1']['es']}</span><span data-en hidden>{P['h1']['en']}</span></h1>
    <p class="sub" data-es>{P['intro']['es']}</p><p class="sub" data-en hidden>{P['intro']['en']}</p>
    <div class="cta">
      <a class="btn turq" data-ev="como_llegar" data-branch="{slug}" href="{b['maps']}" target="_blank" rel="noopener"><span data-es>Cómo llegar</span><span data-en hidden>Directions</span></a>
      <a class="btn coral" data-ev="whatsapp" data-branch="{slug}" href="{b['wa']}" target="_blank" rel="noopener"><span data-es>Reservar por WhatsApp</span><span data-en hidden>Reserve on WhatsApp</span></a>
      <a class="btn ghost" data-ev="menu_nav" data-branch="{slug}" href="/menu" style="border-color:var(--ink);color:var(--ink)"><span data-es>Ver menú</span><span data-en hidden>See menu</span></a>
    </div>
    <div class="lphoto"><img src="{P['img']}" alt="{e(P['img_alt']['es'])}" fetchpriority="high"></div>
  </div>
</section>

<section class="field white" id="guia">
  <div class="wrap">
    <span class="eyebrow" style="color:var(--coral-ink)">{bi('Antes de venir','Before you come')}</span>
    <h2 class="disp">{bi('Qué esperar en Papaya Slice '+e(b['name']),'What to expect at Papaya Slice '+e(b['name']))}</h2>
    <div class="guia">{guia_html}</div>
  </div>
</section>

<section class="field white" id="horario">
  <div class="wrap">
    <span class="eyebrow" style="color:var(--coral-ink)">{bi('Visítanos','Visit us')}</span>
    <h2 class="disp">{bi('Dirección y horario','Address and hours')}</h2>
    <div class="lgrid">
      <div class="card">
        <h3>{bi('Dirección','Address')}</h3>
        <p><address style="font-style:normal" data-es>{e(b['addr']['es'])}, Quintana Roo</address><address style="font-style:normal" data-en hidden>{e(b['addr']['en'])}, Quintana Roo</address></p>
        <p data-es>{P['how']['es']}</p><p data-en hidden>{P['how']['en']}</p>
        <p><a data-ev="phone" data-branch="{slug}" href="{tel_href}">{e(b['tel'])}</a></p>
        <div class="mapcard" data-embed="{map_embed}">
          <div class="mapph" aria-hidden="true"><svg width="34" height="44" viewBox="0 0 34 44"><path d="M17 0C7.6 0 0 7.4 0 16.6 0 29 17 44 17 44s17-15 17-27.4C34 7.4 26.4 0 17 0z" fill="#F07A45"/><circle cx="17" cy="16.5" r="6.5" fill="#fff"/></svg><span>{e(b['addr']['es'])}</span></div>
          <div class="mapbtns"><button type="button" class="btn ghost mapopen" style="border-color:var(--ink);color:var(--ink)">{bi('Ver el mapa','Show map')}</button><a class="btn turq" data-ev="como_llegar" data-branch="{slug}" href="{b['maps']}" target="_blank" rel="noopener">{bi('Cómo llegar en Google Maps','Directions in Google Maps')}</a></div>
        </div>
      </div>
      <div class="card">
        <h3>{bi('Horario','Hours')}</h3>
        <table class="hrs" data-es><tbody>{hours_rows(b['hours'], True)}</tbody></table>
        <table class="hrs" data-en hidden><tbody>{hours_rows(b['hours'], False)}</tbody></table>
        <p style="margin-top:12px;color:var(--muted);font-size:14px" data-es>Si vienes en grupo o para un evento, confirma por WhatsApp.</p>
        <p style="margin-top:12px;color:var(--muted);font-size:14px" data-en hidden>For groups or events, confirm on WhatsApp.</p>
      </div>
    </div>
  </div>
</section>

<section class="field coral" id="menu">
  <div class="wrap">
    <span class="eyebrow">{bi('Lo que pide la gente','What people order')}</span>
    <h2 class="disp">{bi('Rebanada, charola o completa','Slice, pan or whole')}</h2>
    <p class="lede" data-es>Masa madre de 72 horas en tres estilos: rebanada Nueva York, charola Detroit y Tokyo Style. Precios en pesos mexicanos; consulta el menú completo en línea.</p>
    <p class="lede" data-en hidden>72-hour sourdough in three styles: New York slice, Detroit pan and Tokyo Style. Prices in Mexican pesos; see the full menu online.</p>
    <div class="dishes">{dish_html}</div>
    <div class="btn-row"><a class="btn white" data-ev="menu_nav" data-branch="{slug}" href="/menu">{bi('Menú completo con precios','Full menu with prices')}</a></div>
  </div>
</section>

<section class="field sun" id="pedir">
  <div class="wrap">
    <span class="eyebrow">{bi('A domicilio o para llevar','Delivery or takeout')}</span>
    <h2 class="disp">{bi('Pide en '+e(b['city']),'Order in '+e(b['city']))}</h2>
    <p class="lede" data-es>{P['delivery']['es']}</p><p class="lede" data-en hidden>{P['delivery']['en']}</p>
    <div class="btn-row">
      <a class="btn coral" data-ev="order_rappi" data-branch="{slug}" href="{b['rappi']}" target="_blank" rel="noopener">Rappi</a>
      {uber}
      <a class="btn solid" data-ev="whatsapp" data-branch="{slug}" href="{b['wa']}" target="_blank" rel="noopener">WhatsApp</a>
    </div>
  </div>
</section>

<section class="field turq faq" id="preguntas">
  <div class="wrap">
    <span class="eyebrow">{bi('Antes de venir','Before you come')}</span>
    <h2 class="disp">{bi('Preguntas frecuentes','FAQ')}</h2>
{faq_html}
    <details><summary>{bi('¿Tienen otra sucursal?','Do you have another location?')}</summary><p data-es>{P['other_txt']['es']} <a href="/{OP['slug']}" style="color:#fff">Ver sucursal {e(o['city'])}</a>.</p><p data-en hidden>{P['other_txt']['en']} <a href="/{OP['slug']}" style="color:#fff">See {e(o['city'])} location</a>.</p></details>
  </div>
</section>
</main>

<footer><div class="wrap">
  <div class="grid">
    <div>
      <img class="big-logo" src="/img/ae8d7c9255.png" alt="Papaya Slice" width="600" height="380" loading="lazy" translate="no">
      <p style="opacity:.8;margin:10px 0 0;max-width:36ch" data-es>Pizza de masa madre en Playa del Carmen y Cancún.</p>
      <p style="opacity:.8;margin:10px 0 0;max-width:36ch" data-en hidden>Sourdough pizza in Playa del Carmen and Cancún.</p>
    </div>
    <div>
      <h4 data-es>Contacto</h4><h4 data-en hidden>Contact</h4>
      <a data-ev="whatsapp" data-branch="{slug}" href="{b['wa']}" target="_blank" rel="noopener">WhatsApp</a>
      <a href="https://instagram.com/papayaslicemx" target="_blank" rel="noopener">Instagram</a>
      <a data-ev="phone" data-branch="{slug}" href="{tel_href}">{e(b['tel'])}</a>
    </div>
    <div>
      <h4 data-es>Explora</h4><h4 data-en hidden>Explore</h4>
      <a href="/" data-es>Inicio</a><a href="/" data-en hidden>Home</a>
      <a href="/menu" data-es>Menú</a><a href="/menu" data-en hidden>Menu</a>
      <a href="/playa-del-carmen">Playa del Carmen</a>
      <a href="/cancun">Cancún</a>
    </div>
  </div>
  <div class="legal">© 2026 Papaya Slice · Mu Group · <a href="/privacidad" style="display:inline;color:inherit;text-decoration:underline"><span data-es>Aviso de privacidad</span><span data-en hidden>Privacy notice</span></a></div>
</div></footer>

<nav class="bar" aria-label="Acciones">
  <a class="primary" href="#pedir"><span data-es>Pedir</span><span data-en hidden>Order</span><small>{'Rappi · Uber' if b.get('uber') else 'Rappi'}</small></a>
  <a data-ev="whatsapp" data-branch="{slug}" href="{b['wa']}" target="_blank" rel="noopener"><span data-es>Reservar</span><span data-en hidden>Reserve</span><small>WhatsApp</small></a>
  <a data-ev="menu_nav" data-branch="{slug}" href="/menu"><span data-es>Menú</span><span data-en hidden>Menu</span><small>ES · EN</small></a>
  <a data-ev="como_llegar" data-branch="{slug}" href="{b['maps']}" target="_blank" rel="noopener"><span data-es>Llegar</span><span data-en hidden>Directions</span><small>Maps</small></a>
</nav>

<script>
let lang='es'; try{{ const s=localStorage.getItem('ps-lang'); if(s==='en'||s==='es') lang=s; }}catch(e){{}}
if(lang==='es' && !localStorage.getItem('ps-lang') && /^en/i.test(navigator.language||'')) lang='en';
function apply(){{ document.documentElement.lang = lang==='es'?'es-MX':'en';
  document.querySelectorAll('[data-es]').forEach(x=>x.hidden=(lang!=='es'));
  document.querySelectorAll('[data-en]').forEach(x=>x.hidden=(lang!=='en'));
  document.getElementById('lang-es').setAttribute('aria-pressed',lang==='es'); document.getElementById('lang-en').setAttribute('aria-pressed',lang==='en'); }}
function setLang(l){{ lang=l; try{{localStorage.setItem('ps-lang',l)}}catch(e){{}} apply(); }}
apply();
document.querySelectorAll('.mapopen').forEach(bt=>bt.addEventListener('click',()=>{{const c=bt.closest('.mapcard');const f=document.createElement('iframe');f.src=c.dataset.embed;f.title='Mapa';f.loading='lazy';f.referrerPolicy='no-referrer-when-downgrade';c.querySelector('.mapph').replaceWith(f);bt.remove();}}));
</script>
'''
    return slug, body

os.makedirs('build', exist_ok=True)
for key in BR:
    slug, body = page(key)
    open(f'build/loc-{slug}.html', 'w', encoding='utf-8').write(body)
    print('build/loc-%s.html' % slug, len(body)//1024, 'KB')
