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

import re
import Util

BLKSIZE = 65536

# A string without unescaped quote characters, followed by a quote.
re_scan = re.compile(r"(([^\\\"']|\\.)*)['\"]")

# A URL or hostname to rewrite.
re_url = re.compile(r"(https?:\\?/\\?/)?([a-zA-Z0-9\-\.]+\.(AC|AD|AE|AERO|AF|AG|AI|AL|AM|AN|AO|AQ|AR|ARPA|AS|ASIA|AT|AU|AW|AX|AZ|BA|BB|BD|BE|BF|BG|BH|BI|BIZ|BJ|BM|BN|BO|BR|BS|BT|BV|BW|BY|BZ|CA|CAT|CC|CD|CF|CG|CH|CI|CK|CL|CM|CN|CO|COM|COOP|CR|CU|CV|CW|CX|CY|CZ|DE|DJ|DK|DM|DO|DZ|EC|EDU|EE|EG|ER|ES|ET|EU|FI|FJ|FK|FM|FO|FR|GA|GB|GD|GE|GF|GG|GH|GI|GL|GM|GN|GOV|GP|GQ|GR|GS|GT|GU|GW|GY|HK|HM|HN|HR|HT|HU|ID|IE|IL|IM|IN|INFO|INT|IO|IQ|IR|IS|IT|JE|JM|JO|JOBS|JP|KE|KG|KH|KI|KM|KN|KP|KR|KW|KY|KZ|LA|LB|LC|LI|LK|LR|LS|LT|LU|LV|LY|MA|MC|MD|ME|MG|MH|MIL|MK|ML|MM|MN|MO|MOBI|MP|MQ|MR|MS|MT|MU|MUSEUM|MV|MW|MX|MY|MZ|NA|NAME|NC|NE|NET|NF|NG|NI|NL|NO|NP|NR|NU|NZ|OM|ORG|PA|PE|PF|PG|PH|PK|PL|PM|PN|PR|PRO|PS|PT|PW|PY|QA|RE|RO|RS|RU|RW|SA|SB|SC|SD|SE|SG|SH|SI|SJ|SK|SL|SM|SN|SO|SR|ST|SU|SV|SX|SY|SZ|TC|TD|TEL|TF|TG|TH|TJ|TK|TL|TM|TN|TO|TP|TR|TRAVEL|TT|TV|TW|TZ|UA|UG|UK|US|UY|UZ|VA|VC|VE|VG|VI|VN|VU|WF|WS|XN--0ZWM56D|XN--11B5BS3A9AJ6G|XN--3E0B707E|XN--45BRJ9C|XN--80AKHBYKNJ4F|XN--80AO21A|XN--90A3AC|XN--9T4B11YI5A|XN--CLCHC0EA0B2G2A9GCD|XN--DEBA0AD|XN--FIQS8S|XN--FIQZ9S|XN--FPCRJ9C3D|XN--FZC2C9E2C|XN--G6W251D|XN--GECRJ9C|XN--H2BRJ9C|XN--HGBK6AJ7F53BBA|XN--HLCJ6AYA9ESC7A|XN--J6W193G|XN--JXALPDLP|XN--KGBECHTV|XN--KPRW13D|XN--KPRY57D|XN--LGBBAT1AD8J|XN--MGBAAM7A8H|XN--MGBAYH7GPA|XN--MGBBH1A71E|XN--MGBC0A9AZCG|XN--MGBERP4A5D4AR|XN--O3CW4H|XN--OGBPF8FL|XN--P1AI|XN--PGBS0DH|XN--S9BRJ9C|XN--WGBH1C|XN--WGBL6A|XN--XKC2AL3HYE2A|XN--XKC2DL3A5EE0H|XN--YFRO4I67O|XN--YGBI2AMMX|XN--ZCKZAH|XXX|YE|YT|ZA|ZM|ZW))(?![a-zA-Z0-9\-\.])(:\d+)?", re.I)

class JSPage(object):
    def __init__(self, config, ssl, reader, writer, remote_host):
        self.config = config
        self.ssl = ssl
        self.reader = reader
        self.writer = writer
        self.output_buffer = []
        self.input_buffer = ""
        self.input_pos = 0
        self.eof = False
        self.output_size = 0
        self.remote_host = remote_host

    def read_some(self):
        """
        Read a block of data into the input buffer. Discard any data in
        the input buffer that has already been processed. Set the EOF
        marker if there is no more input.
        """
        if self.eof: return
        s = self.reader(BLKSIZE)
        if not s:
            self.eof = True
            return
        self.input_buffer = self.input_buffer[self.input_pos:] + s
        self.input_pos = 0

    def output(self, s):
        """
        Put a string into the output buffer. If the total length of the
        output buffer is at least BLKSIZE, write it to the output
        stream.
        """
        self.output_buffer.append(s)
        l = self.output_size
        l += len(s)
        if l >= BLKSIZE:
            self.writer("".join(self.output_buffer))
            self.output_buffer = []
            self.output_size = 0
        else:
            self.output_size = l

    def flush(self):
        """
        At the end, flush any remaining data in the output buffer.
        """
        self.writer("".join(self.output_buffer))

    def rewrite_part(self, s):
        m = re_url.match(s)
        if not m: return s

        hostname = m.group(2)
        if hostname.lower().endswith(self.config.hostname):
            return s
        scheme = m.group(1) or ''

        if self.ssl:
            port = self.config.https_port
            endpoint = self.config.https_endpoint
        else:
            port = self.config.http_port
            endpoint = self.config.http_endpoint

        if Util.using_reverseproxy(self.config):
            if scheme != (self.config.reverseproxy_scheme + '://'):
                scheme = (self.config.reverseproxy_scheme + '://')
                if scheme == 'https://':
                    port = self.config.https_port
                else:
                   port = self.config.http_port

        # Not necessary to use standard port numbers. Assume proxy is
        # not doing HTTP on 443 or HTTPS on 80.
        if port == 80 or port == 443:
            portstr = ''
        else:
            portstr = ':' + str(port)

        if scheme:
            s = "".join((scheme, self.config.hostname, portstr, endpoint,
                         hostname, s[m.end():]))
        else:
            scheme = "http://"
            s = "".join((scheme, self.config.hostname, portstr, endpoint,
                         hostname, m.group(4) or '', s[m.end():]))

        return s

    def rewrite(self):
        max_page_size = self.config.max_page_size

        # Read the first block to make sure there is some data to work
        # with.
        self.read_some()

        while True:
            s = self.input_buffer
            p = self.input_pos

            # Too much data without a quoted string match: stop and
            # flush the remainder.
            if len(s) >= max_page_size: break

            # Find the next unescaped quote character.
            m = re_scan.match(s, p)
            if not m:
                # None found. If there is more input, read another
                # chunk of data and try again.
                if self.eof: break
                self.read_some()
                continue

            # Rewrite a possible URL or hostname in the part, and
            # advance to the next position. For efficiency, the quote
            # is included in the string passed to rewrite_part, but
            # this is harmless because it will always be copied to the
            # output anyway.
            self.output(self.rewrite_part(m.group()))
            self.input_pos = m.end()

        # Write whatever is left in the input buffer, and flush the
        # output stream.
        self.output(s[p:])
        self.flush()
