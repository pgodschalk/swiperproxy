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

from streamhtmlparser import *
import urlparse
import Util
import re

try:
    from cStringIO import StringIO
except ImportError, e:
    from StringIO import StringIO

from JSPage import JSPage
from CSSPage import CSSPage

class Page(HtmlParser):
    BLKSIZE = 65536
    tags_and_attribs_list = [(['base', 'a', 'link', 'area'], ['href']),
                             (['audio', 'embed', 'frame', 'script', 'img',
                               'iframe', 'input', 'source'],
                              ['data-thumb', 'src', 'longdesc']),
                             (['form'], ['action']),
                             (['applet', 'object'],
                              ['codebase', 'archive', 'code']),
                             (['command'], ['icon']),
                             (['video'], ['poster', 'src']),
                             (['button'], ['formaction'])]

    simple_attriburl_regex = re.compile(r"((https?:)//[^ \r\n<]+)",
                                        re.I|re.M|re.S)
    counter = 0

    def __init__(self, config, ssl, reader, writer, remote_host):
        HtmlParser.__init__(self)
        self.config = config
        self.ssl = ssl
        self.reader = reader
        self.writer = writer
        self.input_buffer = ''
        self.output_buffer = ''
        self.state = -1
        self.tags_and_attribs = self.create_tabs_and_attribs()
        self.remote_host = remote_host

    def create_tabs_and_attribs(self):
        """
        Based on a list of tuples, create a hash-table with tagnames
        plus attribute names as keys.
        """
        h = {}
        for tags, attribs in self.tags_and_attribs_list:
            for tag in tags:
                for attrib in attribs:
                    h[tag+attrib] = True
        return h

    def rewrite_url(self, m):
        """
        Rewrite a matched URL attribute value snippet.
        """
        return Util.rewrite_URL(m.group(0), self.config, self.ssl,
                                self.remote_host)

    def rewrite(self):
        while True:
            res = self.parse_until_interesting()

            if res == False:
                # We are done.
                self.write_output(True)
                break

            # We found something interesting. Depending on what it is,
            # handle it differently. The input buffer contains any
            # non-parsed data. Continue reading and parsing until the
            # end of the attribute is found (or the maximum attribute
            # size is reached). In case of script or style tags, until
            # the end of the tag or the maximum size is reached.
            if self.state == self.HTMLPARSER_STATE_INT_CDATA_TEXT:
                self.handle_tag()
            elif self.state == self.HTMLPARSER_STATE_INT_VALUE_TEXT \
            or self.state == self.HTMLPARSER_STATE_INT_VALUE_Q_START \
            or self.state == self.HTMLPARSER_STATE_INT_VALUE_DQ_START:
                self.handle_attribute()
            else:
                pass

    def handle_tag(self):
        """
        Read and parse tag contents in blocks of the configured
        max_page_size. Rewrite them based on the tag type: script or
        style.
        """
        # Let JSPage and CSSPage handle reading this tag. The reader
        # ensures that the page is only read until the end of the tag
        # and ensures that the input buffer does not contain the
        # script or CSS data anymore. This is all handled in the
        # JSPage and CSSPage classes.
        if self.tag() == 'script':
            p = JSPage(self.config, self.ssl, self.parsing_reader,
                       self.buffered_writer, self.remote_host)
        elif self.tag() == 'style':
            p = CSSPage(self.config, self.ssl, self.parsing_reader,
                        self.buffered_writer, self.remote_host)
        p.rewrite()


    def buffered_writer(self, s):
        """
        This function writes data to the output buffer and writes the
        output buffer to the client if necessary.
        """
        self.output_buffer += s
        self.write_output(False)

    def parsing_reader(self, BLKSIZE):
        """
        This function is used to read a block of data from the server
        response and parse it until the end of the response or tag
        close. This function is used for the JSPage and CSSPage classes
        as reader and should not update the input buffer of the Page
        instance with data within <script> and <style> tags.
        """

        # Previously we already read until the end tag, so return
        # nothing.
        if self.state == self.HTMLPARSER_STATE_INT_TEXT:
            return None

        # We are already at the end of the input buffer and there's
        # nothing more. Empty the input buffer and return.
        if self.reached_end():
            self.input_buffer = ''
            return None
        if len(self.input_buffer) > 0:
            s = self.input_buffer

        if not s:
            s = self.reader(BLKSIZE)
            if not s or len(s) == 0:
                return None

        self.state = self.parse_until(s, [self.HTMLPARSER_STATE_INT_TEXT])
        if self.state == self.STATEMACHINE_ERROR:
            self.reset()

        # Found end tag, add everything starting at the end tag to the
        # input buffer as this will not be handled by JSPage or
        # CSSPage.
        if self.state == self.HTMLPARSER_STATE_INT_TEXT:
            self.input_buffer = s[self.get_position():]

        return s[:self.get_position()]

    def handle_attribute(self):
        # The max_page_size is set to 5MB by default. If an attribute
        # is larger than this.. well, too bad.
        attr = self.attr()
        self.keep_reading(self.config.max_page_size,
                          [self.HTMLPARSER_STATE_INT_ATTR_SPACE,
                           self.HTMLPARSER_STATE_INT_TAG_CLOSE,
                           self.HTMLPARSER_STATE_INT_TAG_SPACE])

        pos = self.get_position()-1

        if attr == 'style':
            # CSSPage needs read and write functions. Simulate this by
            # using StringIO on the already read value.
            f = StringIO(self.input_buffer[:pos])
            outf = StringIO()
            p = CSSPage(self.config, self.ssl, f.read, outf.write,
                        self.remote_host)
            p.rewrite()
            outf.seek(0)
            self.output_buffer += outf.read()
            self.write_output(False)
            self.input_buffer = self.input_buffer[pos:]
            return
        elif attr.startswith("on"):
            # JSPage needs read and write functions. Simulate this by
            # using StringIO on the already read value.
            f = StringIO(self.input_buffer[:pos])
            outf = StringIO()
            p = JSPage(self.config, self.ssl, f.read, outf.write,
                       self.remote_host)
            p.rewrite()
            outf.seek(0)
            self.output_buffer += outf.read() + self.input_buffer[pos]
            self.write_output(False)
            self.input_buffer = self.input_buffer[pos+1:]
            return
        elif self.tag() == 'meta' and attr == 'content':
            val = re.sub(self.simple_attriburl_regex, self.rewrite_url,
                         self.input_buffer[:pos])
            self.output_buffer += val
            self.write_output(False)
            self.input_buffer = self.input_buffer[pos:]
            return

        # Other URL-containing attributes.
        val = Util.rewrite_URL(self.input_buffer[:pos], self.config, self.ssl,
                               self.remote_host)
        self.output_buffer += val
        self.write_output(False)
        self.input_buffer = self.input_buffer[pos:]

    def keep_reading(self, max_size, states):
        """
        Keep reading from the input stream in blocks until one of the
        requested states is reached or the maximum size is passed. Fill
        the input buffer with the data and return. Do not write data to
        the output buffer because this data is going to be rewritten.
        The first time in the loop, use the current input buffer and do
        not read any data yet.
        """
        length = len(self.input_buffer)
        first_time = True
        while length < max_size:

            if not first_time:
                s = self.reader(self.BLKSIZE)

                if s and len(s) > 0:
                    length += len(s)
                    self.input_buffer += s
            else:
                s = self.input_buffer
                first_time = False

            self.state = self.parse_until(s, states)

            if self.state == self.STATEMACHINE_ERROR:
                self.reset()

            if self.state in states:
                break

            if not s or len(s) == 0:
                break

    def parse_until_interesting(self):
        while True:
            s = self.input_buffer

            if not s or len(s) == 0:
                s = self.reader(self.BLKSIZE)
                if not s or len(s) == 0:
                    self.write_output(True)
                    return False

            self.state = self.parse_until_rewritable(s)

            if self.state != -1:
                self.counter += 1
                self.output_buffer += s[:self.get_position()]
                self.input_buffer = s[self.get_position():]
                self.write_output(False)
                return True

            # Nothing interesting so far, write everything to the
            # client and continue with next block.
            self.output_buffer += s
            self.input_buffer = ''
            self.write_output(False)

    def write_output(self, final):
        """
        Write output buffer in BLKSIZE blocks to the client. If final
        is set, write everything, including the last block even if it 
        is smaller than BLKSIZE. Remove written blocks from the output
        buffer.
        """
        length = len(self.output_buffer)
        for beg in range(0, length, self.BLKSIZE):
            end = beg + self.BLKSIZE
            if end > length:
                if not final:
                    self.output_buffer = self.output_buffer[beg:]
                    return
                end = length
            self.writer(self.output_buffer[beg:end])

        self.output_buffer = ''

    def is_url_attribute(self, this_tag, this_attrib):
        """
        Returns True if the attribute in the tag should contain a URL.
        """
        return self.tags_and_attribs.get(this_tag + this_attrib) or False
