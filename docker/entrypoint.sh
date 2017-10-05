#!/bin/sh

if [ ! -e /opt/SwiperProxy/swiperproxy/cert.pem ]; then
	apk add --no-cache openssl
	openssl req -x509 -newkey rsa:4096 -keyout /tmp/key.pem \
			    -out /tmp/cert.temp.pem -days 365 -nodes \
			    -subj "/C=US/ST=Oregon/L=Portland/O=Company Name/OU=Org/CN=www.example.com"
	cat /tmp/key.pem /tmp/cert.temp.pem > /opt/SwiperProxy/swiperproxy/cert.pem
fi

# TODO support any proxy.conf element use env vars with same field name with SP_ prefix?
sed -i "s/^https_certificate=.*/https_certificate=cert.pem/g" /opt/SwiperProxy/swiperproxy/proxy.conf
sed -i "s/^hostname=.*/hostname=$SP_HOSTNAME/g" /opt/SwiperProxy/swiperproxy/proxy.conf
sed -i "s/^http_port=.*/http_port=$SP_HTTP_PORT/g" /opt/SwiperProxy/swiperproxy/proxy.conf
sed -i "s/^https_port=.*/https_port=$SP_HTTPS_PORT/g" /opt/SwiperProxy/swiperproxy/proxy.conf
sed -i "s/proxy.example.org/$SP_HOSTNAME:$SP_HTTP_PORT/g" /opt/SwiperProxy/swiperproxy/htdocs/index.html

exec "$@"