%define	_class	VFS
%define	modname	%{_class}
%define	__noautoreq /usr/bin/php

Summary:	Virtual File System API
Name:		php-pear-%{modname}
Version:	0.3.0
Release:	14
License:	PHP License
Group:		Development/PHP
Url:		http://pear.php.net/package/VFS/
Source0:	http://download.pear.php.net/package/%{modname}-%{version}.tgz
Patch0:		php-pear-VFS-0.3.0-fix-path.diff
BuildArch:	noarch
BuildRequires:	php-pear
Requires(post,preun):	php-pear
Requires:	php-pear

%description
This package provides a Virtual File System API, with backends for:
- SQL
- FTP
- Local Filesystems
- Hybrid SQL and filesystem

... and more planned. Reading/writing/listing of files are all
supported, and there are both object-based and array-based interfaces
to directory listing.

%prep
%setup -qc
%apply_patches
mv package.xml %{modname}-%{version}/%{modname}.xml

%install
cd %{modname}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{modname}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{modname}.xml %{buildroot}%{_datadir}/pear/packages

# bork
mv %{buildroot}%{_datadir}/pear/lib/VFS/kolab.php %{buildroot}%{_datadir}/pear/%{_class}/

%files
%{_bindir}/vfs
%{_datadir}/pear/%{_class}
%{_datadir}/pear/%{_class}.php
%{_datadir}/pear/data/%{_class}
%{_datadir}/pear/packages/%{modname}.xml
