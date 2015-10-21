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

# Generated using:
#
# h2xml -I.. -I/usr/include streamhtmlparser/htmlparser.h -o \
#     htmlparser.xml
# xml2cython.py -l htmlparser htmlparser.h htmlparser.xml > \
#     ../py-streamhtmlparser/streamhtmlparser.pxd
#
# Manual fixes of constant sized char arrays in structures and forward
# struct definitions.

cdef extern from "../streamhtmlparser/htmlparser.h":
	cdef enum:
		STATEMACHINE_ERROR = 127
		HTMLPARSER_MAX_ENTITY_SIZE = 10
		HTMLPARSER_MAX_STRING = 1024
		STATEMACHINE_MAX_STR_ERROR = 80
		STATEMACHINE_RECORD_BUFFER_SIZE = 1024
		JSPARSER_RING_BUFFER_SIZE = 18

	cdef struct entityfilter_ctx_s:
		int buffer_pos
		int in_entity
		char buffer[HTMLPARSER_MAX_ENTITY_SIZE]
		char output[HTMLPARSER_MAX_ENTITY_SIZE]
	ctypedef entityfilter_ctx_s entityfilter_ctx
	void entityfilter_copy(entityfilter_ctx *, entityfilter_ctx *)

	cdef struct statemachine_ctx_s
	ctypedef void(*state_event_function)(statemachine_ctx_s *, int, char, int)
	cdef struct statemachine_definition_s:
		int num_states
		int * * transition_table
		char * * state_names
		state_event_function * in_state_events
		state_event_function * enter_state_events
		state_event_function * exit_state_events
	ctypedef statemachine_definition_s statemachine_definition
	ctypedef long unsigned int size_t
	cdef struct statemachine_ctx_s:
		int current_state
		int next_state
		statemachine_definition * definition
		char current_char
		int line_number
		int column_number
		char record_buffer[STATEMACHINE_RECORD_BUFFER_SIZE]
		size_t record_pos
		size_t position
		int reached_end
		int recording
		char error_msg[STATEMACHINE_MAX_STR_ERROR]
		void * user
	ctypedef statemachine_ctx_s statemachine_ctx
	cdef struct jsparser_ctx_s:
		statemachine_ctx * statemachine
		statemachine_definition * statemachine_def
		int buffer_start
		int buffer_end
		char buffer[JSPARSER_RING_BUFFER_SIZE]
	ctypedef jsparser_ctx_s jsparser_ctx
	cdef struct htmlparser_ctx_s:
		statemachine_ctx * statemachine
		statemachine_definition * statemachine_def
		jsparser_ctx * jsparser
		entityfilter_ctx * entityfilter
		int value_index
		int in_js
		char tag[HTMLPARSER_MAX_STRING]
		char attr[HTMLPARSER_MAX_STRING]
		char value[HTMLPARSER_MAX_STRING]
	ctypedef htmlparser_ctx_s htmlparser_ctx
	void htmlparser_copy(htmlparser_ctx *, htmlparser_ctx *)
	void jsparser_delete(jsparser_ctx *)
	void htmlparser_set_column_number(htmlparser_ctx *, int)
	int jsparser_buffer_last_identifier(jsparser_ctx *, char *)
	char * statemachine_stop_record(statemachine_ctx *)
	int htmlparser_is_js_quoted(htmlparser_ctx *)
	int statemachine_get_state(statemachine_ctx *)
	int htmlparser_insert_text(htmlparser_ctx *)
	void htmlparser_set_line_number(htmlparser_ctx *, int)
	int statemachine_get_line_number(statemachine_ctx *)
	void jsparser_copy(jsparser_ctx *, jsparser_ctx *)
	int htmlparser_get_column_number(htmlparser_ctx *)
	char * entityfilter_process(entityfilter_ctx *, char)
	void jsparser_buffer_append_str(jsparser_ctx *, char *)
	void statemachine_enter_state(statemachine_definition *, int, state_event_function)
	void statemachine_reset(statemachine_ctx *)
	statemachine_ctx * statemachine_duplicate(statemachine_ctx *, statemachine_definition *, void *)
	int jsparser_buffer_set(jsparser_ctx *, int, char)
	char * htmlparser_get_error_msg(htmlparser_ctx *)
	void htmlparser_delete(htmlparser_ctx *)
	int statemachine_parse(statemachine_ctx *, char *, int)
	void statemachine_delete(statemachine_ctx *)
	jsparser_ctx * jsparser_new()
	int htmlparser_get_line_number(htmlparser_ctx *)
	void statemachine_definition_delete(statemachine_definition *)
	int htmlparser_in_css(htmlparser_ctx *)
	int htmlparser_is_attr_quoted(htmlparser_ctx *)
	char jsparser_buffer_pop(jsparser_ctx *)
	int htmlparser_is_url_start(htmlparser_ctx *)
	void jsparser_buffer_slice(jsparser_ctx *, char *, int, int)
	entityfilter_ctx * entityfilter_new()
	int htmlparser_value_index(htmlparser_ctx *)
	void statemachine_start_record(statemachine_ctx *)
	void statemachine_definition_populate(statemachine_definition *, int * *, char * *)
	void entityfilter_delete(entityfilter_ctx *)
	int statemachine_get_column_number(statemachine_ctx *)
	char jsparser_buffer_get(jsparser_ctx *, int)
	char * statemachine_get_error_msg(statemachine_ctx *)
	htmlparser_ctx * htmlparser_new()
	int jsparser_state(jsparser_ctx *)
	int htmlparser_state(htmlparser_ctx *)
	void statemachine_encode_char(char, char *, size_t)
	void statemachine_set_state(statemachine_ctx *, int)
	void statemachine_exit_state(statemachine_definition *, int, state_event_function)
	char * statemachine_record_buffer(statemachine_ctx *)
	int htmlparser_parse(htmlparser_ctx *, char *, int)
	int htmlparser_parse_until_rewritable(htmlparser_ctx *, char *, int)
	int htmlparser_parse_until(htmlparser_ctx *, char *, int, int *)
	int htmlparser_parse_until_statechange(htmlparser_ctx *, char *, int, int *)
	void jsparser_buffer_append_chr(jsparser_ctx *, char)
	char * htmlparser_attr(htmlparser_ctx *)
	void htmlparser_reset(htmlparser_ctx *)
	void jsparser_reset(jsparser_ctx *)
	void statemachine_copy(statemachine_ctx *, statemachine_ctx *, statemachine_definition *, void *)
	statemachine_ctx * statemachine_new(statemachine_definition *, void *)
	int htmlparser_in_js(htmlparser_ctx *)
	int htmlparser_attr_type(htmlparser_ctx *)
	void statemachine_set_line_number(statemachine_ctx *, int)
	statemachine_definition * statemachine_definition_new(int)
	void statemachine_set_column_number(statemachine_ctx *, int)
	void statemachine_in_state(statemachine_definition *, int, state_event_function)
	jsparser_ctx * jsparser_duplicate(jsparser_ctx *)
	void htmlparser_reset_mode(htmlparser_ctx *, int)
	size_t statemachine_record_length(statemachine_ctx *)
	void entityfilter_reset(entityfilter_ctx *)
	char * htmlparser_tag(htmlparser_ctx *)
	int jsparser_parse(jsparser_ctx *, char *, int)
	char * htmlparser_value(htmlparser_ctx *)
	int htmlparser_js_state(htmlparser_ctx *)

