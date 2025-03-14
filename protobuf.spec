# TODO:
# - add bindings for java (maven build)
# - add bindings for javascript
# - add bindings for csharp
#
# Conditional build:
%bcond_without	python3	# Python 3.x bindings
%bcond_without	ruby	# Ruby bindings
%bcond_without	tests	# perform "make check" (requires 4+GB RAM on 64-bit archs)

Summary:	Protocol Buffers - Google's data interchange format
Summary(pl.UTF-8):	Protocol Buffers - format wymiany danych Google
Name:		protobuf
Version:	3.20.3
Release:	3
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/google/protobuf/releases
Source0:	https://github.com/google/protobuf/releases/download/v%{version}/%{name}-all-%{version}.tar.gz
# Source0-md5:	a1e8f594f998576180ff1efa49007f54
Source1:	ftdetect-proto.vim
Source2:	https://github.com/protocolbuffers/utf8_range/archive/1d1ea7e3fedf482d4a12b473c1ed25fe0f371a45/utf8_range-20231110.tar.gz
# Source2-md5:	3ee3e8809236fbac057b26e502afe4cb
Patch0:		system-gtest.patch
Patch1:		no-wrap-memcpy.patch
Patch2:		%{name}-x32.patch
Patch3:		%{name}-32bit.patch
URL:		https://github.com/google/protobuf/
BuildRequires:	autoconf >= 2.59
BuildRequires:	automake >= 1:1.11
%{?with_tests:BuildRequires:	gmock-devel >= 1.9.0}
%{?with_tests:BuildRequires:	gtest-devel >= 1.9.0}
BuildRequires:	libstdc++-devel >= 6:4.7
BuildRequires:	libtool
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.3
BuildRequires:	python3-setuptools
BuildRequires:	rpm-pythonprov
%endif
BuildRequires:	rpmbuild(macros) >= 1.714
%if %{with ruby}
BuildRequires:	ruby-devel
BuildRequires:	ruby-rake
BuildRequires:	ruby-rake-compiler
%endif
BuildRequires:	sed >= 4.0
BuildRequires:	zlib-devel >= 1.2.0.4
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_vimdatadir	%{_datadir}/vim

# triggers bogus "overflow in constant expression" errors with gcc 4.9 .. 5.4
%define		filterout	-fwrapv

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
Requires:	libstdc++-devel >= 6:4.7

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
Summary:	Python 2 bindings for Protocol Buffers
Summary(pl.UTF-8):	Wiązania Pythona 2 do buforów protokołowych (Protocol Buffers)
Group:		Development/Languages/Python
Requires:	python-modules >= 1:2.7
# does not use C++ library at this time
BuildArch:	noarch

%description -n python-protobuf
Python 2 bindings for Protocol Buffers.

%description -n python-protobuf -l pl.UTF-8
Wiązania Pythona 2 do buforów protokołowych (Protocol Buffers).

%package -n python3-protobuf
Summary:	Python 3 bindings for Protocol Buffers
Summary(pl.UTF-8):	Wiązania Pythona 3 do buforów protokołowych (Protocol Buffers)
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.3
# does not use C++ library at this time
BuildArch:	noarch

%description -n python3-protobuf
Python 3 bindings for Protocol Buffers.

%description -n python3-protobuf -l pl.UTF-8
Wiązania Pythona 3 do buforów protokołowych (Protocol Buffers).

%package -n ruby-google-protobuf
Summary:	Ruby bindings for Google Protocol Buffers
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki Google Protocol Buffers
Group:		Development/Languages
Requires:	ruby

%description -n ruby-google-protobuf
Ruby bindings for Google Protocol Buffers.

%description -n ruby-google-protobuf -l pl.UTF-8
Wiązania języka Ruby do biblioteki Google Protocol Buffers.

%package -n vim-syntax-protobuf
Summary:	Vim syntax highlighting for Protocol Buffers descriptions
Summary(pl.UTF-8):	Podświetlanie składni Vima dla opisów buforów protokołowych (Protocol Buffers)
Group:		Development/Libraries
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-protobuf
This package contains syntax highlighting for Protocol Buffers
descriptions in Vim editor.

