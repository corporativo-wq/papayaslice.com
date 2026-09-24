#!/usr/bin/env bash
# Reconstruye papayaslice.com a partir de src/ y deja los archivos publicables en la raíz del repo.
set -e
cd "$(dirname "$0")"
mkdir -p build
( cd src/menu && python3 build.py )
( cd src/landing && python3 build.py )
python3 src/site_build.py
echo "OK: index.html, menu.html e img/ regenerados. Haz commit y push a main para publicar."
