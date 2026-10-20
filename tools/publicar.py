#!/usr/bin/env python3
"""Prepara la publicación en GitHub sin acceso directo al repo (vía Claude in Chrome, página "Upload files").

Uso (desde la raíz del repo, después de ./build.sh y del OK de Fernando):
    python3 tools/publicar.py "Mensaje del commit"            # toma los archivos cambiados según git
    python3 tools/publicar.py "Mensaje" archivo1 archivo2 ...  # o una lista explícita

Genera:
  tools/out/payload.txt  → los cambios comprimidos (gzip + base64).
  tools/out/trozo_00.js, trozo_01.js, …  → el paquete partido en trozos de 8000 caracteres. NO se usa file_upload
                           (Chrome ya no acepta rutas de archivos del sandbox): el paquete se mete por javascript_tool.
  tools/out/subir.js     → se ejecuta con javascript_tool en https://github.com/<REPO>/upload/main.
     Pasos en Chrome (cada uno es una llamada a javascript_tool, en la misma pestaña, sin recargarla):
       (a) window.__z = []; 'ok'
       (b) el contenido de cada trozo_NN.js, en orden (cada uno responde cuántos trozos van)
       (c) el contenido de subir.js: revisa largo y hash del paquete, descarga main, aplica los cambios, comprueba
           hashes antes y después, mete los archivos en el formulario y llena el mensaje
       (d) scroll al botón y clic en "Commit changes" (si el clic por ref no envía, clic por coordenadas).
  tools/out/verificar.js → se ejecuta en una pestaña de https://papayaslice.com/ ~1 min después:
                           compara el hash de cada archivo publicado contra el build local.

Base: la etiqueta git `github-main` marca lo que hay en GitHub (la pone tools/sincronizar.py). Se publica la
diferencia entre esa etiqueta y tu copia actual. Si GitHub cambió desde entonces, el hash "antes" falla y no se sube nada.
Cuando verificar.js diga OK en todo:  python3 tools/publicar.py --hecho   (mueve `github-main` a tu HEAD).
Archivos de texto: se mandan como parches mínimos (comprimidos). Nuevos o binarios (imágenes): completos.
"""
import base64, difflib, gzip, hashlib, json, os, re, subprocess, sys

REPO = "corporativo-wq/papayaslice.com"
SITE = "https://papayaslice.com"
ATTR = ("Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>")
TOK = re.compile(r"\w+|\s+|[^\w\s]")
TEXT_EXT = {".html", ".json", ".py", ".md", ".txt", ".xml", ".css", ".js", ".sh", ".svg", ""}


def git(*a):
    return subprocess.run(["git", *a], capture_output=True, check=False).stdout


def u16(s):
    return len(s.encode("utf-16-le")) // 2


def h12(b):
    return hashlib.sha256(b).hexdigest()[:12]


BASE = "github-main"


