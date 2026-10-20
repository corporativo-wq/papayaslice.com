#!/usr/bin/env python3
"""Pone la copia local al día con main en GitHub ANTES de hacer cambios (sin acceso directo al repo).

Uso:  python3 tools/sincronizar.py
Descarga de raw.githubusercontent.com cada archivo que git conoce, reemplaza los que cambiaron y hace un
commit local "Sync con main". Si alguien subió archivos NUEVOS en GitHub, este script no los ve: revisa la
lista de archivos del repo en el navegador (https://github.com/corporativo-wq/papayaslice.com) si dudas.
"""
import subprocess, sys, urllib.request, time

REPO = "corporativo-wq/papayaslice.com"
if subprocess.run(["git", "status", "--porcelain"], capture_output=True).stdout.strip():
    sys.exit("Hay cambios locales sin commit. Guárdalos o descártalos antes de sincronizar.")
files = subprocess.run(["git", "ls-files"], capture_output=True, text=True).stdout.split()
changed = []
for f in files:
    url = f"https://raw.githubusercontent.com/{REPO}/main/{urllib.request.quote(f)}?t={int(time.time())}"
    try:
        remote = urllib.request.urlopen(url, timeout=30).read()
    except Exception as e:
        print("no se pudo bajar", f, e); continue
    if open(f, "rb").read() != remote:
        open(f, "wb").write(remote); changed.append(f)
# OJO: sincroniza sobre HEAD; si HEAD tiene cambios que aún no están en GitHub, publícalos antes.
if changed:
    subprocess.run(["git", "add", "-A"]); subprocess.run(["git", "commit", "-qm", "Sync con main en GitHub"])
    print("Actualizados:", *changed, sep="\n  ")
else:
    print("La copia local ya es igual a main.")
subprocess.run(["git", "tag", "-f", "github-main", "HEAD"], capture_output=True)  # base para tools/publicar.py
