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
LD_MENU=json.dumps({"@context":"https://schema.org","@type":"Menu","@id":D+"/menu/#menu","name":"Menú Papaya Slice","url":D+"/menu","inLanguage":"es-MX","hasMenuSection":[{"@type":"MenuSection","name":(m.get("short") or m["title"])["es"]} for m in C["menu"]]},ensure_ascii=False)
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
    while i<len(lines) and (lines[i].startswith('<meta') or lines[i].startswith('<link')): headlines.append(lines[i]); i+=1
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
open('index.html','w').write(wrap(L,SEO['inicio']['title'],SEO['inicio']['description'],'/',LD_HOME))
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
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://papayaslice.com/sitemap.xml\n')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://papayaslice.com/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n<url><loc>https://papayaslice.com/menu</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>\n<url><loc>https://papayaslice.com/playa-del-carmen</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n<url><loc>https://papayaslice.com/cancun</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n<url><loc>https://papayaslice.com/privacidad</loc><changefreq>yearly</changefreq><priority>0.2</priority></url>\n</urlset>\n')
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
