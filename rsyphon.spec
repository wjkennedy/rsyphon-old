#
# $Id$
#
%define name   rsyphon
#
# "ver" below, is automatically set to the current version (as defined 
# by the VERSION file) when "make source_tarball" is executed.
# Therefore, it can be set to any three digit number here.
#
%define ver    0.0.0
# Set rel to 1 when is is a final release otherwise, set it to a 0.x number
# This is convenient when final release need to upgrade "beta" releases.
%define rel    0.16%{?dist}
%define packager William Kennedy <william@a9group.net>
#define prefix /usr
%define _build_all 1
%define _boot_flavor standard
# Set this to 1 to build only the boot rpm
# it can also be done in the .rpmmacros file
#define _build_only_boot 1
%{?_build_only_boot:%{expand: %%define _build_all 0}}

%define _unpackaged_files_terminate_build 0

# prevent RPM from stripping files (eg. bittorrent binaries)
%define __spec_install_post /usr/lib/rpm/brp-compress
# prevent RPM files to be changed by prelink
%{?__prelink_undo_cmd:%undefine __prelink_undo_cmd}

%define is_suse %(test -f /etc/SuSE-release && echo 1 || echo 0)
%define is_ppc64 %([ "`uname -m`" = "ppc64" ] && echo 1 || echo 0)
%define is_ps3 %([ `grep PS3 /proc/cpuinfo >& /dev/null; echo $?` -eq 0 ] && echo 1 || echo 0) 

%if %is_ppc64
%define _build_arch ppc64
%endif

%if %is_ps3
%define _build_arch ppc64-ps3
%endif

%if %is_suse
%define python_xml python-xml
%else
%define python_xml PyXML
%endif

# Still use the correct lib even on fc-18+ where --target noarch sets %_libdir to /usr/lib even on x86_64 arch.
%define static_libcrypt_a /usr/lib/libcrypt.a
%if "%(arch)" == "x86_64"
%define static_libcrypt_a /usr/lib64/libcrypt.a
%endif

Summary: Software that automates Linux installs, software distribution, and production deployment.
Name: %name
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
Source0: http://download.sourceforge.net/rsyphon/%{name}-%{ver}.tar.bz2
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: A9 Platform Tools
BuildRequires: docbook-utils, dos2unix, flex, libtool, readline-devel, /usr/bin/wget, openssl-devel, gcc, gcc-c++, ncurses-devel, bc, rsync >= 2.4.6
BuildRequires: libuuid-devel, device-mapper-devel, gperf, binutils-devel, pam-devel, quilt
BuildRequires: lzop, glib2-devel >= 2.22.0
Requires: rsync >= 2.4.6, syslinux >= 1.48, libappconfig-perl, dosfstools, /usr/bin/perl
#AutoReqProv: no

%description
Rsyphon is software that automates Linux installs, software
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution,
configuration changes, and operating system updates to your network of
Linux machines. You can even update from one Linux release version to
another!It can also be used to ensure safe production deployments.
By saving your current production image before updating to your new
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back
to the last production image with a simple update command!Some
typical environments include: Internet server farms, database server
farms, high performance clusters, computer labs, and corporate desktop
environments.

%if %{_build_all}

%package server
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Requires: rsync >= 2.4.6, rsyphon-common = %{version}, perl-AppConfig, dosfstools, /sbin/chkconfig, perl, perl(XML::Simple) >= 2.14, python, mkisofs
#AutoReqProv: no

%description server
Rsyphon is software that automates Linux installs, software 
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The server package contains those files needed to run a Rsyphon
server.

%package flamethrower
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Requires: rsyphon-server = %{version}, /sbin/chkconfig, perl, flamethrower >= 0.1.6
#AutoReqProv: no

%description flamethrower
Rsyphon is software that automates Linux installs, software 
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The flamethrower package allows you to use the flamethrower utility to perform
installations over multicast.

%package common
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Requires: perl, systemconfigurator >= 2.2.11
#AutoReqProv: no

%description common
Rsyphon is software that automates Linux installs, software 
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!It can also be used to ensure safe production deployments.
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism. If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with rs_updateclient, even with Puppet.
Typical deployment scenarios include build and web farms, database server 
farms, high performance clusters, software development labs and Linux desktop
environments.

The common package contains files common to Rsyphon clients 
and servers.

