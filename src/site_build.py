import json,base64,io,re,os,shutil
from PIL import Image
D='https://papayaslice.com'
os.makedirs('.',exist_ok=True)
LD_HOME=json.dumps({
 "@context":"https://schema.org","@graph":[
  {"@type":"Organization","@id":D+"/#org","name":"Papaya Slice","url":D+"/","logo":D+"/favicon.png","sameAs":["https://www.instagram.com/papayaslicemx"]},
  {"@type":"WebSite","@id":D+"/#site","url":D+"/","name":"Papaya Slice","inLanguage":"es-MX","publisher":{"@id":D+"/#org"}},
  {"@type":"Restaurant","@id":D+"/#av38","name":"Papaya Slice · Av. 38","url":D+"/playa-del-carmen","image":D+"/og.jpg","telephone":"+52 984 803 5648","priceRange":"$$","servesCuisine":["Pizza","Italiana"],"sameAs":["https://www.instagram.com/papayaslicemx"],"menu":D+"/menu","acceptsReservations":"True","parentOrganization":{"@id":D+"/#org"},
   "address":{"@type":"PostalAddress","streetAddress":"Calle 38 entre 5a Av. y Calle Flamingos, Locales Miranda #4, Centro","addressLocality":"Playa del Carmen","addressRegion":"Quintana Roo","postalCode":"77710","addressCountry":"MX"},
   "geo":{"@type":"GeoCoordinates","latitude":20.6345583,"longitude":-87.0643145},"hasMap":"https://www.google.com/maps/search/?api=1&query=Papaya%20Slice%20Playa%20del%20Carmen&query_place_id=ChIJNSS3HGtDTo8RPtVX0R9kA34",
   "openingHoursSpecification":[{"@type":"OpeningHoursSpecification","dayOfWeek":["Monday","Tuesday","Wednesday","Thursday","Friday","Saturday","Sunday"],"opens":"13:00","closes":"00:00"}]},
  {"@type":"Restaurant","@id":D+"/#nader","name":"Papaya Slice · Náder","url":D+"/cancun","image":D+"/og.jpg","telephone":"+52 998 174 6115","priceRange":"$$","servesCuisine":["Pizza","Italiana"],"sameAs":["https://www.instagram.com/papayaslicemx"],"menu":D+"/menu","acceptsReservations":"True","parentOrganization":{"@id":D+"/#org"},
   "address":{"@type":"PostalAddress","streetAddress":"Av. Carlos Náder 44, Centro","addressLocality":"Cancún","addressRegion":"Quintana Roo","postalCode":"77750","addressCountry":"MX"},
   "geo":{"@type":"GeoCoordinates","latitude":21.1642827,"longitude":-86.8236381},"hasMap":"https://www.google.com/maps/search/?api=1&query=Papaya%20Slice%20Nader%20Cancun&query_place_id=ChIJP8gEC1ktTI8RI6subVZflxw",
   "openingHoursSpecification":[
     {"@type":"OpeningHoursSpecification","dayOfWeek":["Tuesday","Wednesday","Sunday"],"opens":"14:00","closes":"22:00"},
     {"@type":"OpeningHoursSpecification","dayOfWeek":["Thursday","Friday","Saturday"],"opens":"14:00","closes":"23:00"}]}
 ]},ensure_ascii=False)
GRAPH=json.loads(LD_HOME)["@graph"]
ORG=GRAPH[0]; R38=[x for x in GRAPH if x.get("@id")==D+"/#av38"][0]; RNA=[x for x in GRAPH if x.get("@id")==D+"/#nader"][0]
def ld_loc(r,slug,city):
    r=dict(r); r["@id"]=D+"/"+slug+"/#restaurant"; r["url"]=D+"/"+slug
    return json.dumps({"@context":"https://schema.org","@graph":[ORG,r,
      {"@type":"BreadcrumbList","itemListElement":[{"@type":"ListItem","position":1,"name":"Papaya Slice","item":D+"/"},{"@type":"ListItem","position":2,"name":city,"item":D+"/"+slug}]}]},ensure_ascii=False)
