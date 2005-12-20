%define 	zope_subname	zwiki
Summary:	Zope product which allows you to build wiki webs in Zope
Summary(pl):	Produkt Zope umo¿liwiaj±cy budowanie stron WWW typu wiki
Name:		Zope3-%{zope_subname}
Version:	3.0.0
Release:	1
License:	GPL
Group:		Development/Tools
Source0:	http://www.zope.org/Products/Zope3-Packages/zwiki/%{version}/zwiki-%{version}.tgz
# Source0-md5:	7a469eb4c313c40c89a4e0a47da27e8e
URL:		http://www.zope.org/DevHome/Wikis/DevSite/Projects/ComponentArchitecture/ZwikiForZope3
BuildRequires:	python
Requires(post,postun):	/usr/sbin/installzope3package
%pyrequires_eq	python-modules
Requires:	Zope3
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define         zope_libdir             /usr/lib/zope3
%define         zope_pyscriptdir        /usr/share/zope3/lib/python

%description
ZWiki is a Zope product which allows you to build wiki webs in Zope.

%description -l pl
ZWiki to produkt Zope umo¿liwiaj±cy budowanie stron WWW typu wiki.

%prep
%setup -q -n zwiki-%{version}

%build
./configure \
	--with-python=%{_bindir}/python
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT%{_sysconfdir}/zope3
install -d $RPM_BUILD_ROOT%{_var}/spool/%{name}/{tmp,new,cur}

python install.py install \
        --root="$RPM_BUILD_ROOT" \
        --install-purelib="%{zope_pyscriptdir}"

mv $RPM_BUILD_ROOT%{_prefix}/zopeskel $RPM_BUILD_ROOT%{_sysconfdir}/zope3

%py_comp $RPM_BUILD_ROOT%{zope_pyscriptdir}
%py_ocomp $RPM_BUILD_ROOT%{zope_pyscriptdir}
%py_postclean

ln -s %{_var}/spool/%{name} $RPM_BUILD_ROOT%{zope_pyscriptdir}/%{zope_subname}/mail-queue

%clean
rm -rf $RPM_BUILD_ROOT

%post
%{_sbindir}/installzope3package %{zope_pyscriptdir}/%{zope_subname} %{zope_subname}
if [ -f /var/lock/subsys/zope3 ]; then
	/etc/rc.d/init.d/zope3 restart >&2
fi

%postun
if [ "$1" = "0" ]; then
	%{_sbindir}/installzope3package -d %{zope_subname}
	if [ -f /var/lock/subsys/zope ]; then
		/etc/rc.d/init.d/zope restart >&2
	fi
fi

%files
%defattr(644,root,root,755)
%doc zwiki/*.txt
%{zope_pyscriptdir}
%{_sysconfdir}/zope3/zopeskel%{_sysconfdir}/package-includes/*.zcml
%attr(770,zope,zope) %{_var}/spool/%{name}
