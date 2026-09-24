# papayaslice.com — sitio oficial de Papaya Slice (pizzería, Playa del Carmen y Cancún)

Este repositorio publica el sitio con **GitHub Pages** desde la rama `main` (raíz). Todo lo que esté en la raíz
(`index.html`, `menu.html`, `img/`, etc.) es lo que se ve en https://papayaslice.com. **No edites esos archivos a mano**:
se generan desde `src/`.

## Cómo hacer un cambio (menú, precios, textos, horarios, fotos)
1. Edita la fuente:
   - **Menú (platillos, precios, descripciones, secciones, bebidas):** `src/menu/build.py` → diccionario `MENU`. Cada platillo tiene `n` (nombre ES/EN con `b("es","en")`), `d` (descripción), `p` (precio MXN), opcional `img`, `nuevo`, `cut` (foto recortada que gira).
   - **Portada (textos, sucursales, horarios, links de Rappi/Uber/WhatsApp, platillos destacados):** `src/landing/build.py` → diccionario `D` y constantes `MENU_URL`, `WATI`.
   - **Diseño/HTML/CSS:** `src/menu/menu_template.html` y `src/landing/landing_template.html`.
   - **Fotos:** `src/menu/imgs.json` y `src/landing/imgs.json` (clave → data URI base64). Para agregar una foto nueva, guárdala ahí con una clave y refiérela con `"img":"clave"`.
   - **SEO (title, description, datos estructurados, sitemap):** `src/site_build.py`.
2. Regenera: `./build.sh` (requiere python3 con Pillow; scipy solo si se recortan fotos nuevas).
3. `git add -A && git commit -m "…" && git push origin main`. GitHub Pages publica en ~1 minuto.

## Reglas de marca (acordadas con el dueño, Fernando)
- Fondo blanco siempre; nunca negro. Paleta: coral #F07A45, turquesa #2A9D9A, durazno #FFE7D6, crema #FFF6EC (sin amarillo).
- Sin iconografía decorativa (caritas, estrellas, rayos). El anillo giratorio "MASA MADRE · 72 HORAS" se conserva.
- Tipografías: Sofia Sans Extra Condensed 900 (nombres, precios, botones), Dela Gothic One (títulos grandes), Outfit (texto). Pendiente: comprar Druk (Condensed Super + Wide Super) y sustituir.
- Idiomas ES/EN con `data-es`/`data-en`. Precios en MXN.
- Fotos temporales de Aperol se sustituirán por fotos propias.

## Datos reales
- WhatsApp: +52 984 179 8683. Instagram: @papayaslicemx.
- Av. 38 (Playa del Carmen): Calle 38 entre 5a Av. y Calle Flamingos, Locales Miranda #4. 13:00–00:00 todos los días. Rappi 1930135819. Uber Eats store WmePdADXWy-KCQKVOP7y5Q.
- Náder (Cancún): Av. Carlos Náder 44, Centro. Lun cerrado; Mar–Mié y Dom 14:00–22:00; Jue–Sáb 14:00–23:00. Rappi 1930378884. Sin Uber Eats.
