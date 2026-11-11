cd "$(dirname "$0")"
cd ../mpeg2dec

# Déclare les fichiers non suivis à inclure dans le patch (sans les stager)
git add -N .clang-format .clangd
git diff HEAD > ../patchs/mpeg2dec.patch
