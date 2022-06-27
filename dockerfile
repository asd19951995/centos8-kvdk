FROM 8378006361/centos8.2.2004:v3

ADD kvdk-install.sh /usr/bin/kvdk-install.sh

RUN chmod +x /usr/bin/kvdk-install.sh

ENTRYPOINT ["/usr/bin/kvdk-install.sh"]
