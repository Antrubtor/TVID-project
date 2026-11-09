if [ ! -d "videos" ]; then
    wget -c -O videos.zip "https://nc.cyberdra.net/s/o2XGqepknKDemrs/download?path=%2FTP%2Fvideos"
    unzip videos.zip
    rm videos.zip
fi

if [ ! -d ".venv" ]; then
    uv sync
fi

if [ ! -d "mpeg2dec" ]; then
    git clone git@github.com:aholtzma/mpeg2dec.git
    cd mpeg2dec
    ./configure
    if [ "$OSTYPE" != "darwin"* ]; then
        sed -i "s/#define inline __attribute__ ((__always_inline__))/\/\/#define inline \_\_attribute\_\_ \(\(\_\_always_inline\_\_\)\)/g" include/config.h # pour compiler sur mac
    fi
    make -j$(nproc)
    cd ..
fi

if [ -d "encoded_images" ]; then
    rm -rf encoded_images
fi

mkdir -p encoded_images/bw_numbers encoded_images/Jaggies1 encoded_images/lci encoded_images/pendulum
cd encoded_images/bw_numbers
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/bw_numbers.m2v
cd ../../encoded_images/Jaggies1
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/Jaggies1.m2v
cd ../../encoded_images/lci
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/lci.m2v
cd ../../encoded_images/pendulum
../../mpeg2dec/src/mpeg2dec -o pgm ../../videos/elementary/pendulum.m2v
