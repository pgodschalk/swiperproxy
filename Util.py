#!/usr/bin/env python

# Copyright (c) 2014-2015 SwiperProxy Team
#
# Permission is hereby granted, free of charge, to any person obtaining
# a copy of this software and associated documentation files (the
# "Software"), to deal in the Software without restriction, including
# without limitation the rights to use, copy, modify, merge, publish
# distribute, sublicense and/or sell copies of the Software, and to
# permit persons to whom the Software is furnished to do so, subject
# to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS
# BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN
# ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN
# CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

import urlparse
import traceback

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
