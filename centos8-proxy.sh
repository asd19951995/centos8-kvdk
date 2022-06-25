#!/bin/bash

export http_proxy=http://child-prc.intel.com:913 
export https_proxy=http://child-prc.intel.com:913
export ftp_proxy=https://child-prc.intel.com:913
export socks_proxy=http://child-prc.intel.com:913

sed -i -e "s|mirrorlist=|#mirrorlist=|g" /etc/yum.repos.d/CentOS-*
sed -i -e "s|#baseurl=http://mirror.centos.org|baseurl=http://vault.centos.org|g" /etc/yum.repos.d/CentOS-*
