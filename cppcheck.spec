#
# Conditional build:
%bcond_without	gui	# Qt4-based GUI
#
Summary:	Tool for static C/C++ code analysis
Summary(pl.UTF-8):	Narzędzie do statycznej analizy kodu w C/C++
Name:		cppcheck
Version:	1.72
Release:	1
License:	GPL v3+
Group:		Development/Tools
Source0:	http://downloads.sourceforge.net/cppcheck/%{name}-%{version}.tar.bz2
# Source0-md5:	2bd36f91ae0191ef5273bb7f6dc0d72e
Patch0:		%{name}-gui-paths.patch
Patch1:		%{name}-translations.patch
URL:		http://cppcheck.sourceforge.net/
BuildRequires:	cmake >= 2.8
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
%patch1 -p1

%{__sed} -i -e 's,-I[^ ]*/externals,,g' lib/lib.pri

%build
%{__make} DB2MAN=%{_datadir}/sgml/docbook/xsl-stylesheets/manpages/docbook.xsl man

mkdir build
cd build
%{cmake} \
	../ \
	-DBUILD_SHARED_LIBS:BOOL=OFF \
	-DBUILD_GUI:BOOL=%{?with_gui:ON}%{!?with_gui:OFF} \
	-DHAVE_RULES:BOOL=ON


%{__make}

%install
rm -rf $RPM_BUILD_ROOT
cd build

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT

install -Dp ../cppcheck.1 $RPM_BUILD_ROOT%{_mandir}/man1/cppcheck.1

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS readme.txt
%attr(755,root,root) %{_bindir}/cppcheck
%{_mandir}/man1/cppcheck.1*

%if %{with gui}
%files gui
%defattr(644,root,root,755)
%attr(755,root,root) %{_bindir}/cppcheck-gui
%dir %{_datadir}/CppCheck
%{_datadir}/CppCheck/*.cfg
%dir %{_datadir}/CppCheck/lang
%lang(de) %{_datadir}/CppCheck/lang/cppcheck_de.qm
%lang(es) %{_datadir}/CppCheck/lang/cppcheck_es.qm
%lang(fi) %{_datadir}/CppCheck/lang/cppcheck_fi.qm
%lang(fr) %{_datadir}/CppCheck/lang/cppcheck_fr.qm
%lang(it) %{_datadir}/CppCheck/lang/cppcheck_it.qm
%lang(ja) %{_datadir}/CppCheck/lang/cppcheck_ja.qm
%lang(ko) %{_datadir}/CppCheck/lang/cppcheck_ko.qm
%lang(nl) %{_datadir}/CppCheck/lang/cppcheck_nl.qm
%lang(ru) %{_datadir}/CppCheck/lang/cppcheck_ru.qm
%lang(sr) %{_datadir}/CppCheck/lang/cppcheck_sr.qm
%lang(sv) %{_datadir}/CppCheck/lang/cppcheck_sv.qm
%lang(zh_CN) %{_datadir}/CppCheck/lang/cppcheck_zh_CN.qm
%endif