LD_38=ld_loc(R38,"playa-del-carmen","Playa del Carmen"); LD_NA=ld_loc(RNA,"cancun","Cancún")
LD_MENU=json.dumps({"@context":"https://schema.org","@type":"Menu","@id":D+"/menu/#menu","name":"Menú Papaya Slice","url":D+"/menu","inLanguage":"es-MX","hasMenuSection":[{"@type":"MenuSection","name":n} for n in ["Especial del mes","Rebanadas","Pizzas completas","Focaccias","Para empezar","Ensaladas","Pastas","Postres","Bebidas"]]},ensure_ascii=False)
# Eventos de conversión: cada clic en un elemento con data-ev se manda a window.dataLayer (lo lee GTM/GA4 cuando se instale)
# ev: como_llegar | whatsapp | phone | order_rappi | order_uber | menu_nav | branch_page ; branch: playa-del-carmen | cancun
EVENTS='''<script>
window.dataLayer=window.dataLayer||[];
document.addEventListener('click',function(e){var a=e.target.closest('[data-ev]');if(!a)return;
window.dataLayer.push({event:'cta_click',cta:a.getAttribute('data-ev'),branch:a.getAttribute('data-branch')||'',page:location.pathname,href:a.getAttribute('href')||''});
if(typeof gtag==='function'){gtag('event',a.getAttribute('data-ev'),{branch:a.getAttribute('data-branch')||'',page_path:location.pathname});}},{passive:true});
</script>
'''
def wrap(body,title,desc,path,ld):
    body=re.sub(r'^<title>.*?</title>\n','',body)
    lines=body.split('\n'); headlines=[]; i=0
    while i<len(lines) and (lines[i].startswith('<meta') or lines[i].startswith('<link')): headlines.append(lines[i]); i+=1
    rest='\n'.join(lines[i:])
    head=f'''<!doctype html>
<html lang="es-MX">
<head>
<meta charset="utf-8">
<script async src="https://www.googletagmanager.com/gtag/js?id=G-MET4FF2MEP"></script><script>window.dataLayer=window.dataLayer||[];function gtag(){{dataLayer.push(arguments);}}gtag('js',new Date());gtag('config','G-MET4FF2MEP');</script>
<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">
<title>{title}</title>
<meta name="description" content="{desc}">
<link rel="canonical" href="{D}{path}">
<meta name="robots" content="index,follow,max-image-preview:large">
<meta name="google-site-verification" content="V9eAQSvRRDtoa64PSJ6_y-MzPrVYQnG66pzsdlKXZsg">
<meta property="og:type" content="website"><meta property="og:site_name" content="Papaya Slice"><meta property="og:locale" content="es_MX">
<meta property="og:title" content="{title}"><meta property="og:description" content="{desc}">
<meta property="og:url" content="{D}{path}"><meta property="og:image" content="{D}/og.jpg"><meta property="og:image:width" content="1200"><meta property="og:image:height" content="630">
<meta name="twitter:card" content="summary_large_image">
<link rel="icon" type="image/png" sizes="192x192" href="/favicon.png"><link rel="apple-touch-icon" href="/apple-touch-icon.png">
<script type="application/ld+json">{ld}</script>
'''
    return head+'\n'.join(headlines)+'\n</head>\n<body>\n'+rest+'\n'+EVENTS+'</body>\n</html>\n'
