#!/usr/bin/env python

import urlparse
import traceback

def remove_PATH_endpoint(path, config):
    if path.startswith(config.https_endpoint):
        lens = len(config.https_endpoint)
        if lens:
            path = path[lens-1:]
    if path.startswith(config.http_endpoint):
        lens = len(config.http_endpoint)
        if lens:
            path = path[lens-1:]
    return path

def rewrite_URL_strip(url, config):
    """
    Strip the proxy hostname part of the passed URL.
    """
    try:
        res = urlparse.urlsplit(url)

        if res[1]:
           newres = [ item for item in res ]
           host = res[1].split(":")[0]
           if host.endswith(config.hostname):
               host = host.split(config.hostname)[0]
           newres[1] = host

           newres[2] = remove_PATH_endpoint(res[2], config)

           url = urlparse.urlunsplit(newres)
    except Exception, e:
        pass
    return url

def rewrite_URL(url, config, ssl, remote_host):
    """
    Rewrite the URL and add the proxy's HTTP or HTTPS ports when
    necessary. For absolute URLs without scheme, use the same scheme as
    used to access the proxy (using the 'ssl' flag).
    """
    try:
        # Strip our own hostname for the rewrites to work.
        url = rewrite_URL_strip(url,config)
        res = urlparse.urlsplit(url)
        need_rewrite = False

        # Handle rewrites.
        for (f, t) in config.rewrites:
            if res[1] and res[1].split(":")[0].lower() == f.lower() \
            and (res[0] == '' or res[0] == 'http' or res[0] == 'https'):
                newres = [ item for item in res ]
                host = t

                # No scheme, use the scheme used to access proxy.
                if res[0] == '': # res[0] == scheme
                    if ssl:
                        newres[0]='https'
                    else:
                        newres[0]='http'

                # Add port of proxy.
                if newres[0] == 'http':
                    port = config.http_port
                elif newres[0] == 'https':
                    port = config.https_port

                newres[1] = host + ":" + str(port)
                url = urlparse.urlunsplit(newres)
                return url

        # Handle absolute HTTP or HTTPS URL.
        newres = [ item for item in res ]
        host = res[1].split(":")[0]

        # No scheme, use the scheme used to access proxy.
        if res[0] == '': # res[0] == scheme
            if ssl:
                newres[0]='https'
            else:
                newres[0]='http'

        # Add the endpoint from URL scheme.
        if newres[0] == 'http':
            endpoint = config.http_endpoint
        elif newres[0] == 'https':
            endpoint = config.https_endpoint

        # Change scheme and port if using a reverse proxy and if scheme
        # is different
        if using_reverseproxy(config):
            if newres[0] != config.reverseproxy_scheme:
                newres[0] = config.reverseproxy_scheme

        # Add port of proxy.
        if newres[0] == 'http':
            port = config.http_port
        elif newres[0] == 'https':
            port = config.https_port

        newres[1] = config.hostname + ":" + str(port)
        if host == '':
            host = remote_host
        if str(newres[2]).startswith("/"):
            newres[2] = endpoint + host + newres[2]
        else:
            newres[2] = endpoint + host + "/" + newres[2]
        url = urlparse.urlunsplit(newres)
    except Exception, e:
        pass
    return url

def using_reverseproxy(config):
        """
        Returns True if we are using a reverse proxy
        (config.http_endpoint != config.https_endpoint), False
        otherwise.
        """
        return not (config.http_endpoint == config.https_endpoint)
