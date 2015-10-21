// Copyright (c) 2008, Google Inc.
// All rights reserved.
//
// Redistribution and use in source and binary forms, with or without
// modification, are permitted provided that the following conditions are
// met:
//
//     * Redistributions of source code must retain the above copyright
// notice, this list of conditions and the following disclaimer.
//     * Redistributions in binary form must reproduce the above
// copyright notice, this list of conditions and the following disclaimer
// in the documentation and/or other materials provided with the
// distribution.
//     * Neither the name of Google Inc. nor the names of its
// contributors may be used to endorse or promote products derived from
// this software without specific prior written permission.
//
// THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
// "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
// LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
// A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
// OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
// SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
// LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
// DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
// THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
// (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
// OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
//
// ---
// Author: mjwiacek@google.com (Mike Wiacek)
//
// Python module providing bindings to the streamhtmlparser

#include <string.h>

#include <streamhtmlparser/htmlparser.h>
#include <streamhtmlparser/jsparser.h>

#include "Python.h"
#include "modsupport.h"

#define FQ_MODULE_NAME  "py_streamhtmlparser"

/* Parser Enumerated Types */
enum JavaScriptParserState {
  JS_STATE_TEXT = JSPARSER_STATE_TEXT,
  JS_STATE_Q = JSPARSER_STATE_Q,
  JS_STATE_DQ = JSPARSER_STATE_DQ,
  JS_STATE_REGEXP = JSPARSER_STATE_REGEXP,
  JS_STATE_COMMENT = JSPARSER_STATE_COMMENT,
};

enum HtmlParserState {
  HTML_STATE_TEXT = HTMLPARSER_STATE_TEXT,
  HTML_STATE_TAG = HTMLPARSER_STATE_TAG,
  HTML_STATE_ATTR = HTMLPARSER_STATE_ATTR,
  HTML_STATE_VALUE = HTMLPARSER_STATE_VALUE,
  HTML_STATE_COMMENT = HTMLPARSER_STATE_COMMENT,
  HTML_STATE_JS_FILE = HTMLPARSER_STATE_JS_FILE,
  HTML_STATE_CSS_FILE = HTMLPARSER_STATE_CSS_FILE,
  HTML_STATE_ERROR = HTMLPARSER_STATE_ERROR
};

enum AttributeType {
  ATTR_NONE = HTMLPARSER_ATTR_NONE,
  ATTR_REGULAR = HTMLPARSER_ATTR_REGULAR,
  ATTR_URI = HTMLPARSER_ATTR_URI,
  ATTR_JS = HTMLPARSER_ATTR_JS,
  ATTR_STYLE = HTMLPARSER_ATTR_STYLE
};

enum ParserMode {
  MODE_HTML = HTMLPARSER_MODE_HTML,
  MODE_JS = HTMLPARSER_MODE_JS,
  MODE_CSS = HTMLPARSER_MODE_CSS,
  MODE_HTML_IN_TAG = HTMLPARSER_MODE_HTML_IN_TAG
};

/* Python Module Prototype */
typedef struct {
  PyObject_HEAD;
  htmlparser_ctx *parser_;
} ParserObject;
staticforward PyTypeObject ParserObjectType;


static PyObject *ReturnStringOrNone(const char *ptr) {
  if (ptr == NULL) {
    Py_INCREF(Py_None);
    return Py_None;
  } else {
    return PyString_FromString(ptr);
  }
}

static PyObject *MakeBool(int i) {
  if (i) {
    Py_INCREF(Py_True);
    return Py_True;
  } else {
    Py_INCREF(Py_False);
    return Py_False;
  }
}

static ParserObject *CreateParserObject(void) {
  ParserObject *new = NULL;
  new = PyObject_New(ParserObject, &ParserObjectType);
  if (new == NULL) {
    return (ParserObject *)NULL;  // PyObject_New will set error flag.
  }
  new->parser_ = htmlparser_new();
  if (new->parser_ == NULL) {
    PyObject_Del(new);
    PyErr_Format(PyExc_AssertionError, "Unable to initialize HTML parser");
    return (ParserObject *)NULL;
  }
  return new;
}

static void DeleteParserObject(PyObject *ptr) {		
  ParserObject *self = (ParserObject *)ptr;
  if (self->parser_ != NULL) {
    htmlparser_delete(self->parser_);
  }
  PyObject_Del(ptr);
}

