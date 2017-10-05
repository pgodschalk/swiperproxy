Docker image for swiperproxy

### Building

Run `build.sh`

### Usage

You need to specify some environment settings in order for the container to work properly, namely:

* SP_HOSTNAME - `hostname` in `proxy.conf`
* SP_HTTP_PORT - `http_port` in `proxy.conf`
* SP_HTTPS_PORT= `https_port` in `proxy.conf`

Example:

```
docker run -e SP_HOST=proxy.example.org -e SP_HTTP_PORT=80 -e SP_HTTPS_PORT=443 -p80:8080 -p443:40443 swiperproxy/swiperproxy
```

A self-signed certificate will be generated when the container starts. If you want to use your own, just map it (make sure it contains both private key and certificate as described in documentation):

```
docker run (...) -v /path/to/certificate.pem:/opt/SwiperProxy/swiperproxy/cert.pem swiperproxy/swiperproxy
```

You can also mount logs directory to persist them or your own `htdocs` to use instead such as:

```
docker run (...) -v /path/to/htdocs:/opt/SwiperProxy/swiperproxy/htdocs -v /path/to/logs:/var/log/swiperproxy/ swiperproxy/swiperproxy
```