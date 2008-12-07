#
# TODO:
#	- add bindings for java and python
#	- add vim syntax package
#
Summary:	Protocol Buffers - Google's data interchange format
Summary(pl.UTF-8):	Protocol Buffers - format wymiany danych Google
Name:		protobuf
Version:	2.0.3
Release:	1
License:	BSD
Group:		Libraries
Source0:	http://protobuf.googlecode.com/files/%{name}-%{version}.tar.bz2
# Source0-md5:	37e6e4d63434672c70bd977be9c372cb
URL:		http://code.google.com/p/protobuf/
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

#%description -l pl.UTF-8

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
%attr(755,root,root) %{_libdir}/libproto*.so.*.*.*
%attr(755,root,root) %ghost %{_libdir}/libprotobuf.so.3
%attr(755,root,root) %ghost %{_libdir}/libprotoc.so.3

%files devel
%defattr(644,root,root,755)
%{_includedir}/google
%attr(755,root,root) %{_libdir}/libproto*.la
%attr(755,root,root) %{_libdir}/libproto*.so
%{_examplesdir}/%{name}-%{version}

%files static
%defattr(644,root,root,755)
%attr(755,root,root) %{_libdir}/libproto*.a
