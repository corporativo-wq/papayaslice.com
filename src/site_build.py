import json,base64,io,re,os,shutil
from PIL import Image
os.makedirs('.',exist_ok=True)
# ---- todo sale de contenido.json (fuente única) ----
C=json.load(open('contenido.json',encoding='utf-8'))
S=C['sitio']; SEO=C['seo']; SUC=C['sucursales']
D=S['dominio']
DIAS=['Sunday','Monday','Tuesday','Wednesday','Thursday','Friday','Saturday']
def opening(h):
    """Horario de contenido.json → OpeningHoursSpecification (agrupa días con el mismo horario, Lun→Dom)."""
    grupos=[]
    for d in [1,2,3,4,5,6,0]:
        t=h[str(d)] if str(d) in h else h['default']
        if t is None: continue
        t=tuple(t)
        for g in grupos:
            if g[0]==t: g[1].append(DIAS[d]); break
        else: grupos.append([t,[DIAS[d]]])
    return [{"@type":"OpeningHoursSpecification","dayOfWeek":dias,"opens":t[0],"closes":t[1]} for t,dias in grupos]
def rest(b):
    x=b['schema']
    return {"@type":"Restaurant","@id":D+"/#"+x['ld_id'],"name":x['ld_name'],"url":D+"/"+b['landing']['slug'],"image":D+"/og.jpg","telephone":b['tel'],"priceRange":"$$","servesCuisine":["Pizza","Italiana"],"sameAs":[S['instagram']],"menu":D+"/menu","acceptsReservations":"True","parentOrganization":{"@id":D+"/#org"},
   "address":{"@type":"PostalAddress","streetAddress":x['calle_ld'],"addressLocality":x['localidad'],"addressRegion":"Quintana Roo","postalCode":x['cp'],"addressCountry":"MX"},
   "geo":{"@type":"GeoCoordinates","latitude":x['geo']['lat'],"longitude":x['geo']['lng']},"hasMap":b['maps'],
   "openingHoursSpecification":opening(b['hours'])}
LD_HOME=json.dumps({
 "@context":"https://schema.org","@graph":[
  {"@type":"Organization","@id":D+"/#org","name":S['nombre'],"url":D+"/","logo":D+"/favicon.png","sameAs":[S['instagram']]},
  {"@type":"WebSite","@id":D+"/#site","url":D+"/","name":S['nombre'],"inLanguage":"es-MX","publisher":{"@id":D+"/#org"}}]+[rest(b) for b in SUC.values()]
 },ensure_ascii=False)
