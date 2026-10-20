# papayaslice.com — sitio oficial de Papaya Slice (pizzería, Playa del Carmen y Cancún)

Publica con **GitHub Pages** desde `main` (raíz). Los HTML de la raíz (`index.html`, `menu.html`, `playa-del-carmen.html`,
`cancun.html`), `img/`, `sitemap.xml`, etc. **se generan**: nunca se editan a mano.

## Cómo cambiar algo
1. Edita **`contenido.json`** (fuente única de verdad):
   - `menu`: secciones, platillos, precios (MXN), descripciones ES/EN (`{"es":…,"en":…}`), `nuevo`, `img`, `cut`, bebidas.
   - `portada`: cintas de texto (`mq1`, `mq2`) y platillos destacados (`dishes`, con `anchor` = id de la sección del menú).
   - `sucursales`: por sucursal, dirección, teléfono, WhatsApp, Maps, Rappi/Uber (`null` = no se muestra),
     horario (`hours`: `default` y excepciones por día `"0"`=domingo … `"6"`=sábado; `null` = cerrado),
     `landing` (textos de su página) y `schema` (datos para Google: CP, coordenadas).
     El horario alimenta la portada, la landing y los datos estructurados de Google a la vez.
   - `seo`: title y description de cada página. `sitio`: dominio, GA4, verificación de Search Console, Instagram, WhatsApp de reservas.
2. Diseño: `src/menu/menu_template.html`, `src/landing/landing_template.html`, `src/locations/build.py` (HTML de las landings).
   Fotos: `src/menu/imgs.json` y `src/landing/imgs.json` (clave → data URI base64); se refieren con `"img":"clave"`.
3. `./build.sh` (python3 + Pillow; scipy solo para recortar fotos nuevas). Las imágenes que ya existen en `img/` no se
   reescriben; solo se crean las nuevas. Para regenerar favicon/og, bórralos antes del build.
4. Revisa `git status`: solo deben cambiar los archivos que esperas.

## Flujo obligatorio para cada cambio que pida Fernando
1. **Sincroniza primero:** `python3 tools/sincronizar.py` (deja la copia local igual a `main`).
2. Edita `contenido.json` (o plantillas), corre `./build.sh` y revisa que el cambio salga en todas partes (ES y EN, portada, landings, schema).
3. **Preview** en celular (Playwright, 390 px) y resumen exacto de lo que cambia. Si algo es ambiguo (precio, nombre, etiqueta), pregunta.
4. Con el **OK de Fernando**: `git add -A && git commit -m "…"` local y publica:
   - Con acceso directo al repo: `git push origin main`.
   - Sin acceso (lo normal hoy): `python3 tools/publicar.py "mensaje"` (publica la diferencia contra la etiqueta `github-main`;
     genera `tools/out/trozo_NN.js` y `tools/out/subir.js`). Con Claude in Chrome abre
     `https://github.com/corporativo-wq/papayaslice.com/upload/main` y, con `javascript_tool` en esa misma pestaña:
     `window.__z = []; 'ok'` → el contenido de cada `trozo_NN.js` en orden → el contenido de `subir.js`.
     **No uses `file_upload`**: Chrome ya no acepta rutas de archivos del sandbox. `subir.js` revisa largo y hash del paquete
     antes de nada. Si responde `LISTO`, haz scroll al botón y clic en **Commit changes**; el primer clic por referencia
     a veces no envía: toma captura y da clic por coordenadas. Debe quedar en la página principal del repo.
     Archivos borrados se borran a mano en GitHub. Si el sistema frena la acción, pide a Fernando un OK explícito en el chat.
5. **Verifica en vivo** (~1 min): en una pestaña de https://papayaslice.com ejecuta `tools/out/verificar.js`; todo debe decir OK. Luego `python3 tools/publicar.py --hecho`.
   Nada de "debería funcionar".
6. Reporta a Fernando en 1–2 frases y recuérdale lo que hay que cambiar fuera de la web (caja/POS, menú impreso, Perfil de Google, Rappi/Uber).

## Reglas
- No cambiar nombre, horarios, teléfonos ni datos del Perfil de Google sin aprobación de Fernando.
- Si falta un dato, pregúntalo; no pongas texto de relleno ni fotos genéricas o hechas con IA.
- No mencionar otras marcas del grupo en el sitio.
- Nunca pedir tokens ni contraseñas en el chat. Cambios irreversibles (borrar fichas, archivos) los hace Fernando.
- Medición: cada CTA lleva `data-ev` (`como_llegar`, `whatsapp`, `phone`, `order_rappi`, `order_uber`, `menu_nav`, `branch_page`) y `data-branch`.

## Reglas de marca
- Fondo blanco siempre; nunca negro. Paleta: coral #F07A45, turquesa #2A9D9A, durazno #FFE7D6, crema #FFF6EC (sin amarillo).
- Sin iconografía decorativa (caritas, estrellas, rayos). El anillo giratorio "MASA MADRE · 72 HORAS" se conserva.
- Tipografías: Sofia Sans Extra Condensed 900 (nombres, precios, botones), Dela Gothic One (títulos grandes), Outfit (texto). Pendiente: comprar Druk y sustituir.
- Idiomas ES/EN con `data-es`/`data-en`. Precios en MXN.

## Datos reales (la fuente es contenido.json)
- WhatsApp reservas: +52 984 179 8683. Instagram: @papayaslicemx.
- Av. 38 (Playa del Carmen): Calle 38 entre 5a Av. y Calle Flamingos, Locales Miranda #4. 13:00–23:30 todos los días. Rappi 1930135819. Uber Eats store WmePdADXWy-KCQKVOP7y5Q.
- Náder (Cancún): Av. Carlos Náder 44, Centro. Lun cerrado; Mar–Mié y Dom 14:00–22:00; Jue–Sáb 14:00–23:00. Rappi 1930378884. Sin Uber Eats. WhatsApp reservas Náder: +52 998 174 6115.
