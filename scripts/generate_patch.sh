cd "$(dirname "$0")"
cd ../mpeg2dec

git add -N .clang-format .clangd
git diff HEAD > ../patchs/mpeg2dec.patch
