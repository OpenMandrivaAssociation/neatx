# .spec file to package NeatX in RPM.
# Author: Alexander Todorov <alexx.todorov@no_spam.gmail.com>

%{!?python_sitelib: %global python_sitelib %(%{__python} -c "from distutils.sysconfig import get_python_lib; print get_python_lib()")}
%global nx_homedir /home/.nxhome

Summary: An Open Source NX server
Name: neatx
Version: 0.3.1
#Release: 1%{?dist}
Release: 4
Source0: %{name}-%{version}.tar.gz
License: GPLv2
URL: http://code.google.com/p/neatx/
Group: Networking/Remote access

BuildRequires: autoconf
BuildRequires: automake
BuildRequires: gcc
BuildRequires: make
BuildRequires: python-devel
BuildRequires: python-docutils

Requires: openssh
Requires: python-pexpect
Requires: pkgconfig(pygobject-2.0)
Requires: pygtk2 >= 2.13
Requires: python >= 2.4
Requires: python-simplejson
#Requires: nc
Requires: nxagent
Requires: xauth
Requires: xrdb
Requires: x11-font-misc
Requires(pre): shadow-utils
Requires(post): coreutils

%description
Neatx is an Open Source NX server, similar to the commercial NX server from 
NoMachine.

%prep
%setup -q

%build
#./autogen.sh
%configure2_5x
%make

%install
%makeinstall_std
# provide a meaningfull config file
%__install -D -m 644 %{buildroot}/%_docdir/%{name}/neatx.conf.example %{buildroot}/etc/neatx.conf

%pre
# create the nx user account
getent group nx >/dev/null || groupadd -r nx
getent passwd nx >/dev/null || \
       useradd -r -g nx -m -d %nx_homedir -s %_libdir/%{name}/nxserver-login-wrapper \
      -c "System account for the %{name} package" nx
chown -R nx: %nx_homedir
exit 0

%post
if [ $1 -eq 1 ]; then
    # install authorized keys
    %__install -d -m 700 -o nx -g nx %nx_homedir/.ssh/
    %__install -D -m 600 -o nx -g nx %_datadir/%{name}/authorized_keys.nomachine %nx_homedir/.ssh/authorized_keys
fi

%files
%defattr(-,root,root)
%config(noreplace) /etc/neatx.conf
%_libdir/%{name}
%python_sitelib/%{name}/*
%doc %_docdir/%{name}
%_datadir/%{name}
%_var/lib/%{name}

# not sure how to handle these. rpmlint doesn't report errors on -debuginfo package
#/usr/lib/debug/.build-id/bb/3398f400d7a44a6e0b8842c051dc378215bae8
#/usr/lib/debug/.build-id/bb/3398f400d7a44a6e0b8842c051dc378215bae8.debug
#/usr/lib/debug/usr/local/lib/neatx/fdcopy.debug
#/usr/src/debug/neatx-0.1/src/fdcopy.c


