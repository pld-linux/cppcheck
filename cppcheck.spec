#
# Conditional build:
%bcond_without	gui	# Qt6-based GUI
#
Summary:	Tool for static C/C++ code analysis
Summary(pl.UTF-8):	Narzędzie do statycznej analizy kodu w C/C++
Name:		cppcheck
Version:	2.20.0
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	https://downloads.sourceforge.net/cppcheck/%{name}-%{version}.tar.bz2
# Source0-md5:	052140ea9d97107644440ec669a646b7
Patch0:		%{name}-translations.patch
URL:		http://cppcheck.sourceforge.io/
BuildRequires:	boost-devel
BuildRequires:	cmake >= 3.22
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd45-xml
BuildRequires:	libstdc++-devel >= 6:5.1
BuildRequires:	libxslt-progs
BuildRequires:	pcre-devel
BuildRequires:	python3 >= 1:3.7
BuildRequires:	python3-modules >= 1:3.7
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpmbuild(macros) >= 1.605
BuildRequires:	sed >= 4.0
BuildRequires:	tinyxml2-devel
%if %{with gui}
BuildRequires:	Qt6Charts-devel
BuildRequires:	Qt6Core-devel
BuildRequires:	Qt6Gui-devel
BuildRequires:	Qt6Help-devel
BuildRequires:	Qt6Network-devel
BuildRequires:	Qt6PrintSupport-devel
BuildRequires:	Qt6Widgets-devel
BuildRequires:	qt6-build
BuildRequires:	qt6-linguist
%endif
Requires:	%{name}-common = %{version}-%{release}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
cppcheck is an analysis tool for C/C++ code. Unlike C/C++ compilers
and many other analysis tools, it doesn't detect syntax errors.
cppcheck only detects the types of bugs that the compilers normally
fail to detect. The goal is no false positives.

%description -l pl.UTF-8
cppcheck to narzędzie do analizy kodu w C/C++. W przeciwieństwie do
kompilatorów i innych narzędzi do analizy, nie wykrywa błędów
składni. Wykrywa tylko te rodzaje błędów, których zwykle nie wykrywają
kompilatory. Celem jest brak fałszywych alarmów.

%package common
Summary:	Common files for command line and GUI cppcheck
Summary(pl.UTF-8):	Pliki wspólne dla cppcheck linii poleceń oraz interfejsu graficznego
Group:		X11/Applications
BuildArch:	noarch

%description common
Common files for command line and GUI cppcheck.

%description common -l pl.UTF-8
Pliki wspólne dla cppcheck linii poleceń oraz interfejsu graficznego.

%package gui
Summary:	Qt6-based GUI for cppcheck
Summary(pl.UTF-8):	Oparty na Qt6 graficzny interfejs użytkownika do cppcheck
Group:		X11/Applications
Requires(post,postun):	desktop-file-utils
Requires(post,postun):	gtk-update-icon-cache
Requires:	%{name}-common = %{version}-%{release}
Requires:	hicolor-icon-theme

%description gui
Qt6-based GUI for cppcheck.

%description gui -l pl.UTF-8
Oparty na Qt6 graficzny interfejs użytkownika do cppcheck.

%prep
%setup -q
%patch -P0 -p1

%{__sed} -i -e '1 s,#!.*env python.*,#!%{__python3},' htmlreport/cppcheck-htmlreport

%build
%{__make} DB2MAN=%{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl man

%{cmake} -B build \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_GUI:BOOL=%{?with_gui:ON}%{!?with_gui:OFF} \
	-DWITH_QCHART:BOOL=%{?with_gui:ON}%{!?with_gui:OFF} \
	-DHAVE_RULES:BOOL=ON \
	-DUSE_BOOST:BOOL=ON \
	-DUSE_BUNDLED_TINYXML2:BOOL=OFF \

%{__make} -C build

%install
rm -rf $RPM_BUILD_ROOT

%{__make} -C build install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp cppcheck.1 $RPM_BUILD_ROOT%{_mandir}/man1/cppcheck.1

%clean
rm -rf $RPM_BUILD_ROOT

%post gui
%update_desktop_database_post
%update_icon_cache hicolor

%postun gui
%update_desktop_database_postun
%update_icon_cache hicolor

%files
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cppcheck
%attr(755,root,root) %{_bindir}/cppcheck-htmlreport
%{_mandir}/man1/cppcheck.1*

%files common
%doc AUTHORS TUNING.md readme.md releasenotes.txt
%lang(ja) %doc readmeja.md
%dir %{_datadir}/Cppcheck
%dir %{_datadir}/Cppcheck/addons
%{_datadir}/Cppcheck/addons/*.json
%{_datadir}/Cppcheck/addons/*.py
%dir %{_datadir}/Cppcheck/cfg
%{_datadir}/Cppcheck/cfg/*.cfg
%dir %{_datadir}/Cppcheck/platforms
%{_datadir}/Cppcheck/platforms/*.xml

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cppcheck-gui
%dir %{_datadir}/Cppcheck/lang
%lang(de) %{_datadir}/Cppcheck/lang/cppcheck_de.qm
%lang(es) %{_datadir}/Cppcheck/lang/cppcheck_es.qm
%lang(fi) %{_datadir}/Cppcheck/lang/cppcheck_fi.qm
%lang(fr) %{_datadir}/Cppcheck/lang/cppcheck_fr.qm
%lang(it) %{_datadir}/Cppcheck/lang/cppcheck_it.qm
%lang(ja) %{_datadir}/Cppcheck/lang/cppcheck_ja.qm
%lang(ka) %{_datadir}/Cppcheck/lang/cppcheck_ka.qm
%lang(ko) %{_datadir}/Cppcheck/lang/cppcheck_ko.qm
%lang(nl) %{_datadir}/Cppcheck/lang/cppcheck_nl.qm
%lang(ru) %{_datadir}/Cppcheck/lang/cppcheck_ru.qm
%lang(sr) %{_datadir}/Cppcheck/lang/cppcheck_sr.qm
%lang(sv) %{_datadir}/Cppcheck/lang/cppcheck_sv.qm
%lang(zh_CN) %{_datadir}/Cppcheck/lang/cppcheck_zh_CN.qm
%lang(zh_TW) %{_datadir}/Cppcheck/lang/cppcheck_zh_TW.qm
%{_desktopdir}/cppcheck-gui.desktop
%{_iconsdir}/hicolor/64x64/apps/cppcheck-gui.png
%{_iconsdir}/hicolor/scalable/apps/cppcheck-gui.svg
%endif