L=open('build/papaya-slice-landing.html').read().replace('https://claude.ai/artifact/DoMWeTromrd56uR4MHRPeL','/menu')
M=open('build/papaya-slice-menu.html').read().replace('https://claude.ai/artifact/UMA9LHkZTeD8TuqugmA6Zt','/')
open('index.html','w').write(wrap(L,'Papaya Slice · Pizza de masa madre en Playa del Carmen y Cancún','Pizzería en Playa del Carmen (Calle 38) y Cancún (Av. Náder). Rebanadas estilo NY y Detroit, pizzas completas, focaccias de masa madre de 72 h y spritz. Reserva por WhatsApp o pide por Rappi y Uber Eats.','/',LD_HOME))
open('menu.html','w').write(wrap(M,'Menú y precios · Papaya Slice','Menú completo de Papaya Slice con precios en MXN: rebanadas NY y Detroit, pizzas completas, focaccias de masa madre, pastas, postres, cerveza artesanal y spritz. Playa del Carmen y Cancún.','/menu',LD_MENU))
P38=open('build/loc-playa-del-carmen.html').read(); PNA=open('build/loc-cancun.html').read()
open('playa-del-carmen.html','w').write(wrap(P38,'Pizzería en Playa del Carmen · Papaya Slice Calle 38','Papaya Slice en Playa del Carmen: pizza de masa madre de 72 h por rebanada o completa en Calle 38 entre 5a Av. y Flamingos. Horario, cómo llegar, WhatsApp, Rappi y Uber Eats.','/playa-del-carmen',LD_38))
open('cancun.html','w').write(wrap(PNA,'Pizzería en Cancún centro · Papaya Slice Av. Náder','Papaya Slice en Cancún: pizza de masa madre de 72 h por rebanada o completa en Av. Carlos Náder 44, Centro. Horario, cómo llegar, WhatsApp y Rappi.','/cancun',LD_NA))
open('google4708ea497496b16c.html','w').write('google-site-verification: google4708ea497496b16c.html')
imgs=json.load(open('src/landing/imgs.json'))
logo=Image.open(io.BytesIO(base64.b64decode(imgs['logo'].split(',')[1]))).convert('RGBA')
def icon(size,pad):
    c=Image.new('RGBA',(size,size),(255,255,255,255)); l=logo.copy(); l.thumbnail((size-2*pad,size-2*pad)); c.paste(l,((size-l.width)//2,(size-l.height)//2),l); return c
icon(192,18).save('favicon.png'); icon(180,16).convert('RGB').save('apple-touch-icon.png')
og=Image.new('RGB',(1200,630),(240,122,69)); lw=Image.open(io.BytesIO(base64.b64decode(imgs['logo_w'].split(',')[1]))).convert('RGBA'); lw.thumbnail((900,480)); og.paste(lw,((1200-lw.width)//2,(630-lw.height)//2),lw); og.save('og.jpg',quality=88)
open('robots.txt','w').write('User-agent: *\nAllow: /\nSitemap: https://papayaslice.com/sitemap.xml\n')
open('sitemap.xml','w').write('<?xml version="1.0" encoding="UTF-8"?>\n<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">\n<url><loc>https://papayaslice.com/</loc><changefreq>weekly</changefreq><priority>1.0</priority></url>\n<url><loc>https://papayaslice.com/menu</loc><changefreq>weekly</changefreq><priority>0.9</priority></url>\n<url><loc>https://papayaslice.com/playa-del-carmen</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n<url><loc>https://papayaslice.com/cancun</loc><changefreq>monthly</changefreq><priority>0.8</priority></url>\n</urlset>\n')
open('CNAME','w').write('papayaslice.com\n')
open('404.html','w').write('<!doctype html><html lang="es"><head><meta charset="utf-8"><meta http-equiv="refresh" content="0;url=/"><title>Papaya Slice</title></head><body></body></html>')
for f in ['_redirects','_headers']:
    if os.path.exists('./'+f): os.remove('./'+f)
print('ok')

# ---- externalize inline images into /img/ ----
import hashlib
os.makedirs('img',exist_ok=True)
seen={}
def ext_images(path):
    h=open(path).read()
    def rep(m):
        mime,b64=m.group(1),m.group(2)
        key=hashlib.sha1(b64.encode()).hexdigest()[:10]
        if key not in seen:
            ext={'png':'png','jpeg':'jpg','webp':'webp'}[mime]
            fn=f'img/{key}.{ext}'; open('./'+fn,'wb').write(base64.b64decode(b64)); seen[key]=fn
        return '/'+seen[key]
    h2=re.sub(r'data:image/(png|jpeg|webp);base64,([A-Za-z0-9+/=]+)',rep,h)
    open(path,'w').write(h2); print(path,len(h)//1024,'KB ->',len(h2)//1024,'KB')
ext_images('index.html'); ext_images('menu.html'); ext_images('playa-del-carmen.html'); ext_images('cancun.html')
print(len(seen),'imágenes', sum(os.path.getsize('./'+f) for f in seen.values())//1024,'KB')

# ---- recomprimir imágenes del sitio (ligeras para móvil) ----
for f in os.listdir('img'):
    p='img/'+f; s0=os.path.getsize(p)
    try:
        if f.endswith('.jpg'):
            im=Image.open(p).convert('RGB'); im.thumbnail((900,1350)); b=io.BytesIO(); im.save(b,'JPEG',quality=76,optimize=True,progressive=True)
        elif f.endswith('.webp'):
            continue  # WebP ya viene optimizado; la portada debe quedar en alta definición
        else: continue
        if len(b.getvalue())<s0: open(p,'wb').write(b.getvalue())
    except Exception as e: print('skip',f,e)
