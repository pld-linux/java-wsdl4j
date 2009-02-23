%bcond_without  javadoc         # don't build javadoc

%include	/usr/lib/rpm/macros.java
Summary:	Web Services Description Language Toolkit for Java
Summary(pl.UTF-8):	Język opisu usług WWW dla Javy
Name:		wsdl4j
Version:	1.5.1
Release:	1
License:	IBM Common Public License
Group:		Applications/Text
##cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j login
##cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j export -r wsdl4j-1_5_1 wsdl4j
Source0:	%{name}-%{version}-src.tar.gz
# Source0-md5:	ba2b623dadab131fff061410e8047eb7
URL:		http://sourceforge.net/projects/wsdl4j/
BuildRequires:	ant
BuildRequires:	ant-junit
BuildRequires:	java-gcj-compat-devel
BuildRequires:	jpackage-utils
BuildRequires:	junit
BuildRequires:	rpm-javaprov
BuildRequires:	rpmbuild(macros) >= 1.300
Requires:	jaxp_parser_impl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows
the creation, representation, and manipulation of WSDL documents
describing services. This codebase will eventually serve as a
reference implementation of the standard created by JSR110.

%description -l pl.UTF-8
Pakiet WSDL4J (Web Services Description Language for Java - język
opisu usług WWW dla Javy) pozwala na tworzenie, reprezentowanie i
obróbkę dokumentów WSDL opisujących usługi. Ta podstawa kodu może
służyć za wzorcową implementację standardu stworzonego przez JSR110.

%package javadoc
Summary:	Javadoc for %{name}
Summary(pl.UTF-8):	Dokumentacja javadoc dla pakietu %{name}
Group:		Documentation
Requires:	jpackage-utils

%description javadoc
Javadoc for %{name}.

%description javadoc -l pl.UTF-8
Dokumentacja javadoc dla pakietu %{name}.

%prep
%setup -q

%build
required_jars="junit"
CLASSPATH=$(build-classpath $required_jars)
export CLASSPATH

%ant -Dbuild.compiler=extJavac compile test

%if %{with javadoc}
export SHELL=/bin/sh
%ant javadocs
%endif

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}
cp -a build/lib/qname.jar $RPM_BUILD_ROOT%{_javadir}/qname-%{version}.jar
cp -a build/lib/wsdl4j.jar $RPM_BUILD_ROOT%{_javadir}/wsdl4j-%{version}.jar
ln -s qname-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/qname.jar
ln -s wsdl4j-%{version}.jar $RPM_BUILD_ROOT%{_javadir}/wsdl4j.jar

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -a build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
ln -s %{name}-%{version} $RPM_BUILD_ROOT%{_javadocdir}/%{name} # ghost symlink

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
ln -sf %{name}-%{version} %{_javadocdir}/%{name}

%files
%defattr(644,root,root,755)
%doc license.html
%{_javadir}/*.jar

%if %{with javadoc}
%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
%ghost %{_javadocdir}/%{name}
%endif
