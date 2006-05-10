Summary:	Web Services Description Language Toolkit for Java
Name:		wsdl4j
Version:	1.5.1
Release:	0.1
License:	IBM Common Public License
Group:		Applications/Text
URL:		http://sourceforge.net/projects/wsdl4j
Source0:	%{name}-%{version}-src.tar.gz
# Source0-md5:	ba2b623dadab131fff061410e8047eb7
##cvs -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j login
##cvs -z3 -d:pserver:anonymous@cvs.sourceforge.net:/cvsroot/wsdl4j export -r wsdl4j-1_5_1 wsdl4j
BuildRequires:	jakarta-ant
BuildRequires:	jdk
BuildRequires:	junit
Requires:	java
Requires:	jaxp_parser_impl
BuildArch:	noarch
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
The Web Services Description Language for Java Toolkit (WSDL4J) allows
the creation, representation, and manipulation of WSDL documents
describing services. This codebase will eventually serve as a
reference implementation of the standard created by JSR110.

%package javadoc
Summary:	Javadoc for %{name}
Group:		Documentation

%description javadoc
Javadoc for %{name}.

%prep
%setup -q

%build
export OPT_JAR_LIST="ant/ant-junit junit"
[ -z "$JAVA_HOME" ] && export JAVA_HOME=%{_jvmdir}/java
#ant -Dbuild.compiler=modern compile
#ant -Dbuild.compiler=modern javadocs
ant -Dbuild.compiler=modern compile test javadocs

%install
rm -rf $RPM_BUILD_ROOT

# jars
install -d $RPM_BUILD_ROOT%{_javadir}

for jar in %{name}.jar qname.jar ; do
	vjar=$(echo $jar | sed s+.jar+-%{version}.jar+g)
	install -m 644 build/lib/$jar $RPM_BUILD_ROOT%{_javadir}/$vjar
	ln -fs $vjar $RPM_BUILD_ROOT%{_javadir}$jar
done

# javadoc
install -d $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}
cp -pr build/javadocs/* $RPM_BUILD_ROOT%{_javadocdir}/%{name}-%{version}/

%clean
rm -rf $RPM_BUILD_ROOT

%post javadoc
rm -f %{_javadocdir}/%{name}
ln -s %{name}-%{version} %{_javadocdir}/%{name}

%postun javadoc
if [ "$1" = "0" ]; then
	rm -f %{_javadocdir}/%{name}
fi

%files
%defattr(644,root,root,755)
%doc license.html
%{_javadir}/*

%files javadoc
%defattr(644,root,root,755)
%{_javadocdir}/%{name}-%{version}
