#!/bin/bash
yum config-manager --add-repo /etc/yum.repos.d/CentOS-Linux-PowerTools.repo
yum config-manager --set-enabled PowerTools

yum install -y git gcc gcc-c++ autoconf automake asciidoc bash-completion xmlto libtool pkgconfig glib2 glib2-devel libfabric libfabric-devel doxygen graphviz pandoc ncurses kmod kmod-devel libudev-devel libuuid-devel json-c-devel keyutils-libs-devel gem make cmake libarchive clang-tools-extra hwloc-devel perl-Text-Diff gflags-devel

yum install -y daxctl.x86_64 daxctl-devel.x86_64 daxctl-libs.x86_64

yum install -y ndctl.x86_64 ndctl-devel.x86_64 ndctl-libs.x86_64

yum install -y libatomic numactl

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
https://github.com/pmem/kvdk.git
git submodule init 
git submodule update
mkdir -p build && cd build
cmake .. -DCMAKE_BUILD_TYPE=Release && make -j