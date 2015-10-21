#!/usr/bin/env python
#
# Copyright (c) 2008, Google Inc.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
# notice, this list of conditions and the following disclaimer.
#     * Redistributions in binary form must reproduce the above
# copyright notice, this list of conditions and the following disclaimer
# in the documentation and/or other materials provided with the
# distribution.
#     * Neither the name of Google Inc. nor the names of its
# contributors may be used to endorse or promote products derived from
# this software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
# ---
# Author: mjwiacek@google.com (Mike Wiacek)

import os

import py_streamhtmlparser
import unittest

PARSER_MODE_MAP = {
  'html': py_streamhtmlparser.MODE_HTML,
  'js': py_streamhtmlparser.MODE_JS,
  'css': py_streamhtmlparser.MODE_CSS,
  'html_in_tag': py_streamhtmlparser.MODE_HTML_IN_TAG
}

ATTRIBUTE_TYPE_MAP = {
  'none': py_streamhtmlparser.ATTR_NONE,
  'regular': py_streamhtmlparser.ATTR_REGULAR,
  'uri': py_streamhtmlparser.ATTR_URI,
  'js': py_streamhtmlparser.ATTR_JS,
  'style': py_streamhtmlparser.ATTR_STYLE
}

JAVASCRIPT_STATE_MAP = {
  'text': py_streamhtmlparser.JS_STATE_TEXT,
  'q': py_streamhtmlparser.JS_STATE_Q,
  'dq': py_streamhtmlparser.JS_STATE_DQ,
  'regexp': py_streamhtmlparser.JS_STATE_REGEXP,
  'comment': py_streamhtmlparser.JS_STATE_COMMENT
}

HTML_STATE_MAP = {
  'text': py_streamhtmlparser.HTML_STATE_TEXT,
  'tag': py_streamhtmlparser.HTML_STATE_TAG,
  'attr': py_streamhtmlparser.HTML_STATE_ATTR,
  'value': py_streamhtmlparser.HTML_STATE_VALUE,
  'comment': py_streamhtmlparser.HTML_STATE_COMMENT,
  'js_file': py_streamhtmlparser.HTML_STATE_JS_FILE,
  'css_file': py_streamhtmlparser.HTML_STATE_CSS_FILE,
}