static char HtmlParser__doc__[] = "HtmlParser(): Return a new stream html parser.";
static ParserObject *HtmlParser(PyObject *self,
                                PyObject *args,
                                PyObject *kwdict) {
  ParserObject *new = NULL;
  new = CreateParserObject();

  if (PyErr_Occurred()) {
    Py_DECREF(new);
    return NULL;
  }

  return new;
}

static char parse__doc__[] = "Parse the provided string";
static PyObject *Parse(ParserObject *self, PyObject *args) {
  char *str = NULL;
  int len = -1;

  if (!PyArg_Parse(args, "s#", &str, &len)) {
    return NULL;
  }

  return PyInt_FromLong(htmlparser_parse(self->parser_, str, len));
}

static char tag__doc__[] = "Return the current tag from the parser or None if"
                           " no tag is available.";
static PyObject *tag(ParserObject *self, PyObject *args) {
  const char *tag = NULL;
  tag = htmlparser_tag(self->parser_);
  return ReturnStringOrNone(tag);
}

static char state__doc__[] = "Return the current state the parser is in";
static PyObject *state(ParserObject *self, PyObject *args) {
  return PyInt_FromLong(htmlparser_state(self->parser_));
}

static char attribute__doc__[] = "Returns the current attribute name if "
                                 "inside an attribute name or an attribute "
                                 "value. Rettribute value. Returns NULL "
                                 "otherwise.";
static PyObject *attribute(ParserObject *self, PyObject *args) {
  const char *attr = NULL;
  attr = htmlparser_attr(self->parser_);
  return ReturnStringOrNone(attr);
}

static char value__doc__[] = "Returns the contents of the current "
                             "attribute value";
static PyObject *value(ParserObject *self, PyObject *args) {
  const char *value = NULL;
  value = htmlparser_value(self->parser_);
  return ReturnStringOrNone(value);
}

static char in_javascript__doc__[] = "Returns true if inside javascript."
                                     "This can be a javascript block, a "
                                     "javascript attribute value, or the "
                                     "parser may be in javascript mode.";
static PyObject *InJavaScript(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_in_js(self->parser_));
}

static char is_attribute_quoted__doc__[] = "Returns true if the current "
                                           "attribute is quoted";
static PyObject *IsAttributeQuoted(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_is_attr_quoted(self->parser_));
}

static char is_javascript_quoted__doc__[] = "Returns true if the parser is"
                                            " inside a string literal.";
static PyObject *IsJavaScriptQuoted(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_is_js_quoted(self->parser_));
}

static char in_css__doc__[] = "Returns true if the parser is currently inside "
                              "a CSS construct. Currently this can be either "
                              "a STYLE tag, a STYLE attribute or the fact "
                              "that the parser was reset in MODE_CSS using "
                              "ResetMode().";
static PyObject *InCss(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_in_css(self->parser_));
}

static char value_index__doc__[] = "Returns the index within the current value"
                                   " or None if the parser is not inside an"
                                   " attribute value";
static PyObject *value_index(ParserObject *self, PyObject *args) {
  int index = -1;
  index = htmlparser_value_index(self->parser_);
  if (index == -1) {
    Py_INCREF(Py_None);
    return Py_None;
  } else {
    return PyInt_FromLong(index);
  }
}

static char is_url_start__doc__[] = "Returns true if this is the first"
                                    " character of a url inside an attribute.";
static PyObject *is_url_start(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_is_url_start(self->parser_));
}


static char attribute_type__doc__[] = "Returns the current attribute type.";
static PyObject *attribute_type(ParserObject *self, PyObject *args) {
  return PyInt_FromLong(htmlparser_attr_type(self->parser_));
}

static char get_line__doc__[] = "Return the current line number.";
static PyObject *get_line_number(ParserObject *self, PyObject *args) {
  return PyInt_FromLong(htmlparser_get_line_number(self->parser_));
}

static char set_line__doc__[] = "Set the current line number";
static PyObject *set_line_number(ParserObject *self, PyObject *args) {
  int line = 1;
  if (!PyArg_Parse(args, "i", &line)) {
    return NULL;
  }

  htmlparser_set_line_number(self->parser_, line);
  Py_INCREF(Py_None);
  return Py_None;
}

static char get_column__doc__[] = "Return the current column number.";
static PyObject *get_column_number(ParserObject *self, PyObject *args) {
  return PyInt_FromLong(htmlparser_get_column_number(self->parser_));
}