def changed_files():
    files = []
    for line in git("diff", "--name-status", BASE).decode().splitlines():
        st, path = line.split("\t", 1)
        if st.startswith("D"):
            print("AVISO: archivo borrado (no se puede borrar por Upload files; bórralo a mano en GitHub):", path)
        else:
            files.append(path)
    files += git("ls-files", "--others", "--exclude-standard").decode().split()
    return [f for f in dict.fromkeys(files) if not f.startswith("tools/out/")]


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    if not git("rev-parse", "-q", "--verify", BASE).strip():
        sys.exit("Falta la etiqueta github-main: corre primero python3 tools/sincronizar.py")
    if sys.argv[1] == "--hecho":
        git("tag", "-f", BASE, "HEAD"); print("github-main → HEAD (publicado y verificado)."); return
    msg = sys.argv[1]
    files = sys.argv[2:] or changed_files()
    if not files:
        sys.exit("No hay cambios que publicar.")
    P, H, NEW = {}, {}, {}
    for f in files:
        new_b = open(f, "rb").read()
        r = subprocess.run(["git", "show", f"{BASE}:{f}"], capture_output=True)
        old_b = r.stdout if r.returncode == 0 else None
        is_text = os.path.splitext(f)[1].lower() in TEXT_EXT
        if old_b is not None and is_text:
            old, new = old_b.decode("utf-8"), new_b.decode("utf-8")
            a, b = TOK.findall(old), TOK.findall(new)
            pos = [0]
            for x in a:
                pos.append(pos[-1] + u16(x))
            ops = [[pos[i1], pos[i2], "".join(b[j1:j2])]
                   for t, i1, i2, j1, j2 in difflib.SequenceMatcher(None, a, b, autojunk=False).get_opcodes() if t != "equal"]
            o = old.encode("utf-16-le")  # verificación local del parche
            for s_, e_, t_ in reversed(ops):
                o = o[:2 * s_] + t_.encode("utf-16-le") + o[2 * e_:]
            assert o.decode("utf-16-le") == new, f
            P[f] = ops
            H[f] = [h12(old_b), h12(new_b)]
        else:
            NEW[f] = base64.b64encode(new_b).decode()
            H[f] = [None, h12(new_b)]
    payload = base64.b64encode(gzip.compress(json.dumps({"P": P, "N": NEW, "H": H}, ensure_ascii=False).encode())).decode()
    os.makedirs("tools/out", exist_ok=True)
    open("tools/out/payload.txt", "w").write(payload)
    for old in os.listdir("tools/out"):
        if old.startswith("trozo_"): os.remove("tools/out/" + old)
    N = 8000
    trozos = [payload[i:i + N] for i in range(0, len(payload), N)]
    for k, t in enumerate(trozos):
        open(f"tools/out/trozo_{k:02d}.js", "w").write(f"window.__z.push('{t}'); 'trozo {k + 1} de {len(trozos)}: ' + window.__z.length")
    psha = hashlib.sha256(payload.encode()).hexdigest()[:12]
    js = f"""const Z=(window.__z||[]).join('');
if(Z.length!=={len(payload)}) throw new Error('Paquete incompleto: '+Z.length+' de {len(payload)} caracteres. Repite window.__z=[] y los trozos.');
const zh=[...new Uint8Array(await crypto.subtle.digest('SHA-256',new TextEncoder().encode(Z)))].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,12);
if(zh!=='{psha}') throw new Error('Paquete dañado (hash '+zh+' en vez de {psha}). Repite window.__z=[] y los trozos.');
const MSG={json.dumps(msg)}, DESC={json.dumps(ATTR)};
const u8=s=>Uint8Array.from(atob(s),c=>c.charCodeAt(0));
const J=JSON.parse(await new Response(new Blob([u8(Z)]).stream().pipeThrough(new DecompressionStream('gzip'))).text());
const sha=async b=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,12);
const enc=s=>new TextEncoder().encode(s);
const dt=new DataTransfer(), rep=[];
for(const f in J.P){{let s=await (await fetch('https://raw.githubusercontent.com/{REPO}/main/'+f+'?t='+Date.now(),{{cache:'no-store'}})).text();
 const ok0=(await sha(enc(s)))===J.H[f][0]; for(const [a,b,t] of [...J.P[f]].reverse()) s=s.slice(0,a)+t+s.slice(b);
 const ok1=(await sha(enc(s)))===J.H[f][1]; rep.push([f,ok0,ok1]); dt.items.add(new File([s],f,{{type:'text/plain'}}));}}
for(const f in J.N){{const b=u8(J.N[f]); rep.push([f,true,(await sha(b))===J.H[f][1]]); dt.items.add(new File([b],f));}}
let estado='NO SE SUBIÓ NADA: algún hash no coincide (¿el repo cambió desde tu último sync?)';
if(rep.every(r=>r[1]&&r[2])){{const i=document.querySelector('#upload-manifest-files-input');i.files=dt.files;i.dispatchEvent(new Event('change',{{bubbles:true}}));
 await new Promise(r=>setTimeout(r,5000));
 const set=(el,v)=>{{Object.getOwnPropertyDescriptor(Object.getPrototypeOf(el),'value').set.call(el,v);el.dispatchEvent(new Event('input',{{bubbles:true}}));}};
 set(document.querySelector('#commit-summary-input'),MSG); set(document.querySelector('#commit-description-textarea'),DESC);
 document.querySelector('input[value=direct]')?.click(); estado='LISTO: revisa la lista de archivos y da clic en Commit changes';}}
JSON.stringify({{estado,rep}})
"""
    open("tools/out/subir.js", "w", encoding="utf-8").write(js)
    exp = {f: H[f][1] for f in H}
    ver = f"""const exp={json.dumps(exp)};
const sha=async b=>[...new Uint8Array(await crypto.subtle.digest('SHA-256',b))].map(x=>x.toString(16).padStart(2,'0')).join('').slice(0,12);
const out=[];for(const f in exp){{if(f.startsWith('src/')||f.startsWith('tools/')||/\\.(py|md|sh)$/.test(f)||f==='contenido.json')continue;
 const b=await (await fetch('/'+f+'?t='+Date.now(),{{cache:'no-store'}})).arrayBuffer();out.push(f+((await sha(b))===exp[f]?' OK':' DIFERENTE (espera 1 min y repite)'));}}
out.join('\\n')||'Sin archivos públicos que verificar (solo fuentes).'
"""
    open("tools/out/verificar.js", "w", encoding="utf-8").write(ver)
    print(f"{len(H)} archivos ({len(P)} parches, {len(NEW)} completos) · payload {len(payload)//1024} KB")
    print(f"Paquete: {len(payload)} caracteres, sha {psha}, {len(trozos)} trozos (tools/out/trozo_00.js …)")
    print("1) Abre https://github.com/%s/upload/main y con javascript_tool: window.__z = []; 'ok'" % REPO)
    print("   luego cada trozo_NN.js en orden y al final tools/out/subir.js (debe responder LISTO)")
    print("2) Clic en 'Commit changes'. 3) A ~1 min, en %s ejecuta tools/out/verificar.js" % SITE)
    if len(trozos) > 12:
        print("AVISO: muchos trozos; considera publicar en varias tandas pasando listas de archivos.")


if __name__ == "__main__":
    main()