class PyHtmlParserUnitTest(unittest.TestCase):

  def setUp(self):
    self.parser = py_streamhtmlparser.HtmlParser()
    self.test_data_path = os.environ.get('TESTDATA_PATH',
                                         'src/tests/testdata/')
    self.test_path = os.path.join(self.test_data_path, 'regtest/')
    self.current_chunk = ""
    self.context_map = {}

  def LookupParserMode(self, value):
    if value in PARSER_MODE_MAP:
      return PARSER_MODE_MAP[value]
    else:
      self.fail("Unknown mode type in reset_mode directive")

  def LookupHtmlParserState(self, value):
    if value in HTML_STATE_MAP:
      return HTML_STATE_MAP[value]
    else:
      self.fail("Unable to lookup parser state by directive value")

  def LookupAttributeType(self, value):
    if value in ATTRIBUTE_TYPE_MAP:
      return ATTRIBUTE_TYPE_MAP[value]
    else:
      self.fail("Unable to lookup attribute type")

  def LookupJavaScriptParserState(self, value):
    if value in JAVASCRIPT_STATE_MAP:
      return JAVASCRIPT_STATE_MAP[value]
    else:
      self.fail("Unable to lookup javascript parser state by directive value")

  def ValidateState(self, value):
    state = self.LookupHtmlParserState(value)
    self.assertEqual(state, self.parser.State(), "Unexpected state!")

  def ValidateTag(self, value):
    tag = self.parser.Tag()
    self.assertNotEqual(tag, None, "Tag expected!")
    self.assertEqual(tag.lower(), value.lower())

  def ValidateAttribute(self, value):
    attribute = self.parser.Attribute()
    self.assertNotEqual(attribute, None, "Attribute expected!")
    self.assertEqual(attribute.lower(), value.lower())

  def ValidateValue(self, value):
    parser_value = self.parser.Value()
    self.assertNotEqual(parser_value, None, "Value expected!")
    self.assertEqual(value.lower(), parser_value.lower())

  def ValidateAttributeType(self, value):
    attr_type = self.LookupAttributeType(value)
    self.assertEqual(self.parser.AttributeType(), attr_type, 
                     "Unexpected attribute type!")

  def ValidateAttributeQuoted(self, value):
    if value.lower() == "true":
      self.assert_(self.parser.IsAttributeQuoted(),
                   "Attribute should be quoted")
    else:
      self.failIf(self.parser.IsAttributeQuoted(),
                  "Attribute should not be quoted")

  def ValidateInJavaScript(self, value):
    if value.lower() == "true":
      self.assert_(self.parser.InJavaScript(),
                   "Should be in JavaScript context")
    else:
      self.failIf(self.parser.InJavaScript(),
                  "Should not be in JavaScript context")

  def ValidateIsJavaScriptQuoted(self, value):
    if value.lower() == "true":
      self.assert_(self.parser.IsJavaScriptQuoted(),
                  "Unexpected unquoted JavaScript literal")
    else:
      self.failIf(self.parser.IsJavaScriptQuoted(),
                  "Expected a quoted JavaScript literal")

  def ValidateJavaScriptState(self, value):
    state = self.LookupJavaScriptParserState(value)
    self.assertEqual(state, self.parser.JavaScriptState(), 
                    "Unexpected JavaScript Parser state")

  def ValidateInCss(self, value):
    if value.lower() == "true":
      self.assert_(self.parser.InCss(),
                   "Should be in CSS context")
    else:
      self.failIf(self.parser.InCss(),
                  "Should not be in CSS context")

  def ValidateLine(self, value):
    self.assertEqual(int(value), self.parser.GetLineNumber(),
                    "Unexpected Line count")

  def ValidateColumn(self, value):
    self.assertEqual(int(value), self.parser.GetColumnNumber(),
                    "Unexpected Column count")

  def ValidateValueIndex(self, value):
    self.assertEqual(int(value), self.parser.ValueIndex(),
                     "Unexpected value index!")

  def ValidateIsUrlStart(self, value):
    if value.lower() == "true":
      self.assert_(self.parser.IsUrlStart(),
                   "IsUrlStart should be true.")
    else:
      self.failIf(self.parser.IsUrlStart(),
                  "IsUrlStart should be false.")

  def processAnnotation(self, annotation):
    annotation = annotation.replace("<?state", "").replace("?>", "") 
    annotation = annotation.replace("\n", "").strip()
    pairs = [x.strip() for x in annotation.split(",")]
    for pair in pairs:
      if not pair:
        continue
      (first, second) = pair.lower().split("=")
      if first == "state":
        self.ValidateState(second)
      elif first == "tag":
        self.ValidateTag(second)
      elif first == "attr":
        self.ValidateAttribute(second)
      elif first == "value":
        self.ValidateValue(second)
      elif first == "attr_type":
        self.ValidateAttributeType(second)
      elif first == "attr_quoted":
        self.ValidateAttributeQuoted(second)
      elif first == "in_js":
        self.ValidateInJavaScript(second)
      elif first == "js_quoted":
        self.ValidateIsJavaScriptQuoted(second)
      elif first == "js_state":
        self.ValidateJavaScriptState(second)
      elif first == "in_css":
        self.ValidateInCss(second)
      elif first == "line_number":
        self.ValidateLine(second)
      elif first == "column_number":
        self.ValidateColumn(second)
      elif first == "value_index":
        self.ValidateValueIndex(second)
      elif first == "is_url_start":
        self.ValidateIsUrlStart(second)
      elif first == "save_context":
        copy = py_streamhtmlparser.HtmlParser()
        copy.CopyFrom(self.parser)
        self.context_map[second] = copy
      elif first == "load_context":
        self.parser.CopyFrom(self.context_map[second])
      elif first == "reset":
        if second == "true":
          self.parser.Reset()
      elif first == "reset_mode":
        self.parser.ResetMode(self.LookupParserMode(second))
      elif first == "insert_text":
        if second == "true":
          self.parser.InsertText()
      else:
        self.fail("Unknown test directive!")

  def ValidateFile(self, filename):
    directive_start = "<?state"
    directive_end = "?>"

    # Reset current parser
    self.parser.Reset()

    file_handle = open(self.test_path + filename, "r")
    data = file_handle.read()
    current_index = 0

    while current_index < len(data):
      start_index = data.find(directive_start, current_index)
      stop_index = data.find(directive_end, start_index) + len(directive_end)

      # Parse all text until the first directive
      if current_index > 0 and start_index < 0:
        self.parser.Parse(data[current_index:]) # No more annotations left
        self.current_chunk = data[current_index:]
        current_index += len(data[current_index:])
      else:
        self.parser.Parse(data[current_index:start_index])
        self.current_chunk = data[current_index:start_index]
        current_index += len(data[current_index:start_index])

      # Pull out the current annotation
      annotation = data[start_index:stop_index]
      self.current_chunk = annotation
      self.processAnnotation(annotation)

      # Update line count
      self.parser.SetLineNumber(self.parser.GetLineNumber() +
                                annotation.count('\n'))

      # Update column count
      last_newline = annotation.rfind('\n')
      # If there isn't a newline in the annotation we simple add the size of
      # the annontation to the current column number.
      if last_newline == -1:
        self.parser.SetColumnNumber(self.parser.GetColumnNumber() +
                                    len(annotation))
      # if there is a newline, we consider the column count to be the number of
      # characters after the newline.
      else:
        self.parser.SetColumnNumber(len(annotation) -
                                    last_newline)

      current_index += len(annotation)

    return

  def testSimple(self):
    self.ValidateFile("simple.html")

  def testComments(self):
    self.ValidateFile("comments.html")

  def testJavaScriptBlock(self):
    self.ValidateFile("javascript_block.html")

  def testJavaScriptAttributes(self):
    self.ValidateFile("javascript_attribute.html")

  def testJavaScriptRegExp(self):
    self.ValidateFile("javascript_regexp.html")

  def testTags(self):
    self.ValidateFile("tags.html")

  def testContext(self):
    self.ValidateFile("context.html")

  def testReset(self):
    self.ValidateFile("reset.html")

  def testCData(self):
    self.ValidateFile("cdata.html")

  def testLineCount(self):
    self.ValidateFile("position.html")

  def testError(self):
    self.assertEqual(self.parser.GetErrorMessage(),
                     None)
    self.parser.Reset()

    self.assertEqual(self.parser.Parse("<a href='http://www.google.com' ''>\n"),
                     py_streamhtmlparser.HTML_STATE_ERROR)
    self.assertEqual(self.parser.GetErrorMessage(),
                     r"Unexpected character '\'' in state 'tag_space'")

    self.parser.Reset()
    self.assertEqual(self.parser.GetErrorMessage(),
                     None)

if __name__ == '__main__':
  unittest.main()