GRAPH=json.loads(LD_HOME)["@graph"]
ORG=GRAPH[0]; R38=[x for x in GRAPH if x.get("@id")==D+"/#av38"][0]; RNA=[x for x in GRAPH if x.get("@id")==D+"/#nader"][0]
def ld_loc(r,slug,city):
    r=dict(r); r["@id"]=D+"/"+slug+"/#restaurant"; r["url"]=D+"/"+slug
    return json.dumps({"@context":"https://schema.org","@graph":[ORG,r,
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Papaya Slice","item":D+"/"},{"@type":"ListItem","position":2,"name":city,"item":D+"/"+slug}]}]},ensure_ascii=False)
LD_38=ld_loc(R38,"playa-del-carmen","Playa del Carmen"); LD_NA=ld_loc(RNA,"cancun","Cancún")
def _es(x):
    return (x.get('es') or x.get('en') or '') if isinstance(x,dict) else (x or '')
def _offer(p,name=None):
    o={"@type":"Offer","price":str(p),"priceCurrency":"MXN"}
    if name: o["name"]=name
    return o
def _item(it,sec_price=None,glass=None,bottle=None):
    m={"@type":"MenuItem","name":_es(it['n'])}
    if it.get('d'): m["description"]=_es(it['d'])
    p=it.get('p', sec_price)
    if it.get('p2') is not None:
        m["offers"]=[_offer(p,_es(glass).strip() or None),_offer(it['p2'],_es(bottle).strip() or None)]
    elif p is not None:
        m["offers"]=_offer(p)
    return m
def _sections(menu):
    out=[]
    for sec in menu:
        name=_es(sec.get('short') or sec['title']); items=[]
        sp=sec.get('price')
        for it in sec.get('items',[]): items.append(_item(it,sp))
        if sec['kind']=='pasta':
            forms=', '.join(_es(o['n']) for o in sec['steps'][0]['opts'])
            sauces=', '.join(_es(o['n']) for o in sec['steps'][1]['opts'])
            items.append({"@type":"MenuItem","name":"Pasta fresca ("+forms+")","description":"Salsas: "+sauces,"offers":_offer(sp)})
            for it in sec.get('extra',[]): items.append(_item(it,sp))
        for g in sec.get('groups',[]):
            for it in g['items']: items.append(_item(it,None,sec.get('glass'),sec.get('bottle')))
        if sec.get('pills'):
            for o in sec['pills']['opts']: items.append(_item({'n':o['n'],'p':sec['pills']['p']}))
        out.append({"@type":"MenuSection","name":name,"hasMenuItem":items})
    return out
# Menú completo para Google y las IAs: cada platillo como MenuItem, generado de los MISMOS datos que el menú visible
LD_MENU=json.dumps({"@context":"https://schema.org","@type":"Menu","@id":D+"/menu/#menu","name":"Menú de Papaya Slice","url":D+"/menu","inLanguage":"es-MX","hasMenuSection":_sections(C["menu"])},ensure_ascii=False)
# Eventos de conversión: cada clic en un elemento con data-ev se manda a window.dataLayer (lo lee GTM/GA4 cuando se instale)
# ev: como_llegar | whatsapp | phone | order_rappi | order_uber | menu_nav | branch_page ; branch: playa-del-carmen | cancun
EVENTS='''<script>
window.dataLayer=window.dataLayer||[];
document.addEventListener('click',function(e){var a=e.target.closest('[data-ev]');if(!a)return;
window.dataLayer.push({event:'cta_click',cta:a.getAttribute('data-ev'),branch:a.getAttribute('data-branch')||'',page:location.pathname,href:a.getAttribute('href')||''});
if(typeof gtag==='function'){gtag('event',a.getAttribute('data-ev'),{branch:a.getAttribute('data-branch')||'',page_path:location.pathname});}},{passive:true});
</script>
'''
# Meta Pixel de Papaya Slice: se inserta tal cual antes de </head> en todas las páginas (src/meta_pixel.html)
PIXEL=open('src/meta_pixel.html',encoding='utf-8').read() if os.path.exists('src/meta_pixel.html') else ''
def wrap(body,title,desc,path,ld):
    body=re.sub(r'^<title>.*?</title>\n','',body)
    lines=body.split('\n'); headlines=[]; i=0
    while i<len(lines) and (lines[i].startswith('<meta') or lines[i].startswith('<link') or lines[i].startswith('<style>@font-face')): headlines.append(lines[i]); i+=1
    rest='\n'.join(lines[i:])
    head=f'''<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id={S['ga4_id']}"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','{S['ga4_id']}');</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{D}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="google-site-verification" content="{S['search_console_meta']}">
<meta property="og:type" content="website"><meta property="og:site_name" content="Papaya Slice"><meta property="og:locale" content="es_MX">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{D}{path}"><meta property="og:image" content="{D}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{ld}</script>
'''
    return head+'\n'.join(headlines)+'\n'+PIXEL+'</head>\n<body>\n'+rest+'\n'+EVENTS+'</body>\n</html>\n'
L=open('build/papaya-slice-landing.html').read().replace('https://claude.ai/artifact/DoMWeTromrd56uR4MHRPeL','/menu')
M=open('build/papaya-slice-menu.html').read().replace('https://claude.ai/artifact/UMA9LHkZTeD8TuqugmA6Zt','/')
# Verificación de dominio de Meta: solo en la página de inicio, dentro del <head>
META_VERIF='<meta name="facebook-domain-verification" content="amp07e3miq16lu1dind4zwxx18heut" />\n'
open('index.html','w').write(wrap(L,SEO['inicio']['title'],SEO['inicio']['description'],'/',LD_HOME).replace('</head>',META_VERIF+'</head>',1))
open('menu.html','w').write(wrap(M,SEO['menu']['title'],SEO['menu']['description'],'/menu',LD_MENU))
P38=open('build/loc-playa-del-carmen.html').read(); PNA=open('build/loc-cancun.html').read()
open('playa-del-carmen.html','w').write(wrap(P38,SEO['38']['title'],SEO['38']['description'],'/playa-del-carmen',LD_38))
open('cancun.html','w').write(wrap(PNA,SEO['nader']['title'],SEO['nader']['description'],'/cancun',LD_NA))
PRIV=open('src/privacidad/privacidad.html',encoding='utf-8').read()
open('privacidad.html','w').write(wrap(PRIV,'Aviso de privacidad · Papaya Slice','Aviso de privacidad de Papaya Slice: qué datos recabamos, para qué los usamos y cómo ejercer tus derechos ARCO.','/privacidad','{}'))
open('google4708ea497496b16c.html','w').write('google-site-verification: google4708ea497496b16c.html')
imgs=json.load(open('src/landing/imgs.json'))
logo=Image.open(io.BytesIO(base64.b64decode(imgs['logo'].split(',')[1]))).convert('RGBA')
def icon(size,pad):
    c=Image.new('RGBA',(size,size),(255,255,255,255)); l=logo.copy(); l.thumbnail((size-2*pad,size-2*pad)); c.paste(l,((size-l.width)//2,(size-l.height)//2),l); return c
# íconos y og.jpg solo se generan si no existen (así un build no reescribe binarios idénticos); bórralos para regenerarlos
if not os.path.exists('favicon.png'): icon(192,18).save('favicon.png')
if not os.path.exists('apple-touch-icon.png'): icon(180,16).convert('RGB').save('apple-touch-icon.png')
if not os.path.exists('og.jpg'):
  og=Image.new('RGB',(1200,630),(240,122,69)); lw=Image.open(io.BytesIO(base64.b64decode(imgs['logo_w'].split(',')[1]))).convert('RGBA'); lw.thumbnail((900,480)); og.paste(lw,((1200-lw.width)//2,(630-lw.height)//2),lw); og.save('og.jpg',quality=88)
open('CNAME','w').write('papayaslice.com\n')
open('404.html','w').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/"><title>Papaya Slice</title></head><body></body></html>')
for f in ['_redirects','_headers']:
    if os.path.exists('./'+f): os.remove('./'+f)
print('ok')

# ---- externalize inline images into /img/ ----
import hashlib
os.makedirs('img',exist_ok=True)
seen={}; NUEVAS=set()  # imágenes nuevas de este build (las existentes no se reescriben)
def ext_images(path):
    h=open(path).read()
    def rep(m):
        mime,b64=m.group(1),m.group(2)
        key=hashlib.sha1(b64.encode()).hexdigest()[:10]
        if key not in seen:
            ext={'png':'png','jpeg':'jpg','webp':'webp'}[mime]
            fn=f'img/{key}.{ext}'; seen[key]=fn
            if not os.path.exists('./'+fn): open('./'+fn,'wb').write(base64.b64decode(b64)); NUEVAS.add(fn)
        return '/'+seen[key]
    h2=re.sub(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)',rep,h)
    open(path,'w').write(h2); print(path,len(h)//1024,'KB ->',len(h2)//1024,'KB')
ext_images('index.html'); ext_images('menu.html'); ext_images('playa-del-carmen.html'); ext_images('cancun.html')
# ---- foto principal responsive (LCP): variantes 480/800/1200 ≤120 KB, srcset y fetchpriority ----
HERO_W=(480,800,1200)
def hero_variants(src):
    base=src[len('/img/'):].rsplit('.',1)[0]; im=None; out=[]
    for w in HERO_W:
        fn=f'img/{base}-{w}.webp'
        if not os.path.exists(fn):
            if im is None: im=Image.open(src.lstrip('/')).convert('RGB')
            r=im.resize((w,round(im.height*w/im.width)),Image.LANCZOS)
            for q in (72,66,60,55,50,45):
                b=io.BytesIO(); r.save(b,'WEBP',quality=q,method=6,sharp_yuv=True)
                if len(b.getvalue())<=120*1024: break
            open(fn,'wb').write(b.getvalue())
        out.append((fn,w))
    return out
def responsive_hero(path):
    h=open(path,encoding='utf-8').read()
    def fix(m):
        tag=m.group(0); src=re.search(r'src="(/img/[0-9a-f]+\.webp)"',tag)
        if not src: return tag
        im=Image.open(src.group(1).lstrip('/'))
        if im.width<=1200: return tag
        v=hero_variants(src.group(1)); W,H=v[-1][1],round(im.height*v[-1][1]/im.width)
        srcset=', '.join(f'/{f} {w}w' for f,w in v)
        tag=tag.replace(src.group(0),f'src="/{v[1][0]}" srcset="{srcset}" sizes="100vw" width="{W}" height="{H}"')
        return tag
    h2=re.sub(r'<img[^>]*fetchpriority="high"[^>]*>',fix,h)
    if h2!=h: open(path,'w',encoding='utf-8').write(h2)
for _p in ('index.html','playa-del-carmen.html'): responsive_hero(_p)
# ---- resto de fotos de la portada: WebP con srcset, width/height y lazy debajo del primer pantallazo ----
# Anchos medidos en pantalla (celular 390 px / escritorio 1372 px), por foto original.
PORTADA_SIZES={'da6e6e826c.png':(52,52),'9637a14a2b.png':(368,624),'9a2aa7b216.webp':(354,406),
  '6dd7297540.jpg':(390,457),'ae9c3f46c1.jpg':(390,457),'82de2b8ad0.jpg':(390,457),'ae8d7c9255.png':(354,362)}
ARRIBA={'da6e6e826c.png','9637a14a2b.png'}
SIN_WH={'9a2aa7b216.webp'}  # su CSS la muestra cuadrada: width/height cambiarían el alto  # visibles al cargar en celular: sin lazy
def webp_set(name,max_css):
    """Variantes WebP del original para cubrir hasta 3x el ancho mostrado. Devuelve [(ruta, ancho)]."""
    base,ext=name.rsplit('.',1); im=Image.open('img/'+name); W,H=im.size
    alpha=im.mode in ('RGBA','LA','P')
    need=min(W,max_css*3)
    ws=sorted({w for w in (120,240,480,800,1200) if w<need}|{need})
    out=[]
    for w in ws:
        fn=f'img/{base}-{w}w.webp'
        if not os.path.exists(fn):
            r=(im.convert('RGBA') if alpha else im.convert('RGB')).resize((w,round(H*w/W)),Image.LANCZOS)
            r.save(fn,'WEBP',quality=(85 if alpha else 72),method=6)
        out.append((fn,w))
    return out,W,H
def portada_imgs(path):
    h=open(path,encoding='utf-8').read()
    def fix(m):
        tag=m.group(0)
        if 'srcset=' in tag: return tag
        sm=re.search(r'src="/img/([0-9a-f]+\.(?:png|jpg|jpeg|webp))"',tag)
        if not sm or sm.group(1) not in PORTADA_SIZES: return tag
        name=sm.group(1); mob,desk=PORTADA_SIZES[name]
        vs,W,H=webp_set(name,max(mob,desk))
        sizes='100vw' if mob>=390 and desk>=1000 else (f'(min-width: 900px) {desk}px, 100vw' if mob>=390 else f'(min-width: 900px) {desk}px, {mob}px')
        mid=vs[min(1,len(vs)-1)][0]
        new=f'src="/{mid}" srcset="'+', '.join(f'/{f} {w}w' for f,w in vs)+f'" sizes="{sizes}"'
        tag=tag.replace(sm.group(0),new)
        if 'width=' not in tag and name not in SIN_WH: tag=tag.replace('<img ',f'<img width="{W}" height="{H}" ',1)
        if name not in ARRIBA:
            if 'loading=' not in tag: tag=tag.replace('<img ','<img loading="lazy" ',1)
            if 'decoding=' not in tag: tag=tag.replace('<img ','<img decoding="async" ',1)
        return tag
    h2=re.sub(r'<img [^>]*>',fix,h)
    # fotos de platillos pintadas con JavaScript (mapa IMG): WebP de hasta 800 px (se muestran a 240-324 px)
    def fixmap(m):
        d=json.loads(m.group(1))
        for k,v in d.items():
            name=v.rsplit('/',1)[1]
            if name.endswith('.jpg') or name.endswith('.png'):
                vs,W,H=webp_set(name,267); d[k]='/'+vs[-1][0]
        return 'const IMG = '+json.dumps(d)
    h2=re.sub(r'const IMG = (\{[^}]*\})',fixmap,h2,count=1)
    if h2!=h: open(path,'w',encoding='utf-8').write(h2)
portada_imgs('index.html')
print(len(seen),'imágenes', sum(os.path.getsize('./'+f) for f in seen.values())//1024,'KB')

# ---- recomprimir imágenes del sitio (ligeras para móvil) ----
for p in sorted(NUEVAS):
    f=os.path.basename(p); s0=os.path.getsize(p)
    try:
        if f.endswith('.jpg'):
            im=Image.open(p).convert('RGB'); im.thumbnail((900,1350)); b=io.BytesIO(); im.save(b,'JPEG',quality=76,optimize=True,progressive=True)
        elif f.endswith('.webp'):
            continue  # WebP ya viene optimizado; la portada debe quedar en alta definición
        else: continue
        if len(b.getvalue())<s0: open(p,'wb').write(b.getvalue())
    except Exception as e: print('skip',f,e)

# ---- robots.txt: política del Estándar SEO GMBH 2.0, punto 13 (igual que Mu) ----
open('robots.txt','w').write("""# papayaslice.com — política de rastreo (Estándar SEO GMBH 2.0, punto 13)
# Búsqueda: permitidos
User-agent: Googlebot
User-agent: Bingbot
User-agent: OAI-SearchBot
User-agent: ChatGPT-User
User-agent: PerplexityBot
User-agent: Perplexity-User
User-agent: Claude-SearchBot
User-agent: Claude-User
User-agent: Applebot
Allow: /

# Entrenamiento de modelos: permitidos
User-agent: Google-Extended
User-agent: GPTBot
User-agent: ClaudeBot
User-agent: Applebot-Extended
User-agent: CCBot
Allow: /

# Resto de agentes
User-agent: *
Allow: /

Sitemap: https://papayaslice.com/sitemap.xml
""")

# ---- sitemap.xml con lastmod real: la fecha solo cambia cuando cambia la página (src/lastmod.json) ----
import datetime
SM=[('/','index.html','weekly','1.0'),('/menu','menu.html','weekly','0.9'),('/playa-del-carmen','playa-del-carmen.html','monthly','0.8'),('/cancun','cancun.html','monthly','0.8'),('/privacidad','privacidad.html','yearly','0.2')]
LM_F='src/lastmod.json'
LM=json.load(open(LM_F,encoding='utf-8')) if os.path.exists(LM_F) else {}
hoy=datetime.date.today().isoformat()
for url,f,_,_ in SM:
    hsh=hashlib.sha256(open(f,'rb').read()).hexdigest()[:16]
    if LM.get(url,{}).get('hash')!=hsh: LM[url]={'hash':hsh,'fecha':hoy}
open(LM_F,'w',encoding='utf-8').write(json.dumps(LM,ensure_ascii=False,indent=1)+'\n')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n'+''.join(f'<url><loc>{D}{u}</loc><lastmod>{LM[u]["fecha"]}</lastmod><changefreq>{cf}</changefreq><priority>{pr}</priority></url>\n' for u,_,cf,pr in SM)+'</urlset>\n')
