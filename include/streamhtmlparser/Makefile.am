## Process this file with automake to produce Makefile.in

# Make sure that when we re-make ./configure, we get the macros we need
ACLOCAL_AMFLAGS = -I m4

# This is so we can #include <streamhtmlparser/foo>
AM_CPPFLAGS = -I$(top_srcdir)/src

# These are good warnings to turn on by default
if GCC
AM_CXXFLAGS = -Wall -Wwrite-strings -Woverloaded-virtual -Wno-sign-compare
endif

# The -no-undefined flag allows libtool to generate shared libraries for
# Cygwin and MinGW.  LIBSTDCXX_LA_LINKER_FLAG is used to fix a Solaris bug.
AM_LDFLAGS = -no-undefined $(LIBSTDCXX_LA_LINKER_FLAG)

googleincludedir = $(includedir)/$(PACKAGE)

## The .h files you want to install (that is, .h files that people
## who install this package can include in their own applications.)
googleinclude_HEADERS = \
  src/streamhtmlparser/statemachine.h \
  src/streamhtmlparser/jsparser.h \
  src/streamhtmlparser/htmlparser.h \
  src/streamhtmlparser/htmlparser_cpp.h

noinst_HEADERS = \
  src/streamhtmlparser/htmlparser_cpp.h.in

docdir = $(prefix)/share/doc/$(PACKAGE)-$(VERSION)
## This is for HTML and other documentation you want to install.
## Add your documentation files (in doc/) in addition to these
## top-level boilerplate files.  Also add a TODO file if you have one.
dist_doc_DATA = AUTHORS COPYING ChangeLog INSTALL NEWS README

lib_LTLIBRARIES = libstreamhtmlparser.la

if ENABLE_PYTHON

pyexec_LTLIBRARIES = py_streamhtmlparser.la

endif ENABLE_PYTHON

## unittests you want to run when people type 'make check'.
## TESTS is for binary unittests, check_SCRIPTS for script-based unittests.
## TESTS_ENVIRONMENT sets environment variables for when you run unittest,
## but it only seems to take effect for *binary* unittests (argh!)
TESTS =
TESTS_ENVIRONMENT = TESTDATA_PATH=$(top_srcdir)/src/tests/testdata
check_SCRIPTS = src/tests/generate_fsm_test_sh
# Every time you add a unittest to check_SCRIPTS, add it here too
noinst_SCRIPTS = src/tests/generate_fsm_test.sh

TESTDATA =

## vvvv RULES TO MAKE THE LIBRARIES, BINARIES, AND UNITTESTS

TESTS += statemachine_test
statemachine_test_SOURCES = src/tests/statemachine_test.c \
                            src/statemachine.c \
                            src/tests/statemachine_test_fsm.h

TESTS += jsparser_test
jsparser_test_SOURCES = src/tests/jsparser_test.c \
                        src/statemachine.c \
                        src/jsparser.c

TESTS += htmlparser_test
htmlparser_test_SOURCES = src/tests/htmlparser_test.c \
                          src/statemachine.c \
                          src/jsparser.c \
                          src/htmlparser.c

htmlparser_test_LDADD = libstreamhtmlparser.la

TESTS += htmlparser_cpp_test
htmlparser_cpp_test_SOURCES = src/tests/htmlparser_cpp_test.cc \
                              src/streamhtmlparser/htmlparser_cpp.h
htmlparser_cpp_test_LDADD = libstreamhtmlparser.la
TESTDATA += \
   src/tests/testdata/regtest/cdata.html \
   src/tests/testdata/regtest/comments.html \
   src/tests/testdata/regtest/context.html \
   src/tests/testdata/regtest/javascript_attribute.html \
   src/tests/testdata/regtest/javascript_block.html \
   src/tests/testdata/regtest/javascript_regexp.html \
   src/tests/testdata/regtest/position.html \
   src/tests/testdata/regtest/reset.html \
   src/tests/testdata/regtest/simple.html \
   src/tests/testdata/regtest/tags.html

TESTS += generate_fsm_c_test
generate_fsm_c_test_SOURCES = src/tests/generate_fsm_c_test.c
generate_fsm_c_test_DEPENDENCIES = src/tests/testdata/sample_fsm.c

src/tests/generate_fsm_test_sh: src/tests/generate_fsm_test.sh \
                                src/tests/testdata/sample_fsm.config \
                                src/tests/testdata/sample_fsm.c \
                                src/tools/generate_fsm.py
	$(top_srcdir)/src/tests/generate_fsm_test.sh $(top_srcdir)

