#
# Conditional build:
%bcond_without	gui	# Qt4-based GUI
#
Summary:	Tool for static C/C++ code analysis
Summary(pl.UTF-8):	Narzędzie do statycznej analizy kodu w C/C++
Name:		cppcheck
Version:	1.51
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/cppcheck/%{name}-%{version}.tar.bz2
# Source0-md5:	8349ab90472801b9d377cfabf846ca28
Patch0:		%{name}-gui-paths.patch
URL:		http://cppcheck.sourceforge.net/
BuildRequires:	cmake
BuildRequires:	docbook-style-xsl
BuildRequires:	docbook-dtd45-xml
BuildRequires:	libstdc++-devel
BuildRequires:	libxslt-progs
BuildRequires:	pcre-devel
BuildRequires:	rpmbuild(macros) >= 1.603
BuildRequires:	sed >= 4.0
BuildRequires:	tinyxml-devel
%if %{with gui}
BuildRequires:	QtGui-devel >= 4
BuildRequires:	QtHelp-devel >= 4
BuildRequires:	qt4-build >= 4
BuildRequires:	qt4-linguist >= 4
BuildRequires:	qt4-qmake >= 4
%endif
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

%package gui
Summary:	Qt4-based GUI for cppcheck
Summary(pl.UTF-8):	Oparty na Qt4 graficzny interfejs użytkownika do cppcheck
Group:		X11/Applications
Requires:	%{name} = %{version}-%{release}

%description gui
Qt4-based GUI for cppcheck.

%description gui -l pl.UTF-8
Oparty na Qt4 graficzny interfejs użytkownika do cppcheck.

%prep
%setup -q
%patch0 -p1

%{__sed} -i -e 's,-I[^ ]*/externals,,g' lib/lib.pri

%build
%{__make} all man \
	CXX="%{__cxx}" \
	CXXFLAGS="%{rpmcxxflags} -DNDEBUG -DHAVE_RULES -DTIXML_USE_STL -Wall" \
	INCLUDE_FOR_CLI="-Ilib" \
	INCLUDE_FOR_TEST="-Ilib -Icli" \
	LDFLAGS="%{rpmldflags} -lpcre" \
	TINYXML="%{_libdir}/libtinyxml.so" \
	DB2MAN=%{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl

%if %{with gui}
cd gui
qmake-qt4 \
	QMAKE_CXX="%{__cxx}" \
	QMAKE_CXXFLAGS_RELEASE="%{rpmcxxflags}" \
	QMAKE_LFLAGS_RELEASE="%{rpmldflags}"
%{__make}
lrelease-qt4 cppcheck_*.ts
# compiled version not used yet (code refers to manual.html at sf.net)
#cd help
#%{_libdir}/qt4/bin/qcollectiongenerator online-help.qhcp -o online-help.qhc
%endif

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	TINYXML="%{_libdir}/libtinyxml.so" 

install -Dp cppcheck.1 $RPM_BUILD_ROOT%{_mandir}/man1/cppcheck.1

%if %{with gui}
install -d $RPM_BUILD_ROOT{%{_bindir},%{_datadir}/cppcheck-gui}
install gui/cppcheck-gui $RPM_BUILD_ROOT%{_bindir}
install -p gui/cppcheck_*.qm $RPM_BUILD_ROOT%{_datadir}/cppcheck-gui
%{__make} -C gui install \
	DESTDIR=$RPM_BUILD_ROOT
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS Changelog readme.txt
%attr(755,root,root) %{_bindir}/cppcheck
%{_mandir}/man1/cppcheck.1*

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%doc readme_gui.txt
%attr(755,root,root) %{_bindir}/cppcheck-gui
%dir %{_datadir}/cppcheck-gui
%lang(de) %{_datadir}/cppcheck-gui/cppcheck_de.qm
%{_datadir}/cppcheck-gui/cppcheck_en.qm
%lang(es) %{_datadir}/cppcheck-gui/cppcheck_es.qm
%lang(fi) %{_datadir}/cppcheck-gui/cppcheck_fi.qm
%lang(fr) %{_datadir}/cppcheck-gui/cppcheck_fr.qm
%lang(ja) %{_datadir}/cppcheck-gui/cppcheck_ja.qm
%lang(nl) %{_datadir}/cppcheck-gui/cppcheck_nl.qm
%lang(pl) %{_datadir}/cppcheck-gui/cppcheck_pl.qm
%lang(ru) %{_datadir}/cppcheck-gui/cppcheck_ru.qm
%lang(sr) %{_datadir}/cppcheck-gui/cppcheck_sr.qm
%lang(sv) %{_datadir}/cppcheck-gui/cppcheck_sv.qm
%endif
