%define		_class		VFS
%define		upstream_name	%{_class}
%define		_requires_exceptions pear(Horde

Name:		php-pear-%{upstream_name}
Version:	0.3.0
Release:	%mkrel 2
Summary:	Virtual File System API
License:	PHP License
Group:		Development/PHP
URL:		http://pear.php.net/package/VFS/
Source0:	http://download.pear.php.net/package/%{upstream_name}-%{version}.tgz
Patch0:		php-pear-VFS-0.3.0-fix-path.diff
Requires(post): php-pear
Requires(preun): php-pear
Requires:	php-pear
BuildRequires:	php-pear
BuildArch:	noarch
BuildRoot:	%{_tmppath}/%{name}-%{version}

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
%setup -q -c
%patch0 -p 1
mv package.xml %{upstream_name}-%{version}/%{upstream_name}.xml

%install
rm -rf %{buildroot}

cd %{upstream_name}-%{version}
pear install --nodeps --packagingroot %{buildroot} %{upstream_name}.xml
rm -rf %{buildroot}%{_datadir}/pear/.??*

rm -rf %{buildroot}%{_datadir}/pear/docs
rm -rf %{buildroot}%{_datadir}/pear/tests

install -d %{buildroot}%{_datadir}/pear/packages
install -m 644 %{upstream_name}.xml %{buildroot}%{_datadir}/pear/packages

# bork
mv %{buildroot}%{_datadir}/pear/lib/VFS/kolab.php %{buildroot}%{_datadir}/pear/%{_class}/

%clean
rm -rf %{buildroot}

%post
%if %mdkversion < 201000
pear install --nodeps --soft --force --register-only \
    %{_datadir}/pear/packages/%{upstream_name}.xml >/dev/null || :
%endif

%preun
%if %mdkversion < 201000
if [ "$1" -eq "0" ]; then
    pear uninstall --nodeps --ignore-errors --register-only \
        %{upstream_name} >/dev/null || :
fi
%endif

%files
%defattr(-,root,root)
%{_bindir}/vfs
%{_datadir}/pear/%{_class}
%{_datadir}/pear/%{_class}.php
%{_datadir}/pear/data/%{_class}
%{_datadir}/pear/packages/%{upstream_name}.xml


%changelog
* Fri Dec 16 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-2mdv2012.0
+ Revision: 741815
- fix major breakage by careless packager

* Mon Nov 28 2011 Oden Eriksson <oeriksson@mandriva.com> 0.3.0-1
+ Revision: 735253
- fix build
- new version

* Thu May 05 2011 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-6
+ Revision: 667646
- mass rebuild

* Fri Dec 03 2010 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-5mdv2011.0
+ Revision: 607163
- rebuild

* Mon Nov 16 2009 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-4mdv2010.1
+ Revision: 466489
- rediff patch for md5sum value
- spec cleanup
- use pear installer
- don't ship tests, even in documentation
- own all directories
- use rpm filetriggers starting from mandriva 2010.1

* Thu Sep 03 2009 Christophe Fergeau <cfergeau@mandriva.com> 0.2.0-4mdv2010.0
+ Revision: 426672
- rebuild

* Thu Jan 01 2009 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-3mdv2009.1
+ Revision: 321931
- rebuild

* Thu Sep 11 2008 Guillaume Rousse <guillomovitch@mandriva.org> 0.2.0-2mdv2009.0
+ Revision: 283895
- fix dependencies
- don't duplicate spec-helper work for DOS eol removal
- don't duplicate package name in summary

* Wed Aug 20 2008 Oden Eriksson <oeriksson@mandriva.com> 0.2.0-1mdv2009.0
+ Revision: 274175
- fix "build"
- 0.2.0

* Wed Jun 18 2008 Thierry Vignaud <tv@mandriva.org> 0.1.0-3mdv2009.0
+ Revision: 224892
- rebuild

* Tue Mar 04 2008 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-2mdv2008.1
+ Revision: 178548
- rebuild

  + Olivier Blin <blino@mandriva.org>
    - restore BuildRoot

  + Thierry Vignaud <tv@mandriva.org>
    - kill re-definition of %%buildroot on Pixel's request


* Sat Nov 11 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdv2007.0
+ Revision: 82804
- Import php-pear-VFS

* Sat May 20 2006 Oden Eriksson <oeriksson@mandriva.com> 0.1.0-1mdk
- 0.1.0
- rediffed P0

* Fri Feb 10 2006 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-7mdk
- new group (Development/PHP)

* Fri Aug 26 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-6mdk
- rebuilt to fix auto deps

* Wed Aug 10 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-5mdk
- rebuilt to use new pear auto deps/reqs from pld

* Sun Jul 31 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-4mdk
- fix deps

* Thu Jul 21 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-3mdk
- reworked the %%post and %%preun stuff, like in conectiva
- fix deps

* Wed Jul 20 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-2mdk
- fix deps

* Tue Jul 19 2005 Oden Eriksson <oeriksson@mandriva.com> 0.0.5-1mdk
- initial Mandriva package (PLD import)