TESTDATA += \
   src/tests/testdata/sample_fsm.config \
   src/tests/testdata/sample_fsm.c

if ENABLE_PYTHON

check_SCRIPTS += src/tests/py_streamhtmlparser_test_py
noinst_SCRIPTS += src/tests/py_streamhtmlparser_test.py

src/tests/py_streamhtmlparser_test_py: src/tests/py_streamhtmlparser_test.py
	export $(TESTS_ENVIRONMENT); \
	PYTHONPATH=".libs:$(PYTHONPATH)" \
	$(top_srcdir)/src/tests/py_streamhtmlparser_test.py

endif ENABLE_PYTHON

libstreamhtmlparser_la_SOURCES = src/statemachine.c \
src/jsparser.c \
src/htmlparser.c \
src/htmlparser_fsm.h \
src/jsparser_fsm.h

STREAMHTMLPARSER_SYMBOLS='^htmlparser_'

libstreamhtmlparser_la_CFLAGS = -DNDEBUG $(AM_CFLAGS)
libstreamhtmlparser_la_LDFLAGS = -export-symbols-regex $(STREAMHTMLPARSER_SYMBOLS)

if ENABLE_PYTHON

PYTHON_CFLAGS = -I/usr/include/python$(PYTHON_VERSION) -fpic
PYTHON_LDFLAGS = -avoid-version -module

py_streamhtmlparser_la_SOURCES = src/py_streamhtmlparser.c
py_streamhtmlparser_la_LIBADD = libstreamhtmlparser.la
py_streamhtmlparser_la_LDFLAGS = $(PYTHON_LDFLAGS)
py_streamhtmlparser_la_CFLAGS = $(PYTHON_CFLAGS)

endif ENABLE_PYTHON

## ^^^^ END OF RULES TO MAKE THE LIBRARIES, BINARIES, AND UNITTESTS


## This should always include $(TESTS), but may also include other
## binaries that you compile but don't want automatically installed.
noinst_PROGRAMS = $(TESTS)

rpm: dist-gzip packages/rpm.sh packages/rpm/rpm.spec
	@cd packages && ./rpm.sh ${PACKAGE} ${VERSION}

deb: dist-gzip packages/deb.sh packages/deb/*
	@cd packages && ./deb.sh ${PACKAGE} ${VERSION}

dist-hook:
	test ! -e "$(distdir)/vsprojects" \
	   || chmod -R u+w $(distdir)/*.sln $(distdir)/vsprojects/

EXTRA_DIST = packages/rpm.sh packages/rpm/rpm.spec packages/deb.sh packages/deb \
	autogen.sh $(SCRIPTS) src/solaris/libstdc++.la $(TESTDATA) \
  src/tools/generate_fsm.py src/tools/fsm_config.py \
  src/htmlparser_fsm.config src/jsparser_fsm.config \
  src/tests/statemachine_test_fsm.config \
	src/tests/testdata/sample_fsm.c \
  $(BUILT_SOURCES)

# These files are auto-generated via generate_fsm.py.  Since we don't want
# to require python to build ctemplate, we include these in the dist
src/htmlparser_fsm.h: src/tools/generate_fsm.py src/tools/fsm_config.py src/htmlparser_fsm.config
				$(top_srcdir)/src/tools/generate_fsm.py $(top_srcdir)/src/htmlparser_fsm.config > $@

src/jsparser_fsm.h: src/tools/generate_fsm.py src/tools/fsm_config.py src/jsparser_fsm.config
				$(top_srcdir)/src/tools/generate_fsm.py $(top_srcdir)/src/jsparser_fsm.config > $@

libtool: $(LIBTOOL_DEPS)
	$(SHELL) ./config.status --recheck

EXTRA_DIST += libtool

src/tests/statemachine_test_fsm.h: src/tools/generate_fsm.py src/tools/fsm_config.py src/tests/statemachine_test_fsm.config
				$(top_srcdir)/src/tools/generate_fsm.py $(top_srcdir)/src/tests/statemachine_test_fsm.config > $@

# This is a required hack for auto-generated .h files: cf the automake info pages
# NOTE: since we put these .h files in BUILT_SOURCES, we don't need to put
# them in as deps for the binaries that use them.  In fact, it's important
# that we don't; instead we put them in EXTRA_DIST.  This mean, in practice,
# they'll go at the end of the distribution tarfile, which means they'll
# have a later timestamp than the .config files that generate them, which
# means users won't try to rebuild them.  Ah, the joys of automake.
BUILT_SOURCES = src/htmlparser_fsm.h \
                src/jsparser_fsm.h \
                src/tests/statemachine_test_fsm.h
