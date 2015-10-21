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

cimport streamhtmlparser
from libc.stdlib cimport malloc, free

cdef class HtmlParser:
    """
    Cython based Python wrapper around streamhtmlparser.
    """
    cdef streamhtmlparser.htmlparser_ctx *parser

    STATEMACHINE_ERROR = streamhtmlparser.STATEMACHINE_ERROR
    HTMLPARSER_STATE_INT_TEXT = streamhtmlparser.HTMLPARSER_STATE_INT_TEXT
    HTMLPARSER_STATE_INT_TAG_START = streamhtmlparser.HTMLPARSER_STATE_INT_TAG_START
    HTMLPARSER_STATE_INT_TAG_NAME = streamhtmlparser.HTMLPARSER_STATE_INT_TAG_NAME
    HTMLPARSER_STATE_INT_DECLARATION_START = streamhtmlparser.HTMLPARSER_STATE_INT_DECLARATION_START
    HTMLPARSER_STATE_INT_DECLARATION_BODY = streamhtmlparser.HTMLPARSER_STATE_INT_DECLARATION_BODY
    HTMLPARSER_STATE_INT_COMMENT_OPEN = streamhtmlparser.HTMLPARSER_STATE_INT_COMMENT_OPEN
    HTMLPARSER_STATE_INT_COMMENT_BODY = streamhtmlparser.HTMLPARSER_STATE_INT_COMMENT_BODY
    HTMLPARSER_STATE_INT_COMMENT_DASH = streamhtmlparser.HTMLPARSER_STATE_INT_COMMENT_DASH
    HTMLPARSER_STATE_INT_COMMENT_DASH_DASH = streamhtmlparser.HTMLPARSER_STATE_INT_COMMENT_DASH_DASH
    HTMLPARSER_STATE_INT_PI = streamhtmlparser.HTMLPARSER_STATE_INT_PI
    HTMLPARSER_STATE_INT_PI_MAY_END = streamhtmlparser.HTMLPARSER_STATE_INT_PI_MAY_END
    HTMLPARSER_STATE_INT_TAG_SPACE = streamhtmlparser.HTMLPARSER_STATE_INT_TAG_SPACE
    HTMLPARSER_STATE_INT_TAG_CLOSE = streamhtmlparser.HTMLPARSER_STATE_INT_TAG_CLOSE
    HTMLPARSER_STATE_INT_ATTR = streamhtmlparser.HTMLPARSER_STATE_INT_ATTR
    HTMLPARSER_STATE_INT_ATTR_SPACE = streamhtmlparser.HTMLPARSER_STATE_INT_ATTR_SPACE
    HTMLPARSER_STATE_INT_VALUE = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE
    HTMLPARSER_STATE_INT_VALUE_TEXT = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE_TEXT
    HTMLPARSER_STATE_INT_VALUE_Q_START = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE_Q_START
    HTMLPARSER_STATE_INT_VALUE_Q = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE_Q
    HTMLPARSER_STATE_INT_VALUE_DQ_START = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE_DQ_START
    HTMLPARSER_STATE_INT_VALUE_DQ = streamhtmlparser.HTMLPARSER_STATE_INT_VALUE_DQ
    HTMLPARSER_STATE_INT_CDATA_COMMENT_START = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_COMMENT_START
    HTMLPARSER_STATE_INT_CDATA_COMMENT_START_DASH = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_COMMENT_START_DASH
    HTMLPARSER_STATE_INT_CDATA_COMMENT_BODY = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_COMMENT_BODY
    HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH
    HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH_DASH = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH_DASH
    HTMLPARSER_STATE_INT_CDATA_TEXT = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_TEXT
    HTMLPARSER_STATE_INT_CDATA_LT = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_LT
    HTMLPARSER_STATE_INT_CDATA_MAY_CLOSE = streamhtmlparser.HTMLPARSER_STATE_INT_CDATA_MAY_CLOSE
    HTMLPARSER_STATE_INT_JS_FILE = streamhtmlparser.HTMLPARSER_STATE_INT_JS_FILE
    HTMLPARSER_STATE_INT_CSS_FILE = streamhtmlparser.HTMLPARSER_STATE_INT_CSS_FILE
    HTMLPARSER_STATE_INT_NULL = streamhtmlparser.HTMLPARSER_STATE_INT_NULL

    def __cinit__(self):
        self.parser = streamhtmlparser.htmlparser_new()

    def __dealloc__(self):
        streamhtmlparser.htmlparser_delete(self.parser)

    def reset(self):
        streamhtmlparser.htmlparser_reset(self.parser)

    def reset_mode(self, mode):
        streamhtmlparser.htmlparser_reset_mode(self.parser, mode)

    def state(self):
        return streamhtmlparser.htmlparser_state(self.parser)

    def parse(self, s):
        return streamhtmlparser.htmlparser_parse(self.parser, s, len(s))

    def parse_until_rewritable(self, s):
        return streamhtmlparser.htmlparser_parse_until_rewritable(self.parser,
																  s, len(s))

    def parse_until(self, s, states):
        cdef int *c_states
        cdef int retval
        cdef int old_position

        # Copy the passed states list to an integer array, terminated with -1
        c_states = <int *>malloc((len(states)+1) * sizeof(int))

        if not c_states:
            raise MemoryError()
    
        for i in range(len(states)):
            c_states[i] = states[i]
        c_states[i + 1] = -1

        retval = streamhtmlparser.htmlparser_parse_until(self.parser, s, len(s),
														 c_states)
        free(c_states)
        return retval

    def parse_until_statechange(self, s, states):
        cdef int *c_states
        cdef int retval
        cdef int old_position

        # Copy the passed states list to an integer array, terminated with -1
        c_states = <int *>malloc((len(states)+1) * sizeof(int) * 2)

        if not c_states:
            raise MemoryError()
    
        for i in range(len(states)):
            c_states[i * 2] = states[i][0]
            c_states[i * 2 + 1] = states[i][1]

        c_states[i * 2 + 2] = -1

        retval=streamhtmlparser.htmlparser_parse_until_statechange(self.parser,
																   s, len(s),
																   c_states)
        free(c_states)
        return retval

    def is_attr_quoted(self):
        return bool(streamhtmlparser.htmlparser_is_attr_quoted(self.parser))

    def in_js(self):
        return bool(streamhtmlparser.htmlparser_in_js(self.parser))

    def tag(self):
        cdef char *t
        t = streamhtmlparser.htmlparser_tag(self.parser)
        if t == NULL:
            return None
        return t 

    def attr(self):
        cdef char *a
        a = streamhtmlparser.htmlparser_attr(self.parser)
        if a == NULL:
            return None
        return a

    def value(self):
        cdef char *v
        v = streamhtmlparser.htmlparser_value(self.parser)
        if v == NULL:
            return None
        return v

    def in_css(self):
        return bool(streamhtmlparser.htmlparser_in_css(self.parser))

    def js_state(self):
        return streamhtmlparser.htmlparser_js_state(self.parser)

    def is_js_quoted(self):
        return bool(streamhtmlparser.htmlparser_is_js_quoted(self.parser))

    def value_index(self):
        return streamhtmlparser.htmlparser_value_index(self.parser)

    def is_url_start(self):
        return bool(streamhtmlparser.htmlparser_is_url_start(self.parser))

    def attr_type(self):
        return streamhtmlparser.htmlparser_attr_type(self.parser)

    def get_line_number(self):
        return streamhtmlparser.htmlparser_get_line_number(self.parser)

    def set_line_number(self, int line):
        streamhtmlparser.htmlparser_set_line_number(self.parser, line)

    def get_column_number(self):
        return streamhtmlparser.htmlparser_get_column_number(self.parser)

    def get_position(self):
        return self.parser.statemachine.position

    def reached_end(self):
        return bool(self.parser.statemachine.reached_end)

    def get_error_msg(self):
        cdef char *m
        m = streamhtmlparser.htmlparser_get_error_msg(self.parser)
        if m == NULL:
            return None
        return m

    def insert_text(self):
        return streamhtmlparser.htmlparser_insert_text(self.parser)

