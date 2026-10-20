import json
# El menú vive en contenido.json (raíz del repo) → "menu". No lo edites aquí.
MENU = json.load(open("../../contenido.json", encoding="utf-8"))["menu"]

imgs = json.load(open('imgs.json'))
logo = imgs.pop('logo')
html = open('menu_template.html').read()
html = html.replace('__LOGOW__', imgs.pop('logo_w')).replace('__LOGO__', logo).replace('__IMGS__', json.dumps(imgs)).replace('__MENU__', json.dumps(MENU, ensure_ascii=False))
open('../../build/papaya-slice-menu.html','w').write(html)
print(len(html)//1024, 'KB')
