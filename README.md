install 

cd centos8-kvdk/
docker build -t centos8 .
docker run -it --name centos8 -v /mnt/pmem0:/mnt/pmem0