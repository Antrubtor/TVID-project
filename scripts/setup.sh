#!/usr/bin/env bash

set -eou pipefail

cd "$(dirname "$0")"
cd ..


if [ ! -d "videos" ]; then
    wget -c -O videos.zip "https://nc.cyberdra.net/s/o2XGqepknKDemrs/download?path=%2FTP%2Fvideos"
    unzip videos.zip
    rm videos.zip
fi


if [ ! -d "mpeg2dec" ]; then
    git clone git@github.com:aholtzma/mpeg2dec.git
    ./scripts/apply_patch.sh
    cd mpeg2dec

    if [ "$(uname)" = "Darwin" ]; then
        ac_cv_build=aarch64-apple-darwin ac_cv_host=aarch64-apple-darwin ./configure --disable-sdl --without-x
        sed -i.bak "s/#define inline __attribute__ ((__always_inline__))/\/\/#define inline \_\_attribute\_\_ \(\(\_\_always_inline\_\_\)\)/g" include/config.h # pour compiler sur mac
    else
        ./configure
    fi

    make -j$(nproc)
    cd ..
fi


if [ -d "encoded_images" ]; then
    rm -rf encoded_images
fi


mkdir -p encoded_images/bw_numbers encoded_images/Jaggies1 encoded_images/lci encoded_images/pendulum encoded_images/cnn encoded_images/ctv1 encoded_images/ctv2 encoded_images/ctv3
cd encoded_images/bw_numbers
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/bw_numbers.m2v
cd ../../encoded_images/Jaggies1
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/Jaggies1.m2v
cd ../../encoded_images/lci
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/lci.m2v
cd ../../encoded_images/pendulum
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/pendulum.m2v

cd ../../encoded_images/cnn
../../mpeg2dec/src/mpeg2dec -t 0x1422 -o pgm ../../videos/ts/cnn.ts
cd ../../encoded_images/ctv1
../../mpeg2dec/src/mpeg2dec -t 0x3e9 -o pgm ../../videos/ts/ctv.ts
cd ../../encoded_images/ctv2
../../mpeg2dec/src/mpeg2dec -t 0x3f3 -o pgm ../../videos/ts/ctv.ts
cd ../../encoded_images/ctv3
../../mpeg2dec/src/mpeg2dec -t 0x3fd -o pgm ../../videos/ts/ctv.ts


cd ../..
uv sync
