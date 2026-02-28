# TODO:
# - add bindings for java (maven build)
# - add bindings for javascript
# - add bindings for csharp
#
# Conditional build:
%bcond_without	python3		# Python 3.x bindings
%bcond_with	ruby		# Ruby bindings
%bcond_without	tests		# test suite (requires 4+GB RAM on 64-bit archs)

# versions have diverged: for protoc 29.x binding version is 3.29.x, 4.29.x and 5.29.x depending on language
# see version.json for individual languages
%define	protoc_version	29.6
%define	cpp_version	5.%{protoc_version}
%define	python_version	5.%{protoc_version}
%define	ruby_version	4.%{protoc_version}
# libraries soname
%define	abi_ver		%{protoc_version}.0

# dependencies
%define	abseil_ver	20250814.0
Summary:	Protocol Buffers - Google's data interchange format
Summary(pl.UTF-8):	Protocol Buffers - format wymiany danych Google
Name:		protobuf
Version:	%{cpp_version}
Release:	1
License:	BSD
Group:		Libraries
#Source0Download: https://github.com/protocolbuffers/protobuf/releases
Source0:	https://github.com/protocolbuffers/protobuf/archive/v%{protoc_version}/%{name}-%{protoc_version}.tar.gz
# Source0-md5:	097e057e4e6e006e5127b43abf0a85bd
Source1:	ftdetect-proto.vim
Patch0:		%{name}-abseil-if_constexpr.patch
Patch3:		no-death-test.patch
URL:		https://github.com/protocolbuffers/protobuf/
BuildRequires:	abseil-cpp-devel >= %{abseil_ver}
%{?with_tests:BuildRequires:	abseil-cpp-test-devel >= %{abseil_ver}}
BuildRequires:	cmake >= 3.10
%{?with_tests:BuildRequires:	gmock-devel >= 1.9.0}
%{?with_tests:BuildRequires:	gtest-devel >= 1.9.0}
BuildRequires:	libstdc++-devel >= 6:7
BuildRequires:	pkgconfig
BuildRequires:	sed >= 4.0
%if %{with python3}
BuildRequires:	python3-modules >= 1:3.8
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

# False negative _ZN6google8protobuf8internal15ThreadSafeArena13thread_cache_E
%define		skip_post_check_so libprotoc.so.*

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
Requires:	utf8_range = %{version}-%{release}
Requires:	zlib >= 1.2.0.4

%description libs
Protocol Buffers library.

%description libs -l pl.UTF-8
Biblioteka buforów protokołowych (Protocol Buffers).

%package lite
Summary:	Protocol Buffers LITE_RUNTIME library
Summary(pl.UTF-8):	Biblioteka LITE_RUNTIME buforów protokołowych (Protocol Buffers)
Group:		Libraries
Requires:	utf8_range = %{version}-%{release}

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
Requires:	libstdc++-devel >= 6:7
Requires:	utf8_range-devel = %{version}-%{release}
Obsoletes:	protobuf-static < %{version}-%{release}

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

%package upb-devel
Summary:	upb - small protobuf implementation written in C
Summary(en.UTF-8):	μpb - small protobuf implementation written in C
Group:		Development/Libraries
Requires:	abseil-cpp-devel >= %{abseil_ver}
Requires:	utf8_range-devel = %{version}-%{release}

%description upb-devel
upb is a small protobuf implementation written in C.

%description upb-devel -l en.UTF-8
μpb (often written 'upb') is a small protobuf implementation written
in C.

%description upb-devel -l pl.UTF-8
μpb (często pisane "upb") to mała implementacja protobuf napisana w C.

%package -n utf8_range
Summary:	Fast UTF-8 validation Range algorithm libraries
Summary(pl.UTF-8):	Biblioteki szybkiego algorytmu Range do sprawdzania poprawności UTF-8
License:	MIT
Group:		Libraries
Requires:	abseil-cpp >= %{abseil_ver}

%description -n utf8_range
Fast UTF-8 validation Range algorithm libraries.

%description -n utf8_range -l pl.UTF-8
Biblioteki szybkiego algorytmu Range do sprawdzania poprawności
kodowania UTF-8.

%package -n utf8_range-devel
Summary:	Header files for utf8_range UTF-8 validation libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek utf8_range do sprawdzania poprawiości UTF-8
License:	MIT
Group:		Development/Libraries
Requires:	abseil-cpp-devel >= %{abseil_ver}
Requires:	utf8_range = %{version}-%{release}

%description -n utf8_range-devel
Header files for utf8_range UTF-8 validation libraries.

%description -n utf8_range-devel -l pl.UTF-8
Pliki nagłówkowe bibliotek utf8_range do sprawdzania poprawiości
kodowania UTF-8.

%package -n python3-protobuf
Summary:	Python 3 bindings for Protocol Buffers
Summary(pl.UTF-8):	Wiązania Pythona 3 do buforów protokołowych (Protocol Buffers)
Version:	%{python_version}
Group:		Development/Languages/Python
Requires:	python3-modules >= 1:3.8

%description -n python3-protobuf
Python 3 bindings for Protocol Buffers.

%description -n python3-protobuf -l pl.UTF-8
Wiązania Pythona 3 do buforów protokołowych (Protocol Buffers).

%package -n ruby-google-protobuf
Summary:	Ruby bindings for Google Protocol Buffers
Summary(pl.UTF-8):	Wiązania języka Ruby do biblioteki Google Protocol Buffers
Version:	%{ruby_version}
Group:		Development/Languages
Requires:	ruby

%description -n ruby-google-protobuf
Ruby bindings for Google Protocol Buffers.

%description -n ruby-google-protobuf -l pl.UTF-8
Wiązania języka Ruby do biblioteki Google Protocol Buffers.

