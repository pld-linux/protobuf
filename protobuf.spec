# TODO:
# - add bindings for java (maven build)
#
# Conditional build:
%bcond_without	python	# Python bindings
%bcond_without	tests	# perform "make check"

Summary:	Protocol Buffers - Google's data interchange format
Summary(pl.UTF-8):	Protocol Buffers - format wymiany danych Google
Name:		protobuf
Version:	2.6.1
Release:	2
License:	BSD
Group:		Libraries
Source0:	https://github.com/google/protobuf/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	af05b2cca289f7b86eef2734a0cdc8b9
Source1:	ftdetect-proto.vim
Patch0:		system-gtest.patch
URL:		https://github.com/google/protobuf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake
%{?with_tests:BuildRequires:	gtest-devel}
BuildRequires:	libstdc++-devel
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	rpmbuild(macros) >= 1.219
BuildRequires:	zlib-devel >= 1.2.0.4
%if %{with python}
BuildRequires:	python-google-apputils
BuildRequires:	python-setuptools
BuildRequires:	rpm-pythonprov
%endif
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vimdatadir	%{_datadir}/vim

%description
Protocol Buffers are a way of encoding structured data in an efficient
yet extensible format. Google uses Protocol Buffers for almost all of
its internal RPC protocols and file formats.

Protocol buffers are a flexible, efficient, automated mechanism for
serializing structured data - think XML, but smaller, faster, and
simpler. You define how you want your data to be structured once, then
you can use special generated source code to easily write and read
your structured data to and from a variety of data streams and using a
variety of languages. You can even update your data structure without
breaking deployed programs that are compiled against the "old" format.

This package contains Protocol Buffers compiler for all programming
languages.

%description -l pl.UTF-8
Bufory protokołowe (Protocol Buffers) to sposób kodowania danych
strukturalnych w wydajny i rozszerzalny sposób. Google używa buforów
protokołowych do prawie wszystkich wewnętrznych protokołów RPC i
formatów plików.

Bufory protokołowe to elastyczny, wydajny i zautomatyzowany sposób
serializacji danych strukturalnych - podobny do XML-a, ale mniejszy,
szybszy i prostszy. Definiuje się raz, jaką strukturę mają mieć dane,
a następnie używa specjalnie wygenerowanego kodu źródłowego do łatwego
zapisu i odczytu danych strukturalnych do i z różnych strumieni
danych, z poziomu różnych języków. Można nawet uaktualniać strukturę
danych bez psucia programów skompilowanych w oparciu o "stary" format.

Ten pakiet zawiera kompilator buforów protokołowych dla wszystkich
języków programowania. 

%package libs
Summary:	Protocol Buffers library
Summary(pl.UTF-8):	Biblioteka buforów protokołowych (Protocol Buffers)
Group:		Libraries
Requires:	zlib >= 1.2.0.4

%description libs
Protocol Buffers library.

%description libs -l pl.UTF-8
Biblioteka buforów protokołowych (Protocol Buffers).

%package lite
Summary:	Protocol Buffers LITE_RUNTIME library
Summary(pl.UTF-8):	Biblioteka LITE_RUNTIME buforów protokołowych (Protocol Buffers)
Group:		Libraries

%description lite
Protocol Buffers library for programs built with optimize_for =
LITE_RUNTIME.

The "optimize_for = LITE_RUNTIME" option causes the compiler to
generate code which only depends libprotobuf-lite, which is much
smaller than libprotobuf but lacks descriptors, reflection, and some
other features.

%description lite -l pl.UTF-8
Biblioteka buforów protokołowych (Protocol Buffers) zbudowana dla
programów z opcją optimize_for = LITE_RUNTIME.

Opcja ta powoduje, że kompilator generuje kod, który wymaga tylko
biblioteki libprotobuf-lite, która jest mniejsza niż libprotobuf, ale
nie ma niektórych elementów, takich jak deskryptory czy refleksje.

