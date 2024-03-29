rsyphon
======

Proper documentation is in /usr/share/doc/rsyphon-*


Building and/or Installing rsyphon from Source
--------------------------------------------------------------------------------
Rsyphon should build and operate on most Linux distributions. Supported distributions include Debian Lenny-Jessie, SUSE Linux Enterprise 10, 11, RHEL/CentOS 5-7.

If you must build rsyphon yourself:

Before you can build rsyphon, you'll need to do the following:

Install the appropriate build dependencies for your distribution.

## Ubuntu 12.04, 12.10: ##
    apt-get install build-essential rpm flex libtool uuid-dev gettext python-dev libpam-dev libreadline-dev binutils-dev libssl-dev libz-dev dos2unix docbook-utils libncurses-dev

## RHEL6, CentOS6, and friends: ##
    yum install rpm-build patch wget flex bc docbook-utils dos2unix device-mapper-devel gperf pam-devel quilt lzop glib2-devel PyXML glibc-static xz e2fsprogs-devel libtool libuuid-devel gettext-devel python-devel readline-devel binutils-devel openssl-devel

## Debian: ##
    apt-get install build-essential flex libtool uuid-dev gettext python-dev libssl-dev zlib1g-dev libgusb-dev libglib2.0-dev gperf

Run './configure'

Run 'make show_targets' to see a list of make targets from which you can choose.

Run 'make' to build, 'sudo make install' to install the resulting build. RPM and Debian packages can also be built via 'make rpm' or 'make deb'.