static char set_column__doc__[] = "Set the current column number.";
static PyObject *set_column_number(ParserObject *self, PyObject *args) {
  int column = 1;
  if (!PyArg_Parse(args, "i", &column)) {
    return NULL;
  }

  htmlparser_set_column_number(self->parser_, column);
  Py_INCREF(Py_None);
  return Py_None;
}

static char get_error_message__doc__[] = "Return a human readable error message"
                                         " or no message if there was no"
                                         " error.";
static PyObject *GetErrorMessage(ParserObject *self, PyObject *args) {
  const char *error_message = NULL;
  error_message = htmlparser_get_error_msg(self->parser_);
  return ReturnStringOrNone(error_message);
}

static char javascript_state__doc__[] = "Returns the current state of the "
                                        "javascript parser. [For testing only!]";
static PyObject *javascript_state(ParserObject *self, PyObject *args) {
  return PyInt_FromLong(htmlparser_js_state(self->parser_));
}

static char copy_from__doc__[] = "Copies the context of the HtmlParser object "
                                 "referenced in the argument to the current "
                                 "object.";
static PyObject *CopyFrom(ParserObject *self, PyObject *arg) {
  ParserObject *src;

  if (arg->ob_type != self->ob_type) {
    PyErr_SetString(PyExc_TypeError, "expected ParserObject object");
    return NULL;
  }

  src = (ParserObject *)arg;
  htmlparser_copy(self->parser_, src->parser_);
  Py_INCREF(Py_None);
  return Py_None;
}

static char reset__doc__[] = "Reset the parser to its initial state and "
                             "default (MODE_HTML) mode.";
static PyObject *Reset(ParserObject *self, PyObject *args) {
  htmlparser_reset(self->parser_);
  Py_INCREF(Py_None);
  return Py_None;
}

static char reset_mode__doc__[] = "Reset parser to its initial state and "
                                  "change the parser mode";
static PyObject *ResetMode(ParserObject *self, PyObject *args) {
  int mode = -1;
  if (!PyArg_Parse(args, "i", &mode)) {
    return NULL;
  }

  if (mode != MODE_HTML &&
      mode != MODE_JS &&
      mode != MODE_CSS &&
      mode != MODE_HTML_IN_TAG) {
    PyErr_Format(PyExc_ValueError, "Mode must be MODE_HTML or MODE_JS");
    return NULL;
  }

  htmlparser_reset_mode(self->parser_, mode);
  Py_INCREF(Py_None);
  return Py_None;
}

static char insert_text__doc__[] = "TODO(mjwiacek): Put something here.";
static PyObject *insert_text(ParserObject *self, PyObject *args) {
  return MakeBool(htmlparser_insert_text(self->parser_));
}

static PyMethodDef parserMethods[] = {
  {"Parse", (PyCFunction)Parse, METH_O, parse__doc__},
  {"Tag", (PyCFunction)tag, METH_NOARGS, tag__doc__},
  {"State", (PyCFunction)state, METH_NOARGS, state__doc__},
  {"Attribute", (PyCFunction)attribute, METH_NOARGS, attribute__doc__},
  {"Value", (PyCFunction)value, METH_NOARGS, value__doc__},
  {"InJavaScript", (PyCFunction)InJavaScript, METH_NOARGS,
      in_javascript__doc__},
  {"IsAttributeQuoted", (PyCFunction)IsAttributeQuoted, METH_NOARGS,
      is_attribute_quoted__doc__},
  {"IsJavaScriptQuoted", (PyCFunction)IsJavaScriptQuoted, METH_NOARGS,
      is_javascript_quoted__doc__},
  {"InCss", (PyCFunction)InCss, METH_NOARGS, in_css__doc__},
  {"ValueIndex", (PyCFunction)value_index, METH_NOARGS, value_index__doc__},
  {"IsUrlStart", (PyCFunction)is_url_start, METH_NOARGS, value_index__doc__},
  {"AttributeType", (PyCFunction)attribute_type, METH_NOARGS,
      attribute_type__doc__},
  {"GetLineNumber", (PyCFunction)get_line_number, METH_NOARGS, get_line__doc__},
  {"SetLineNumber", (PyCFunction)set_line_number, METH_O, set_line__doc__},
  {"GetColumnNumber", (PyCFunction)get_column_number, METH_NOARGS,
      get_column__doc__},
  {"SetColumnNumber", (PyCFunction)set_column_number, METH_O,
      set_column__doc__},
  {"GetErrorMessage", (PyCFunction)GetErrorMessage, METH_NOARGS,
      get_error_message__doc__},
  {"JavaScriptState", (PyCFunction)javascript_state, METH_NOARGS,
      javascript_state__doc__},
  {"CopyFrom", (PyCFunction)CopyFrom, METH_O, copy_from__doc__},
  {"Reset", (PyCFunction)Reset, METH_NOARGS, reset__doc__},
  {"ResetMode", (PyCFunction)ResetMode, METH_O, reset_mode__doc__},
  {"InsertText", (PyCFunction)insert_text, METH_NOARGS, insert_text__doc__},
  {NULL, NULL} /* sentinel */
};