%package client
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Requires: rsyphon-common = %{version}, systemconfigurator >= 2.2.11, perl-AppConfig, rsync >= 2.4.6, perl
#AutoReqProv: no

%description client
Rsyphon is software that automates Linux installs, software
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution,
configuration changes, and operating system updates to your network of
Linux machines. You can even update from one Linux release version to
another!It can also be used to ensure safe production deployments.
By saving your current production image before updating to your new
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back
to the last production image with a simple update command!Some
typical environments include: Internet server farms, database server
farms, high performance clusters, computer labs, and corporate desktop
environments.

The client package contains the files needed on a machine for it to
be imaged by a Rsyphon server.

%endif

%package %{_build_arch}boot-%{_boot_flavor}
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Obsoletes: rsyphon-%{_build_arch}boot
BuildRequires: python, python-devel, gettext
%if %is_ps3
BuildRequires: dtc
%endif
Requires: rsyphon-server >= %{version}
Requires: %{name}-initrd_template = %{version}
Provides: %{name}-boot-%{_boot_flavor} = %{version}
AutoReqProv: no

%description %{_build_arch}boot-%{_boot_flavor}
Rsyphon is software that automates Linux installs, software 
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution, 
configuration changes, and operating system updates to your network of 
Linux machines. You can even update from one Linux release version to 
another!It can also be used to ensure safe production deployments.  
By saving your current production image before updating to your new 
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back 
to the last production image with a simple update command!Some 
typical environments include: Internet server farms, database server 
farms, high performance clusters, computer labs, and corporate desktop
environments.

The %{_build_arch}boot package provides specific kernel, ramdisk, and fs utilities
to boot and install %{_build_arch} Linux machines during the Rsyphon autoinstall
process.

%package %{_build_arch}initrd_template
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
BuildRequires: python, python-devel, %{python_xml}, %{static_libcrypt_a}
Requires: %{name}-%{_build_arch}boot-%{_boot_flavor} = %{version}
Provides: %{name}-initrd_template = %{version}
AutoReqProv: no

%description %{_build_arch}initrd_template
Rsyphon is software that automates Linux installs, software
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution,
configuration changes, and operating system updates to your network of
Linux machines. You can even update from one Linux release version to
another!It can also be used to ensure safe production deployments.
By saving your current production image before updating to your new
production image, you have a highly reliable contingency mechanism.If
the new production enviroment is found to be flawed, simply roll-back
to the last production image with a simple update command!Some
typical environments include: Internet server farms, database server
farms, high performance clusters, computer labs, and corporate desktop
environments.

The %{_build_arch}initrd_template package provides initrd template files for creating custom
ramdisk that works with a specific kernel by using UYOK (Use Your Own Kernel).The custom
ramdisk can then be used to boot and install %{_build_arch} Linux machines during the
Rsyphon autoinstall process.

%package bittorrent
Summary: Software that automates Linux installs, software distribution, and production deployment.
Version: %ver
Release: %rel
License: GPL
Group: Applications/System
BuildRoot: /tmp/%{name}-%{ver}-root
BuildArch: noarch
Packager: %packager
URL: http://rsyphon.a9group.net/docs.htm
Distribution: System Installation Suite
Requires: rsyphon-server = %{version}, /sbin/chkconfig, perl, perl(Getopt::Long)
#AutoReqProv: no

%description bittorrent
Rsyphon is software that automates Linux installs, software
distribution, and production deployment.Rsyphon makes it easy to
do installs, software distribution, content or data distribution,
configuration changes, and operating system updates to your network of
Linux machines. You can even update from one Linux release version to
another!It can also be used to ensure safe production deployments and
rapid deployment of Disaster Recovery or scale-up.
By saving a production image before updating to your new production image,
you have a highly reliable contingency mechanism. If
the new production enviroment is found to be flawed, simply roll-back
to the last production image with a simple update command!Some
typical environments include: Internet server farms, database server
farms, high performance clusters, computer labs, and corporate desktop
environments.

The bittorrent package allows you to use the BitTorrent protocol to perform
installations.

%changelog

* Mon Sep 29 2014 William Kennedy <william@a9group.net> 0.1
- Fork from SystemImager 4.3
%prep

# Prepare source tree
%setup -q