%description -n vim-syntax-protobuf -l pl.UTF-8
Ten pakiet zawiera pliki podświetlania składni edytora Vim dla opisów
buforów protokołowych (Protocol Buffers).

%prep
%setup -q -a2
%patch -P 0 -p1
%patch -P 1 -p1
%patch -P 2 -p1
#%ifnarch %{x8664} aarch64 alpha ia64 mips64 ppc64 s390x sparc64
%patch -P 3 -p1
#%endif

%{__mv} utf8_range-* third_party/utf8_range

%{__sed} -i -e '1s,/usr/bin/env python$,%{__python3},' \
	examples/add_person.py \
	examples/list_people.py

# gcc 10.2 false positive warning (with tag values >= 128):
#
#  if (tag < 128) {
#    return *ptr == tag;
#           ~~~~~^~~~~~ error: comparison is always false due to limited range of data type [-Werror=type-limits]
#  } else {
#
#%{__sed} -i -e 's/-Werror //' src/Makefile.am

%ifarch %{ix86} x32
# fail due to memory space limit or some unexpected allocation sizes(?)
%{__sed} -i -e '/^TEST/ s/AnyTest, TestPackFromSerializationExceedsSizeLimit/DISABLED_&/' src/google/protobuf/any_test.cc
%{__sed} -i -e '/^TEST/ s/ArenaTest, \(SpaceAllocated_and_Used\|BlockSizeSmallerThanAllocation\)/DISABLED_&/' src/google/protobuf/arena_unittest.cc
%endif

%build
%{__libtoolize}
%{__aclocal} -I m4
%{__autoconf}
%{__autoheader}
%{__automake}
# Additional variables defined according to https://bugs.freebsd.org/bugzilla/show_bug.cgi?id=192821
%configure \
	CFLAGS='%{rpmcflags} -DGOOGLE_PROTOBUF_NO_RTTI' \
	CPPFLAGS='%{rpmcppflags} -DGOOGLE_PROTOBUF_NO_RTTI' \
	--disable-silent-rules \
	--disable-external-gtest
%{__make}

cd python
%if %{with python3}
%py3_build
%endif
cd ..

%if %{with ruby}
cd ruby
rake
#rake clobber_package gem
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

cd python
%if %{with python3}
%py3_install
%endif
cd ..

%if %{with ruby}
install -d $RPM_BUILD_ROOT{%{ruby_vendorarchdir}/google,%{ruby_vendorlibdir}/google,%{ruby_specdir}}
install ruby/lib/google/protobuf_c.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/google
cp -pr ruby/lib/google/{protobuf,protobuf.rb} $RPM_BUILD_ROOT%{ruby_vendorlibdir}/google
cp -p ruby/google-protobuf.gemspec $RPM_BUILD_ROOT%{ruby_specdir}/google-protobuf-%{version}.gemspec
%endif
cp -pr examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

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
%attr(755,root,root) %ghost %{_libdir}/libprotoc.so.31

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf.so.31

%files lite
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-lite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf-lite.so.31

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

%if %{with python3}
%files -n python3-protobuf
%defattr(644,root,root,755)
%doc python/README.md
%dir %{py3_sitescriptdir}/google
%{py3_sitescriptdir}/google/protobuf
%{py3_sitescriptdir}/protobuf-%{version}-py*.egg-info
%{py3_sitescriptdir}/protobuf-%{version}-py*-nspkg.pth
%endif

%if %{with ruby}
%files -n ruby-google-protobuf
%defattr(644,root,root,755)
%doc ruby/README.md
%dir %{ruby_vendorarchdir}/google
%attr(755,root,root) %{ruby_vendorarchdir}/google/protobuf_c.so
%dir %{ruby_vendorlibdir}/google
%{ruby_vendorlibdir}/google/protobuf.rb
%{ruby_vendorlibdir}/google/protobuf
%{ruby_specdir}/google-protobuf-%{version}.gemspec
%endif

%files -n vim-syntax-protobuf
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/proto.vim
%{_datadir}/vim/syntax/proto.vim
