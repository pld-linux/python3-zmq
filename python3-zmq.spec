#
# Conditional build:
%bcond_without	doc	# Sphinx documentation
%bcond_with	tests	# unit tests (using network? and finally hang)

%define		module		pyzmq
%define		zeromq_ver	4.3.2
Summary:	Py0MQ - 0MQ bindings for Python 3
Summary(en.UTF-8):	Py0MQ - ØMQ bindings for Python 3
Summary(pl.UTF-8):	Py0MQ - wiązania biblioteki ØMQ dla Pythona 3
Name:		python3-zmq
Version:	26.4.0
Release:	1
License:	BSD
Group:		Development/Languages/Python
#Source0Download: https://github.com/zeromq/pyzmq/releases
Source0:	https://github.com/zeromq/pyzmq/archive/v%{version}/%{name}-%{version}.tar.gz
# Source0-md5:	1262271b8ede1a6f8922c35b11dd27cd
URL:		http://github.com/zeromq/pyzmq
BuildRequires:	cmake >= 3.14
BuildRequires:	ninja
BuildRequires:	python3-Cython >= 3.0.0
BuildRequires:	python3-build
BuildRequires:	python3-devel >= 1:3.8
BuildRequires:	python3-installer
BuildRequires:	python3-packaging
BuildRequires:	python3-scikit-build-core >= 0.10
%if %{with tests}
BuildRequires:	python3-gevent
BuildRequires:	python3-pytest
BuildRequires:	python3-tornado
%endif
BuildRequires:	rpm-build >= 4.6
BuildRequires:	rpm-pythonprov
BuildRequires:	rpmbuild(macros) >= 2.044
BuildRequires:	zeromq-devel >= %{zeromq_ver}
%if %{with doc}
BuildRequires:	python3-Cython >= 3.0.0
BuildRequires:	python3-enum-tools
BuildRequires:	python3-gevent
BuildRequires:	python3-linkify-it-py
BuildRequires:	python3-pygments >= 2.4.2
BuildRequires:	python3-sphinx-toolbox
BuildRequires:	sphinx-pdg-3 >= 1.7
%endif
Requires:	python3-modules >= 1:3.8
Requires:	python3-tornado
Requires:	zeromq >= %{zeromq_ver}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
0MQ bindings for Python 3.

%description -l en.UTF-8
ØMQ bindings for Python 3.

%description -l pl.UTF-8
Wiązania biblioteki ØMQ dla Pythona 3.

%package devel
Summary:	Header files for Py0MQ (Python 3 version)
Summary(pl.UTF-8):	Pliki nagłowkowe dla Py0MQ (wersja dla Pythona 3)
Group:		Development/Languages/Python
Requires:	%{name} = %{version}-%{release}

%description devel
Header files for Py0MQ (Python 3 version).

%description devel -l pl.UTF-8
Pliki nagłowkowe dla Py0MQ (wersja dla Pythona 3).

%package apidocs
Summary:	API documentation for Py0MQ module
Summary(pl.UTF-8):	Dokumentacja API modułu Py0MQ
Group:		Documentation
BuildArch:	noarch

%description apidocs
API documentation for Py0MQ module.

%description apidocs -l pl.UTF-8
Dokumentacja API modułu Py0MQ.

%prep
%setup -qn %{module}-%{version}

%build
%py3_build_pyproject

%if %{with doc}
%__unzip -qo build-3/*.whl -d build-3/build-path
PYTHONPATH=$(pwd)/build-3/build-path \
%{__make} -C docs html \
	SPHINXBUILD=sphinx-build-3
%endif

%install
rm -rf $RPM_BUILD_ROOT

%py3_install_pyproject

%{__rm} -r $RPM_BUILD_ROOT%{py3_sitedir}/zmq/tests

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc AUTHORS.md LICENSE.md README.md
%dir %{py3_sitedir}/zmq
%{py3_sitedir}/zmq/*.py
%{py3_sitedir}/zmq/*.pyi
%{py3_sitedir}/zmq/*.pxd
%{py3_sitedir}/zmq/__pycache__
%{py3_sitedir}/zmq/py.typed
%dir %{py3_sitedir}/zmq/auth
%{py3_sitedir}/zmq/auth/*.py
%dir %{py3_sitedir}/zmq/backend
%{py3_sitedir}/zmq/backend/*.py
%{py3_sitedir}/zmq/backend/*.pyi
%dir %{py3_sitedir}/zmq/backend/cffi
%{py3_sitedir}/zmq/backend/cffi/*.[ch]
%{py3_sitedir}/zmq/backend/cffi/*.py
%dir %{py3_sitedir}/zmq/backend/cython
%attr(755,root,root) %{py3_sitedir}/zmq/backend/cython/*.so
%{py3_sitedir}/zmq/backend/cython/*.py
%{py3_sitedir}/zmq/backend/cython/*.pxd
%{py3_sitedir}/zmq/backend/cython/*.pxi
%dir %{py3_sitedir}/zmq/devices
%{py3_sitedir}/zmq/devices/*.py
%dir %{py3_sitedir}/zmq/eventloop
%{py3_sitedir}/zmq/eventloop/*.py
%dir %{py3_sitedir}/zmq/green
%{py3_sitedir}/zmq/green/*.py
%dir %{py3_sitedir}/zmq/green/eventloop
%{py3_sitedir}/zmq/green/eventloop/*.py
%dir %{py3_sitedir}/zmq/log
%{py3_sitedir}/zmq/log/*.py
%dir %{py3_sitedir}/zmq/ssh
%{py3_sitedir}/zmq/ssh/*.py
%dir %{py3_sitedir}/zmq/sugar
%{py3_sitedir}/zmq/sugar/*.py
%{py3_sitedir}/zmq/sugar/*.pyi
%dir %{py3_sitedir}/zmq/utils
%{py3_sitedir}/zmq/utils/*.py
%{py3_sitedir}/zmq/*/__pycache__
%{py3_sitedir}/zmq/*/*/__pycache__
%{py3_sitedir}/pyzmq-%{version}.dist-info

%files devel
%defattr(644,root,root,755)
%{py3_sitedir}/zmq/utils/*.h

%if %{with doc}
%files apidocs
%defattr(644,root,root,755)
%doc docs/build/html/{_static,api,*.html,*.js}
%endif
