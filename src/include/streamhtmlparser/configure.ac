## Process this file with autoconf to produce configure.
## In general, the safest way to proceed is to run ./autogen.sh

# make sure we're interpreted by some minimal autoconf
AC_PREREQ(2.57)

AC_INIT(streamhtmlparser, 0.1, opensource@google.com)
# The argument here is just something that should be in the current directory
# (for sanity checking)
AC_CONFIG_SRCDIR(README)
AM_INIT_AUTOMAKE
AM_CONFIG_HEADER(src/config.h)

# Checks for programs.
AC_PROG_CC
AC_PROG_CXX
AC_PROG_CPP
AM_CONDITIONAL(GCC, test "$GCC" = yes)   # let the Makefile know if we're gcc
AC_PROG_LIBTOOL
AM_PATH_PYTHON([2.2], [have_python=yes], [have_python=no])

# Populate $host_cpu, $host_os, etc.
AC_CANONICAL_HOST
# Checks for header files.
AC_HEADER_STDC
AC_HEADER_STDBOOL
case $host_os in
  *mingw*)
    # Disabling fast install keeps libtool from creating wrapper scripts
    # around the executables it builds.  Such scripts have caused failures on
    # MinGW.  Using this option means an extra link step is executed during
    # "make install".
    AC_DISABLE_FAST_INSTALL
    ;;
esac

# Checks for typedefs, structures, and compiler characteristics.
AC_C_CONST
AC_C_INLINE
AC_TYPE_SIZE_T

# Checks for library functions.
AC_FUNC_MALLOC
AC_CHECK_FUNCS([strcasecmp strtol strstr])
AC_CHECK_FUNCS([memchr strchr])

AC_SUBST(LIBTOOL_DEPS)

# Find out what namespace 'normal' STL code lives in, and also what namespace
# the user wants our classes to be defined in
AC_CXX_STL_NAMESPACE
AC_DEFINE_GOOGLE_NAMESPACE(streamhtmlparser)

# Python configure flag
AC_ARG_ENABLE([python],
             [AS_HELP_STRING([--enable-python],
                             [build python bindings])],
             [],
             [enable_python="$have_python"])

AM_CONDITIONAL(ENABLE_PYTHON, test "$enable_python" = yes)

if test "$have_python" != yes -a "$enable_python" = yes; then
  AC_MSG_ERROR(Python not found or too old)
fi

# Solaris 10 6/06 has a bug where /usr/sfw/lib/libstdc++.la is empty.
# If so, we replace it with our own version.
LIBSTDCXX_LA_LINKER_FLAG=
if test -f /usr/sfw/lib/libstdc++.la && ! test -s /usr/sfw/lib/libstdc++.la
then
  LIBSTDCXX_LA_LINKER_FLAG='-L$(top_srcdir)/src/solaris'
fi
AC_SUBST(LIBSTDCXX_LA_LINKER_FLAG)

AC_SUBST(ac_google_namespace)
AC_SUBST(ac_google_start_namespace)
AC_SUBST(ac_google_end_namespace)

# Write generated configuration file
AC_CONFIG_FILES([Makefile \
                 src/streamhtmlparser/htmlparser_cpp.h \
                 ])
AC_OUTPUT