%package devel
Summary:	Header files for Protocol Buffers libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek buforów protokołowych (Protocol Buffers)
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}
Requires:	%{name}-libs = %{version}-%{release}
Requires:	%{name}-lite = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for Protocol Buffers libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek buforów protokołowych (Protocol Buffers).

%package static
Summary:	Static Protocol Buffers libraries
Summary(pl.UTF-8):	Statyczne biblioteki buforów protokołowych (Protocol Buffers)
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static Protocol Buffers libraries.

%description static -l pl.UTF-8
Statyczne biblioteki buforów protokołowych (Protocol Buffers).

%package -n python-protobuf
Summary:	Python bindings for Protocol Buffers
Summary(pl.UTF-8):	Wiązania Pythona do buforów protokołowych (Protocol Buffers)
Group:		Development/Languages/Python
# does not use C++ library at this time
Conflicts:	%{name} < %{version}
Conflicts:	%{name} > %{version}

%description -n python-protobuf
Python bindings for Protocol Buffers.

%description -n python-protobuf -l pl.UTF-8
Wiązania Pythona do buforów protokołowych (Protocol Buffers).

%package -n vim-syntax-protobuf
Summary:	Vim syntax highlighting for Protocol Buffers descriptions
Summary(pl.UTF-8):	Podświetlanie składni Vima dla opisów buforów protokołowych (Protocol Buffers)
Group:		Development/Libraries
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-protobuf
This package contains syntax highlighting for Protocol Buffers
descriptions in Vim editor.

%description -n vim-syntax-protobuf -l pl.UTF-8
Ten pakiet zawiera pliki podświetlania składni edytora Vim dla
opisów buforów protokołowych (Protocol Buffers).

%prep
%setup -q
%patch0 -p1

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# Additional variables defined according to https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=192821
%configure \
	CFLAGS='%{rpmcflags} -DGOOGLE_PROTOBUF_NO_RTTI' \
	CPPFLAGS='%{rpmcppflags} -DGOOGLE_PROTOBUF_NO_RTTI'
%{__make}

%if %{with python}
cd python
%{__python} setup.py build
%{__sed} -i -e 1d build/lib/google/protobuf/descriptor_pb2.py
cd ..
%endif

%if %{with tests}
%{__make} check
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	STRIPBINARIES=no \
	INSTALL="install -p"  \
	CPPROG="cp -p" \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_vimdatadir}/{syntax,ftdetect}
cp -p editors/proto.vim $RPM_BUILD_ROOT%{_vimdatadir}/syntax/proto.vim
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/proto.vim

%if %{with python}
cd python
%{__python} setup.py install \
	--root=$RPM_BUILD_ROOT \
	--single-version-externally-managed \
	--optimize=2
%py_postclean
cd ..
%endif

cp -p examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	-p /sbin/ldconfig
%postun	-p /sbin/ldconfig

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%post	lite -p /sbin/ldconfig
%postun	lite -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt CONTRIBUTORS.txt LICENSE README.md
%attr(755,root,root) %{_bindir}/protoc
%attr(755,root,root) %{_libdir}/libprotoc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotoc.so.9

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf.so.9

%files lite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-lite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf-lite.so.9

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-lite.so
%attr(755,root,root) %{_libdir}/libprotobuf.so
%attr(755,root,root) %{_libdir}/libprotoc.so
%{_libdir}/libprotobuf-lite.la
%{_libdir}/libprotobuf.la
%{_libdir}/libprotoc.la
# XXX: dir shared with libtcmalloc
%dir %{_includedir}/google
%{_includedir}/google/protobuf
%{_pkgconfigdir}/protobuf-lite.pc
%{_pkgconfigdir}/protobuf.pc
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a

%if %{with python}
%files -n python-protobuf
%defattr(644,root,root,755)
%doc python/README.txt
%dir %{py_sitescriptdir}/google
%{py_sitescriptdir}/google/protobuf
%{py_sitescriptdir}/protobuf-%{version}-py*.egg-info
%{py_sitescriptdir}/protobuf-%{version}-py*-nspkg.pth
%endif

%files -n vim-syntax-protobuf
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/proto.vim
%{_datadir}/vim/syntax/proto.vim