# Add patches so it can build on non-debian systems.
%__cp rpm/*.patch initrd_source/patches/

# Download external sources
%{__make} %{?_smp_mflags} get_source

%build
cd $RPM_BUILD_DIR/%{name}-%{version}/

# Make sure we can fin system utils like mkfs.cramfs (when building as non-root)
export PATH=/sbin:/usr/sbin:$PATH

# Build against installed libs, not our system lib which may not be the same version.
export LD_FLAGS=-L$RPM_BUILD_DIR/%{name}-%{version}/initrd_source/build_dir/lib

# Make sure we build the docs
./configure RS_BUILD_DOCS=1

# Only build everything if on x86, this helps with PPC build issues
%if %{_build_all}
#%{__make} %{?_smp_mflags} all
%{__make} -j1 all

%else
%{__make} binaries

%endif

%install
cd $RPM_BUILD_DIR/%{name}-%{version}/

%if %{_build_all}

make install_server_all DESTDIR=$RPM_BUILD_ROOT PREFIX=%_prefix
make install_client_all DESTDIR=$RPM_BUILD_ROOT PREFIX=%_prefix
(cd doc/manual_source;%{__make} html)

%else

%{__make} install_binaries DESTDIR=$RPM_BUILD_ROOT PREFIX=%_prefix

%endif

# Some things that get duplicated because there are multiple calls to
# the make install_* phases.
find $RPM_BUILD_ROOT -name \*~ -exec rm -f '{}' \;

%clean
#__rm -rf $RPM_BUILD_DIR/%{name}-%{version}/
%__rm -rf $RPM_BUILD_ROOT

%if %{_build_all}

%pre server
# /etc/rsyphon/rsyncd.conf is now generated from stubs stored
# in /etc/rsyphon/rsync_stubs.if upgrading from an early
# version, we need to create stub files for all image entries
if [ -f %{_sysconfdir}/rsyphon/rsyncd.conf -a \
  ! -d %{_sysconfdir}/rsyphon/rsync_stubs ]; then
  echo "You appear to be upgrading from a pre-rsync stubs release."
  echo "%{_sysconfdir}/rsyphon/rsyncd.conf is now auto-generated from stub"
  echo "files stored in %{_sysconfdir}/rsyphon/rsync_stubs."
  echo "Backing up %{_sysconfdir}/rsyphon/rsyncd.conf to:"
  echo -n "  %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs... "
  mv %{_sysconfdir}/rsyphon/rsyncd.conf \
    %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs

  ## leave an extra copy around so the postinst knows to make stub files from it
  cp %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs \
    %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs.tmp
  echo "done."
fi  


%post server
# First we check for rsync service under xinetd and get rid of it
# also note the use of DURING_INSTALL, which is used to
# support using this package in Image building without affecting
# processes running on the parrent
if [[ -a %{_sysconfdir}/xinetd.d/rsync ]]; then
  mv %{_sysconfdir}/xinetd.d/rsync %{_sysconfdir}/xinetd.d/rsync.presis~
  `pidof xinetd > /dev/null`
  if [[ $? == 0 ]]; then
      if [ -z $DURING_INSTALL ]; then
          %{_sysconfdir}/init.d/xinetd restart
      fi
  fi
fi

# If we are upgrading from a pre-rsync-stubs release, the preinst script
# will have left behind a copy of the old rsyncd.conf file.we need to parse
# it and make stubs files for each image.

# This assumes that this file has been managed by rsyphon, and
# that there is nothing besides images entries that need to be carried
# forward.

in_image_section=0
current_image=""
if [ -f %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs.tmp ]; then
  echo "Migrating image entries from existing %{_sysconfdir}/rsyphon/rsyncd.conf to"
  echo "individual files in the %{_sysconfdir}/rsyphon/rsync_stubs/ directory..."
  while read line; do
	## Ignore all lines until we get to the image section
	if [ $in_image_section -eq 0 ]; then
	  echo $line | grep -q "^# only image entries below this line"
	  if [ $? -eq 0 ]; then
		in_image_section=1
	  fi
	else
	  echo $line | grep -q "^\[.*]$"
	  if [ $? -eq 0 ]; then
		current_image=$(echo $line | sed 's/^\[//' | sed 's/\]$//')
		echo -e "\tMigrating entry for $current_image"
		if [ -e "%{_sysconfdir}/rsyphon/rsync_stubs/40$current_image" ]; then
		  echo -e "\t%{_sysconfdir}/rsyphon/rsync_stubs/40$current_image already exists."
		  echo -e "\tI'm not going to overwrite it with the value from"
		  echo -e "\t%{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs.tmp"
		  current_image=""
		fi
	  fi
	  if [ "$current_image" != "" ]; then
		echo "$line" >> %{_sysconfdir}/rsyphon/rsync_stubs/40$current_image
	  fi
	fi
  done < %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs.tmp
  rm -f %{_sysconfdir}/rsyphon/rsyncd.conf-before-rsync-stubs.tmp
  echo "Migration complete - please make sure to migrate any configuration you have"
  echo "    made in %{_sysconfdir}/rsyphon/rsyncd.conf outside of the image section."
fi
## END make stubs from pre-stub %{_sysconfdir}/rsyphon/rsyncd.conf file

/usr/sbin/rs_mkrsyncd_conf

if [[ -a /usr/lib/lsb/install_initd ]]; then
  /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/rsyphon-server-rsyncd
  /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/rsyphon-server-netbootmond
  /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/rsyphon-server-monitord
fi

if [[ -a /sbin/chkconfig ]]; then
  /sbin/chkconfig --add rsyphon-server-rsyncd
  /sbin/chkconfig rsyphon-server-rsyncd off
  /sbin/chkconfig --add rsyphon-server-netbootmond
  /sbin/chkconfig rsyphon-server-netbootmond off
  /sbin/chkconfig --add rsyphon-server-monitord
  /sbin/chkconfig rsyphon-server-monitord off
fi

%preun server

if [ $1 = 0 ]; then
	%{_sysconfdir}/init.d/rsyphon-server-rsyncd stop
	%{_sysconfdir}/init.d/rsyphon-server-netbootmond stop
	%{_sysconfdir}/init.d/rsyphon-server-monitord stop

	if [[ -a /usr/lib/lsb/remove_initd ]]; then
	  /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/rsyphon-server-rsyncd
	  /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/rsyphon-server-netbootmond
	  /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/rsyphon-server-monitord
	fi

	if [[ -a /sbin/chkconfig ]]; then
	  /sbin/chkconfig --del rsyphon-server-rsyncd
	  /sbin/chkconfig --del rsyphon-server-netbootmond
	  /sbin/chkconfig --del rsyphon-server-monitord
	fi

	if [[ -a %{_sysconfdir}/xinetd.d/rsync.presis~ ]]; then
	  mv %{_sysconfdir}/xinetd.d/rsync.presis~ %{_sysconfdir}/xinetd.d/rsync
	  `pidof xinetd > /dev/null`
	  if [[ $? == 0 ]]; then
	      %{_sysconfdir}/init.d/xinetd restart
	  fi
	fi
else
	echo
	echo "WARNING: this seems to be an upgrade!"
	echo
	echo "Remember that this operation does not touch the following objects:"
	echo "- master, pre-install, post-install scripts"
	echo "- images"
	echo "- overrides"
	echo

	# This is an upgrade: restart the daemons.
	echo "Restarting services..."
	(%{_sysconfdir}/init.d/rsyphon-server-rsyncd status >/dev/null 2>&1 && \
		%{_sysconfdir}/init.d/rsyphon-server-rsyncd restart) || true
	(%{_sysconfdir}/init.d/rsyphon-server-netbootmond status >/dev/null 2>&1 && \
		%{_sysconfdir}/init.d/rsyphon-server-netbootmond restart) || true
	(%{_sysconfdir}/init.d/rsyphon-server-monitord status >/dev/null 2>&1 && \
		%{_sysconfdir}/init.d/rsyphon-server-monitord restart) || true
fi

%post flamethrower
if [[ -a /usr/lib/lsb/install_initd ]]; then
  /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/rsyphon-server-flamethrowerd
fi

if [[ -a /sbin/chkconfig ]]; then
  /sbin/chkconfig --add rsyphon-server-flamethrowerd
  /sbin/chkconfig rsyphon-server-flamethrowerd off
fi

%preun flamethrower
if [ $1 = 0 ]; then
	%{_sysconfdir}/init.d/rsyphon-server-flamethrowerd stop

	if [[ -a /usr/lib/lsb/remove_initd ]]; then
	  /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/rsyphon-server-flamethrowerd
	fi

	if [[ -a /sbin/chkconfig ]]; then
	  /sbin/chkconfig --del rsyphon-server-flamethrowerd
	fi
else
	# This is an upgrade: restart the daemon.
	(%{_sysconfdir}/init.d/rsyphon-server-flamethrowerd status >/dev/null 2>&1 && \
		%{_sysconfdir}/init.d/rsyphon-server-flamethrowerd restart) || true
fi

%post bittorrent
if [[ -a /usr/lib/lsb/install_initd ]]; then
  /usr/lib/lsb/install_initd %{_sysconfdir}/init.d/rsyphon-server-bittorrent
fi

if [[ -a /sbin/chkconfig ]]; then
  /sbin/chkconfig --add rsyphon-server-bittorrent
  /sbin/chkconfig rsyphon-server-bittorrent off
fi

%pre bittorrent
echo "checking for a tracker binary..."
BT_TRACKER_BIN=`(which bittorrent-tracker || which bttrack) 2>/dev/null`
if [ -z $BT_TRACKER_BIN ]; then
	echo "WARNING: couldn't find a valid tracker binary!"
	echo "--> Install the BitTorrent package (bittorrent for RH)."
	echo "--> For details, please see http://rsyphon.a9group.net/docs.htm"
else
	echo done
fi

echo "checking for a maketorrent binary..."
BT_MAKETORRENT_BIN=`(which maketorrent-console || which btmaketorrent) 2>/dev/null`
if [ -z $BT_MAKETORRENT_BIN ]; then
	echo "WARNING: couldn't find a valid maketorrent binary!"
	echo "--> Install the BitTorrent package (bittorrent for RH)."
	echo "--> For details, please see http://rsyphon.a9group.net/docs.htm"
else
	echo done
fi

echo "checking for a bittorrent binary..."
BT_BITTORRENT_BIN=`(which launchmany-console || which btlaunchmany) 2>/dev/null`
if [ -z $BT_BITTORRENT_BIN ]; then
	echo "WARNING: couldn't find a valid bittorrent binary!"
	echo "--> Install the BitTorrent package (bittorrent for RH)."
	echo "--> For details, please see http://rsyphon.a9group.net/docs.htm"
else
	echo done
fi

%preun bittorrent
if [ $1 = 0 ]; then
	%{_sysconfdir}/init.d/rsyphon-server-bittorrent stop

	if [[ -a /usr/lib/lsb/remove_initd ]]; then
	  /usr/lib/lsb/remove_initd %{_sysconfdir}/init.d/rsyphon-server-bittorrent
	fi

	if [[ -a /sbin/chkconfig ]]; then
	  /sbin/chkconfig --del rsyphon-server-bittorrent
	fi
else
	# This is an upgrade: restart the daemon.
	(%{_sysconfdir}/init.d/rsyphon-server-bittorrent status >/dev/null 2>&1 && \
		%{_sysconfdir}/init.d/rsyphon-server-bittorrent restart) || true
fi

%files common
%defattr(-, root, root)
%{_bindir}/rs_lsimage
%{_mandir}/man8/rs_lsimage*
%{_mandir}/man5/autoinstall*
%dir %{perl_vendorlib}/Rsyphon
%{perl_vendorlib}/Rsyphon/Common.pm
%{perl_vendorlib}/Rsyphon/Config.pm
%{perl_vendorlib}/Rsyphon/Options.pm
%{perl_vendorlib}/Rsyphon/UseYourOwnKernel.pm
%dir %{_sysconfdir}/rsyphon
%config %{_sysconfdir}/rsyphon/UYOK.modules_to_exclude
%config %{_sysconfdir}/rsyphon/UYOK.modules_to_include

%files server
%defattr(-, root, root)
%doc CHANGE.LOG COPYING CREDITS README TODO VERSION
%doc README.Rsyphon_DHCP_options
%doc doc/manual_source/html
# These should move to a files doc section, because they are missing if you don't do doc
# %doc doc/manual/rsyphon* doc/manual/html doc/manual/examples
%doc doc/man/autoinstall* doc/examples/local.cfg
%dir /var/lock/rsyphon
%dir /var/log/rsyphon
%dir %{_sharedstatedir}/rsyphon
%dir %{_sharedstatedir}/rsyphon/images
%dir %{_sharedstatedir}/rsyphon/scripts
%dir %{_sharedstatedir}/rsyphon/scripts/pre-install
%dir %{_sharedstatedir}/rsyphon/scripts/post-install
%dir %{_sharedstatedir}/rsyphon/overrides
%{_sharedstatedir}/rsyphon/overrides/README
%dir %{_datarootdir}/rsyphon
%dir %{_datarootdir}/rsyphon/icons
%config %{_sysconfdir}/rsyphon/pxelinux.cfg/*
%config %{_sysconfdir}/rsyphon/kboot.cfg/*
%config %{_sysconfdir}/rsyphon/autoinstallscript.template
%config(noreplace) %{_sysconfdir}/rsyphon/rsync_stubs/*
%config(noreplace) %{_sysconfdir}/rsyphon/systemimager.conf
%config(noreplace) %{_sysconfdir}/rsyphon/cluster.xml
%config(noreplace) %{_sysconfdir}/rsyphon/getimage.exclude
%{_sysconfdir}/init.d/rsyphon-server-rsyncd
%{_sysconfdir}/init.d/rsyphon-server-netboot*
%{_sysconfdir}/init.d/rsyphon-server-monitord
%{_sharedstatedir}/rsyphon/images/*
%{_sharedstatedir}/rsyphon/scripts/post-install/*
%{_sharedstatedir}/rsyphon/scripts/pre-install/*
%{_sbindir}/rs_addclients
%{_sbindir}/rs_cpimage
%{_sbindir}/rs_getimage
%{_sbindir}/rs_mk*
%{_sbindir}/rs_mvimage
%{_sbindir}/rs_netbootmond
%{_sbindir}/rs_pushupdate
%{_sbindir}/rs_pushinstall
%{_sbindir}/rs_rmimage
%{_sbindir}/rs_monitor
%{_sbindir}/rs_monitortk
%{_bindir}/rs_clusterconfig
%{_bindir}/rs_mk*
%{_bindir}/rs_psh
%{_bindir}/rs_pcp
%{_bindir}/rs_pushoverrides
%{perl_vendorlib}/Rsyphon/Server.pm
%{perl_vendorlib}/Rsyphon/Config.pm
%{perl_vendorlib}/Rsyphon/HostRange.pm
%{_prefix}/lib/rsyphon/confedit
%{perl_vendorlib}/BootMedia
%{perl_vendorlib}/BootGen
%{_mandir}/man5/rsyphon*
%{_mandir}/man8/rs_*
%{_datarootdir}/rsyphon/icons/*

%files client
%defattr(-, root, root)
%doc CHANGE.LOG COPYING CREDITS README VERSION
%config %{_sysconfdir}/rsyphon/updateclient.local.exclude
%config %{_sysconfdir}/rsyphon/client.conf
%{_sbindir}/rs_updateclient
%{_sbindir}/rs_prepareclient
%{_mandir}/man8/rs_updateclient*
%{_mandir}/man8/rs_prepareclient*
%{perl_vendorlib}/Rsyphon/Client.pm
%files flamethrower
%defattr(-, root, root)
%doc CHANGE.LOG COPYING CREDITS README VERSION
%dir /var/state/rsyphon/flamethrower
%config %{_sysconfdir}/rsyphon/flamethrower.conf
%{_sysconfdir}/init.d/rsyphon-server-flamethrowerd

%files bittorrent
%defattr(-, root, root)
%dir %{_sharedstatedir}/rsyphon/tarballs
%dir %{_sharedstatedir}/rsyphon/torrents
%config %{_sysconfdir}/rsyphon/bittorrent.conf
%{_sysconfdir}/init.d/rsyphon-server-bittorrent
%{_sbindir}/rs_installbtimage

%endif

%files %{_build_arch}boot-%{_boot_flavor}
%defattr(-, root, root)
%dir %{_datarootdir}/rsyphon/boot/%{_build_arch}
%dir %{_datarootdir}/rsyphon/boot/%{_build_arch}/standard
%{_datarootdir}/rsyphon/boot/%{_build_arch}/standard/config
%{_datarootdir}/rsyphon/boot/%{_build_arch}/standard/initrd.img
%{_datarootdir}/rsyphon/boot/%{_build_arch}/standard/kernel
#prefix/share/rsyphon/boot/%{_build_arch}/standard/boel_binaries.tar.gz

%files %{_build_arch}initrd_template
%defattr(-, root, root)
%dir %{_datarootdir}/rsyphon/boot/%{_build_arch}/standard/initrd_template
%{_datarootdir}/rsyphon/boot/%{_build_arch}/standard/initrd_template/*