%package -n vim-syntax-protobuf
Summary:	Vim syntax highlighting for Protocol Buffers descriptions
Summary(pl.UTF-8):	Podświetlanie składni Vima dla opisów buforów protokołowych (Protocol Buffers)
Version:	%{protoc_version}
Group:		Development/Libraries
Requires:	vim-rt >= 4:7.2.170

%description -n vim-syntax-protobuf
This package contains syntax highlighting for Protocol Buffers
descriptions in Vim editor.

%description -n vim-syntax-protobuf -l pl.UTF-8
Ten pakiet zawiera pliki podświetlania składni edytora Vim dla opisów
buforów protokołowych (Protocol Buffers).

%prep
%setup -q -n %{name}-%{protoc_version}
%patch -P0 -p1
%patch -P3 -p1

%{__sed} -i -e '1s, */usr/bin/env python$,%{__python3},' \
	examples/add_person.py \
	examples/list_people.py

%{__sed} -i -e '1s, */usr/bin/env ruby$,%{__ruby},' \
	examples/add_person.rb \
	examples/list_people.rb

ln -sf dist/setup.py python/setup.py

%build
mkdir -p build
cd build
%cmake .. \
	-Dprotobuf_BUILD_TESTS=%{__ON_OFF tests} \
	-Dprotobuf_USE_EXTERNAL_GTEST=ON \
	-Dprotobuf_ABSL_PROVIDER=package

%{__make}

export PROTOC="$(pwd)/protoc"
cd ..

%if %{with python3}
cd python
%py3_build
cd ..
%endif

%if %{with ruby}
cd ruby
rake
#rake clobber_package gem
cd ..
%endif

%if %{with tests}
%{__make} -C build test
%endif

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -d $RPM_BUILD_ROOT%{_vimdatadir}/{syntax,ftdetect}
cp -p editors/proto.vim $RPM_BUILD_ROOT%{_vimdatadir}/syntax/proto.vim
cp -p %{SOURCE1} $RPM_BUILD_ROOT%{_vimdatadir}/ftdetect/proto.vim

%if %{with python3}
cd python
%py3_install
cd ..
%endif

%if %{with ruby}
install -d $RPM_BUILD_ROOT{%{ruby_vendorarchdir}/google,%{ruby_vendorlibdir}/google,%{ruby_specdir}}
cp -p ruby/lib/google/protobuf_c.so $RPM_BUILD_ROOT%{ruby_vendorarchdir}/google
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
%doc CONTRIBUTORS.txt LICENSE README.md
%attr(755,root,root) %{_bindir}/protoc
%attr(755,root,root) %{_bindir}/protoc-%{abi_ver}
%{_libdir}/libprotoc.so.%{abi_ver}

%files libs
%defattr(644,root,root,755)
%{_libdir}/libprotobuf.so.%{abi_ver}

%files lite
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-lite.so.%{abi_ver}

%files devel
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-lite.so
%{_libdir}/libprotobuf.so
%{_libdir}/libprotoc.so
# XXX: dir shared with libtcmalloc
%dir %{_includedir}/google
%{_includedir}/google/protobuf
%{_pkgconfigdir}/protobuf-lite.pc
%{_pkgconfigdir}/protobuf.pc
%{_libdir}/cmake/protobuf
%{_examplesdir}/%{name}-%{version}

%files upb-devel
%defattr(644,root,root,755)
%doc upb/README.md
%attr(755,root,root) %{_bindir}/protoc-gen-upb
%attr(755,root,root) %{_bindir}/protoc-gen-upb-%{abi_ver}
%attr(755,root,root) %{_bindir}/protoc-gen-upb_minitable
%attr(755,root,root) %{_bindir}/protoc-gen-upb_minitable-%{abi_ver}
%attr(755,root,root) %{_bindir}/protoc-gen-upbdefs
%attr(755,root,root) %{_bindir}/protoc-gen-upbdefs-%{abi_ver}
%{_libdir}/libupb.a
%{_includedir}/upb
%{_includedir}/upb_generator
%{_pkgconfigdir}/upb.pc

%files -n utf8_range
%defattr(644,root,root,755)
%doc third_party/utf8_range/{LICENSE,README.md}
%{_libdir}/libutf8_range.so
%{_libdir}/libutf8_validity.so

%files -n utf8_range-devel
%defattr(644,root,root,755)
%{_includedir}/utf8_range.h
%{_includedir}/utf8_validity.h
%{_libdir}/cmake/utf8_range
%{_pkgconfigdir}/utf8_range.pc

%if %{with python3}
%files -n python3-protobuf
%defattr(644,root,root,755)
%doc python/README.md
%dir %{py3_sitedir}/google
%dir %{py3_sitedir}/google/_upb
%{py3_sitedir}/google/_upb/_message.cpython-*.so
%{py3_sitedir}/google/protobuf
%{py3_sitedir}/protobuf-%{python_version}-py*.egg-info
%{py3_sitedir}/protobuf-%{python_version}-py*-nspkg.pth
%endif

%if %{with ruby}
%files -n ruby-google-protobuf
%defattr(644,root,root,755)
%doc ruby/README.md
%dir %{ruby_vendorarchdir}/google
%{ruby_vendorarchdir}/google/protobuf_c.so
%dir %{ruby_vendorlibdir}/google
%{ruby_vendorlibdir}/google/protobuf.rb
%{ruby_vendorlibdir}/google/protobuf
%{ruby_specdir}/google-protobuf-%{version}.gemspec
%endif

%files -n vim-syntax-protobuf
%defattr(644,root,root,755)
%{_datadir}/vim/ftdetect/proto.vim
%{_datadir}/vim/syntax/proto.vim