cdef extern from "../htmlparser_fsm.h":
	cdef enum htmlparser_state_internal_enum:
		HTMLPARSER_DUMMY
		HTMLPARSER_STATE_INT_TEXT
		HTMLPARSER_STATE_INT_TAG_START
		HTMLPARSER_STATE_INT_TAG_NAME
		HTMLPARSER_STATE_INT_DECLARATION_START
		HTMLPARSER_STATE_INT_DECLARATION_BODY
		HTMLPARSER_STATE_INT_COMMENT_OPEN
		HTMLPARSER_STATE_INT_COMMENT_BODY
		HTMLPARSER_STATE_INT_COMMENT_DASH
		HTMLPARSER_STATE_INT_COMMENT_DASH_DASH
		HTMLPARSER_STATE_INT_PI
		HTMLPARSER_STATE_INT_PI_MAY_END
		HTMLPARSER_STATE_INT_TAG_SPACE
		HTMLPARSER_STATE_INT_TAG_CLOSE
		HTMLPARSER_STATE_INT_ATTR
		HTMLPARSER_STATE_INT_ATTR_SPACE
		HTMLPARSER_STATE_INT_VALUE
		HTMLPARSER_STATE_INT_VALUE_TEXT
		HTMLPARSER_STATE_INT_VALUE_Q_START
		HTMLPARSER_STATE_INT_VALUE_Q
		HTMLPARSER_STATE_INT_VALUE_DQ_START
		HTMLPARSER_STATE_INT_VALUE_DQ
		HTMLPARSER_STATE_INT_CDATA_COMMENT_START
		HTMLPARSER_STATE_INT_CDATA_COMMENT_START_DASH
		HTMLPARSER_STATE_INT_CDATA_COMMENT_BODY
		HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH
		HTMLPARSER_STATE_INT_CDATA_COMMENT_DASH_DASH
		HTMLPARSER_STATE_INT_CDATA_TEXT
		HTMLPARSER_STATE_INT_CDATA_LT
		HTMLPARSER_STATE_INT_CDATA_MAY_CLOSE
		HTMLPARSER_STATE_INT_JS_FILE
		HTMLPARSER_STATE_INT_CSS_FILE
		HTMLPARSER_STATE_INT_NULL