static int parser_setattr(PyObject *ptr, char *name, PyObject *v) {
  ParserObject *self=(ParserObject *)ptr;
  return 0;
}

static PyObject * parser_getattr(PyObject *ptr, char *name) {
  ParserObject *self = (ParserObject *)ptr;
  return Py_FindMethod(parserMethods, (PyObject *) self, name);
}

// List of functions defined in the module
static struct PyMethodDef modulemethods[] = {
  {"HtmlParser", (PyCFunction) HtmlParser, METH_NOARGS, HtmlParser__doc__},
  {NULL, NULL} /* sentinel */
};

static PyTypeObject ParserObjectType = {
  PyObject_HEAD_INIT(NULL)
  0, /*ob_size*/
  "py_streamhtmlparser", /*tp_name*/
  sizeof(ParserObject),	/*tp_size*/
  0, /*tp_itemsize*/
  DeleteParserObject, /*tp_dealloc*/
  0, /*tp_print*/
  parser_getattr, /*tp_getattr*/
  parser_setattr, /*tp_setattr*/
  0, /*tp_compare*/
  (reprfunc) 0, /*tp_repr*/
  0, /*tp_as_number*/
};

void initpy_streamhtmlparser (void) {
  PyObject *m = NULL;
  ParserObjectType.ob_type = &PyType_Type;

  /* Create the module and add the functions */
  m = Py_InitModule(FQ_MODULE_NAME, modulemethods);

  PyModule_AddIntConstant(m, "JS_STATE_TEXT", JS_STATE_TEXT);
  PyModule_AddIntConstant(m, "JS_STATE_Q", JS_STATE_Q);
  PyModule_AddIntConstant(m, "JS_STATE_DQ", JS_STATE_DQ);
  PyModule_AddIntConstant(m, "JS_STATE_REGEXP", JS_STATE_REGEXP);
  PyModule_AddIntConstant(m, "JS_STATE_COMMENT", JS_STATE_COMMENT);
  PyModule_AddIntConstant(m, "HTML_STATE_TEXT", HTML_STATE_TEXT);
  PyModule_AddIntConstant(m, "HTML_STATE_TAG", HTML_STATE_TAG);
  PyModule_AddIntConstant(m, "HTML_STATE_ATTR", HTML_STATE_ATTR);
  PyModule_AddIntConstant(m, "HTML_STATE_VALUE", HTML_STATE_VALUE);
  PyModule_AddIntConstant(m, "HTML_STATE_COMMENT", HTML_STATE_COMMENT);
  PyModule_AddIntConstant(m, "HTML_STATE_JS_FILE", HTML_STATE_JS_FILE);
  PyModule_AddIntConstant(m, "HTML_STATE_CSS_FILE", HTML_STATE_CSS_FILE);
  PyModule_AddIntConstant(m, "HTML_STATE_ERROR", HTML_STATE_ERROR);
  PyModule_AddIntConstant(m, "ATTR_NONE", ATTR_NONE);
  PyModule_AddIntConstant(m, "ATTR_REGULAR", ATTR_REGULAR);
  PyModule_AddIntConstant(m, "ATTR_URI", ATTR_URI);
  PyModule_AddIntConstant(m, "ATTR_JS", ATTR_JS);
  PyModule_AddIntConstant(m, "ATTR_STYLE", ATTR_STYLE);
  PyModule_AddIntConstant(m, "MODE_HTML", MODE_HTML);
  PyModule_AddIntConstant(m, "MODE_JS", MODE_JS);
  PyModule_AddIntConstant(m, "MODE_CSS", MODE_CSS);
  PyModule_AddIntConstant(m, "MODE_HTML_IN_TAG", MODE_HTML_IN_TAG);

  /* Check for errors */
  if (PyErr_Occurred())
    Py_FatalError("can't initialize module google3.security.streamhtmlparser.py_streamhtmlparser");
}
