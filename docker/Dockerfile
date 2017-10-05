FROM python:2.7.14-alpine as builder

RUN apk add --no-cache build-base linux-headers python-dev file
RUN pip install cython==0.27.1

RUN mkdir -p /opt/SwiperProxy

COPY . /opt/SwiperProxy/swiperproxy

WORKDIR /opt/SwiperProxy/swiperproxy/include/streamhtmlparser
RUN ./configure && make && make install

WORKDIR /opt/SwiperProxy/swiperproxy/include/streamhtmlparser/src/py-streamhtmlparser
RUN make && make install


FROM python:2.7.14-alpine

RUN pip install ipy==0.83
RUN mkdir -p /var/log/swiperproxy/
COPY --from=builder /opt/SwiperProxy/swiperproxy /opt/SwiperProxy/swiperproxy
COPY --from=builder /usr/local/lib/python2.7/site-packages/streamhtmlparser.so /usr/local/lib/python2.7/site-packages/
COPY --from=builder /usr/local/lib/libstreamhtmlparser.so.0 /usr/local/lib/

COPY docker/entrypoint.sh /entrypoint.sh
EXPOSE 8080
EXPOSE 40443
WORKDIR /opt/SwiperProxy/swiperproxy
ENTRYPOINT ["/entrypoint.sh"]
CMD ["./Proxy.py", "-c", "proxy.conf"]
