%define		_class		VFS
%define		_status		beta
%define		_pearname	%{_class}
%define		_requires_exceptions 'pear(Horde/MIME/Magic.php)'

Summary:	Virtual File System API
Name:		php-pear-%{_pearname}
Version:	0.2.0
Release:	%mkrel 4
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/VFS/
Source0:	http://pear.php.net/get/%{_pearname}-%{version}.tgz
Patch0:		%{name}-path_fix.diff
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}-%{release}-buildroot

%description
This package provides a Virtual File System API, with backends for:
- SQL
- FTP
- Local Filesystems
- Hybrid SQL and filesystem

... and more planned. Reading/writing/listing of files are all
supported, and there are both object-based and array-based interfaces
to directory listing.

In PEAR status of this package is: %{_status}.

%prep
%setup -q -c

find . -type d -perm 0700 -exec chmod 755 {} \;
find . -type f -perm 0555 -exec chmod 755 {} \;
find . -type f -perm 0444 -exec chmod 644 {} \;

for i in `find . -type d -name CVS` `find . -type f -name .cvs\*` `find . -type f -name .#\*`; do
    if [ -e "$i" ]; then rm -rf $i; fi >&/dev/null
done

pushd %{_pearname}-%{version}
%patch0 -p0
popd

perl -pi -e "s|\@php_bin\@|%{_bindir}/pear|g" %{_pearname}-%{version}/scripts/%{_class}/*


%install
rm -rf %{buildroot}

install -d %{buildroot}%{_datadir}/pear/%{_class}

install %{_pearname}-%{version}/lib/*.php %{buildroot}%{_datadir}/pear
install %{_pearname}-%{version}/lib/%{_class}/*.php %{buildroot}%{_datadir}/pear/%{_class}

install -d %{buildroot}%{_datadir}/pear/data/%{_class}
install %{_pearname}-%{version}/data/%{_class}/* %{buildroot}%{_datadir}/pear/data/%{_class}/

install -d %{buildroot}%{_bindir}
install -m0755 %{_pearname}-%{version}/scripts/%{_class}/vfs.php %{buildroot}%{_bindir}/pear-%{_pearname}

install -d %{buildroot}%{_datadir}/pear/packages
install -m0644 package.xml %{buildroot}%{_datadir}/pear/packages/%{_pearname}.xml

%post
if [ "$1" = "1" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear install --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi
if [ "$1" = "2" ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear upgrade -f --nodeps -r %{_datadir}/pear/packages/%{_pearname}.xml
	fi
fi

%preun
if [ "$1" = 0 ]; then
	if [ -x %{_bindir}/pear -a -f %{_datadir}/pear/packages/%{_pearname}.xml ]; then
		%{_bindir}/pear uninstall --nodeps -r %{_pearname}
	fi
fi

%clean
rm -rf %{buildroot}

%files
%defattr(644,root,root,755)
%attr(0755,root,root) %{_bindir}/pear-%{_pearname}
%dir %{_datadir}/pear/%{_class}
%{_datadir}/pear/*.php
%{_datadir}/pear/%{_class}/*.php
%{_datadir}/pear/data/%{_class}/*
%{_datadir}/pear/packages/%{_pearname}.xml
