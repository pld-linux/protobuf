#
# TODO:
#	- add bindings for java and python
#	- add vim syntax package
#
Summary:	Protocol Buffers - Google's data interchange format
Summary(pl.UTF-8):	Protocol Buffers - format wymiany danych Google
Name:		protobuf
Version:	2.4.0a
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	61df3f63ec284fc6f57a68c67e4918c6
URL:		http://code.google.com/p/protobuf/
BuildRequires:	libstdc++-devel
BuildRequires:	rpm-pythonprov
Requires:	%{name}-libs = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
Protocol buffers are a flexible, efficient, automated mechanism
for serializing structured data - similar to XML, but smaller,
faster, and simpler. You define how you want your data to be
structured once, then you can use special generated source code
to easily write and read your structured data to and from
a variety of data streams and using a variety of languages.
You can even update your data structure without breaking deployed
programs that are compiled against the "old" format.

Google uses Protocol Buffers for almost all of its internal RPC
protocols and file formats.

%description -l pl.UTF-8
Bufory protokołowe to elastyczny, wydajny i zautomatyzowany sposób
serializacji danych strukturalnych - podobny do XML-a, ale mniejszy,
szybszy i prostszy. Definiuje się raz, jaką strukturę mają mieć dane,
a następnie używa specjalnie wygenerowanego kodu źródłowego do łatwego
zapisu i odczytu danych strukturalnych do i z różnych strumieni
danych, z poziomu różnych języków. Można nawet uaktualniać strukturę
danych bez psucia programów skompilowanych w oparciu o "stary" format.

Google używa buforów protokołowych (Protocol Buffers) do prawie
wszystkich wewnętrznych protokołów RPC i formatów plików.

%package libs
Summary:	protobuf libraries
Summary(pl.UTF-8):	Biblioteki protobuf
Group:		Libraries

%description libs
protobuf libraries.

%description libs -l pl.UTF-8
Biblioteki protobuf.

%package devel
Summary:	Header files for protobuf libraries
Summary(pl.UTF-8):	Pliki nagłówkowe bibliotek protobuf
Group:		Development/Libraries
Requires:	%{name}-libs = %{version}-%{release}
Requires:	libstdc++-devel

%description devel
Header files for protobuf libraries.

%description devel -l pl.UTF-8
Pliki nagłówkowe bibliotek protobuf.

%package static
Summary:	Static protobuf libraries
Summary(pl.UTF-8):	Statyczne biblioteki protobuf
Group:		Development/Libraries
Requires:	%{name}-devel = %{version}-%{release}

%description static
Static protobuf libraries.

%description static -l pl.UTF-8
Statyczne biblioteki protobuf.

%prep
%setup -q

%build
%configure
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install examples/* $RPM_BUILD_ROOT%{_examplesdir}/%{name}-%{version}

%clean
rm -rf $RPM_BUILD_ROOT

%post	libs -p /sbin/ldconfig
%postun	libs -p /sbin/ldconfig

%files
%defattr(644,root,root,755)
%doc CHANGES.txt CONTRIBUTORS.txt README.txt
%attr(755,root,root) %{_bindir}/protoc

%files libs
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-lite.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf-lite.so.7
%attr(755,root,root) %{_libdir}/libprotobuf.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf.so.7
%attr(755,root,root) %{_libdir}/libprotoc.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotoc.so.7

%files devel
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libprotobuf-lite.so
%attr(755,root,root) %{_libdir}/libprotobuf.so
%attr(755,root,root) %{_libdir}/libprotoc.so
%{_libdir}/libprotobuf-lite.la
%{_libdir}/libprotobuf.la
%{_libdir}/libprotoc.la
%{_includedir}/google
%{_examplesdir}/%{name}-%{version}
%{_pkgconfigdir}/protobuf-lite.pc
%{_pkgconfigdir}/protobuf.pc

%files static
%defattr(644,root,root,755)
%{_libdir}/libprotobuf-lite.a
%{_libdir}/libprotobuf.a
%{_libdir}/libprotoc.a
