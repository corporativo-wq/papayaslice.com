import json
# Los datos de la portada viven en contenido.json (raíz del repo): "portada", "sucursales" y "sitio". No los edites aquí.
C=json.load(open('../../contenido.json',encoding='utf-8'))
MENU_URL=C["sitio"]["menu_url"]
WATI=C["sitio"]["wati"]
P=C["portada"]
BRANCHES={k:{x:y for x,y in v.items() if x not in('landing','schema')} for k,v in C["sucursales"].items()}
D={"menuUrl":MENU_URL,"mq1":P["mq1"],"mq2":P["mq2"],"dishes":P["dishes"],"branches":BRANCHES,"quotes":P["quotes"]}
# --- build ---
imgs=json.load(open('imgs.json')); imgs.pop('aperol2',None)
h=open('landing_template.html').read()
h=h.replace('__LOGO__',imgs.pop('logo')).replace('__GIRL__',imgs.pop('girl')).replace('__LOGOW__',imgs.pop('logo_w')).replace('__LOGOCREAM__',imgs.pop('logo_cream')).replace('__PIZZA__',imgs['hero_png']).replace('__TORONJA__',imgs.pop('toronja')).replace('__APEROL1__',imgs.pop('aperol1')).replace('__HUGO__',imgs.pop('hugo'))
h=h.replace('__WATI__',WATI).replace('__MENU__',MENU_URL)
h=h.replace('__IMGS__',json.dumps(imgs)).replace('__DATA__',json.dumps(D,ensure_ascii=False))
open('../../build/papaya-slice-landing.html','w').write(h)
print(len(h)//1024,'KB')
