%define	RELEASE	1
%define rel     %{?CUSTOM_RELEASE} %{!?CUSTOM_RELEASE:%RELEASE}
%define	prefix	/usr

Name: %NAME
Summary: Streamming html context scanner in C
Version: %VERSION
Release: %rel
Group: Development/Libraries
URL: http://code.google.com/p/streamhtmlparser/
License: BSD
Vendor: Google
Packager: Google Inc. <opensource@google.com>
Source: http://%{NAME}.googlecode.com/files/%{NAME}-%{VERSION}.tar.gz
Distribution: Redhat 7 and above.
Buildroot: %{_tmppath}/%{name}-root
Prefix: %prefix

%description
Implementation of an html context scanner with no lookahead. Its purpose is to
scan an html stream and provide context information at any point within the
input stream. An example of a user of this scanner would be an auto escaping
templating system, which would require html context information at very
specific points within the html stream. The implementation is based on a
simplified state machine of HTML4.1.

%package devel
Summary: Streamming html context scanner in C
Group: Development/Libraries
Requires: %{NAME} = %{VERSION}

%description devel
Implementation of an html context scanner with no lookahead. Its purpose is to
scan an html stream and provide context information at any point within the
input stream. An example of a user of this scanner would be an auto escaping
templating system, which would require html context information at very
specific points within the html stream. The implementation is based on a
simplified state machine of HTML4.1.

%changelog
    * Thu Mar 19 2009 <opensource@google.com>
    - First draft

%prep
%setup

%build
%configure
make

%install
rm -rf $RPM_BUILD_ROOT
make DESTDIR=$RPM_BUILD_ROOT install

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(-,root,root)

## Mark all installed files within /usr/share/doc/{package name} as
## documentation (eg README, Changelog).  This depends on the following
## two lines appearing in Makefile.am:
##     docdir = $(prefix)/share/doc/$(PACKAGE)-$(VERSION)
##     dist_doc_DATA = AUTHORS COPYING ChangeLog INSTALL NEWS README
%docdir %{prefix}/share/doc/%{NAME}-%{VERSION}
%{prefix}/share/doc/%{NAME}-%{VERSION}/*
## This captures the rest of your documentation; the stuff in doc/
## %doc doc/*

%{_libdir}/*

%files devel
%defattr(-,root,root)
%{prefix}/include/streamhtmlparser
