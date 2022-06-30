#!/bin/bash

export http_proxy=http://child-prc.intel.com:913
export https_proxy=http://child-prc.intel.com:913
export ftp_proxy=https://child-prc.intel.com:913
export socks_proxy=http://child-prc.intel.com:913

sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-*

yum config-manager --add-repo /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
yum config-manager --set-enabled PowerTools

yum install -y git gcc gcc-c++ autoconf automake asciidoc bash-completion xmlto libtool pkgconfig glib2 glib2-devel libfabric libfabric-devel doxygen graphviz pandoc ncurses kmod kmod-devel libudev-devel libuuid-devel json-c-devel keyutils-libs-devel gem make cmake libarchive clang-tools-extra hwloc-devel perl-Text-Diff gflags-devel libatomic numactl

yum install -y daxctl.x86_64 daxctl-devel.x86_64 daxctl-libs.x86_64 ndctl.x86_64 ndctl-devel.x86_64 ndctl-libs.x86_64

pip3 install GitPython

mkdir -p /home/chengxiang/ && cd /home/chengxiang/
git clone https://github.com/pmem/pmdk.git
cd pmdk
git checkout 1.11.1
make
sudo make install

cd /home/chengxiang/
wget https://github.com/Kitware/CMake/releases/download/v3.12.4/cmake-3.12.4.tar.gz
tar vzxf cmake-3.12.4.tar.gz
cd cmake-3.12.4
./bootstrap
make
sudo make install

cd /home/chengxiang/
git clone https://github.com/pmem/kvdk.git
cd kvdk/
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j

echo c++ 14 --------------------------------------------------------------------------------------------------------

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