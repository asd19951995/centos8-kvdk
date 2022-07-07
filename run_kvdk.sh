#!/bin/bash

export http_proxy=http://child-prc.intel.com:913
export https_proxy=http://child-prc.intel.com:913
export ftp_proxy=https://child-prc.intel.com:913
export socks_proxy=http://child-prc.intel.com:913


cd /home/chengxiang/
rm -rf kvdk/
git clone https://github.com/pmem/kvdk.git
cd kvdk/
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j

echo c++ 17 --------------------------------------------------------------------------------------------------------

cd /home/chengxiang/kvdk/
rm -rf build/
sed -i '11s/11/17/g' CMakeLists.txt
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j

echo c++ 14 --------------------------------------------------------------------------------------------------------

cd /home/chengxiang/kvdk/
rm -rf build/
sed -i '11s/17/14/g' CMakeLists.txt
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j

echo c++ 11 --------------------------------------------------------------------------------------------------------

cd /home/chengxiang/kvdk/
rm -rf build/
sed -i '11s/14/11/g' CMakeLists.txt
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j