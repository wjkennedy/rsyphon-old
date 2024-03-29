#
#	$Id: bc.rul 3304 2005-12-16 04:35:34Z finley $
#   vi: set filetype=make:
#
# 	Perhaps there could be problems here in building multiple arch's from
# 	a single source directory, but we'll deal with that later...  Perhaps use
# 	$(TOPDIR)/tmp/$(ARCH)/ instead of just $(TOPDIR)/tmp/. -BEF-
#
#   2010.06.13  Brian Elliott Finley
#   * remove discover related bits

ISYS_BINARIES_DIR	= $(TOPDIR)/tmp/isys_binaries
ISYS_BINARIES_TARBALL 	= $(ISYS_BINARIES_DIR).tar.gz


PHONY += install_isys_binaries_tarball
install_isys_binaries_tarball:	$(ISYS_BINARIES_TARBALL)
	$(SI_INSTALL) -m 644 $(ISYS_BINARIES_TARBALL) $(BOOT_BIN_DEST)


PHONY += isys_binaries_tarball
isys_binaries_tarball:	$(ISYS_BINARIES_TARBALL)


$(ISYS_BINARIES_TARBALL):	\
				$(SRC_DIR)/modules_build-stamp
	#
	# Put binaries in the isys_binaries_tarball...
	#
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/bin
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/sbin
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/usr/bin
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/usr/sbin
	install -m 755 --strip $(TAR_BINARY) 			$(ISYS_BINARIES_DIR)/bin/
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/etc/ssh
	#
	#

	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/lib

	#

	# copy over libnss files for non-uclibc arches
	# (mklibs doesn't automatically pull these in)
ifeq ($(USERSPACE64),1)
	## there maybe older compat versions that we don't want, but
	## they have names like libnss1_dns so this shouldn't copy them.
	## we do the sort so that files from /lib64 files will be copied over
	## identically named files from /lib
	#cp -a $(sort $(wildcard /lib*/libnss_dns-*)) $(ISYS_BINARIES_DIR)/lib
	## if multiple libnss_dns.so.* symlinks exist, only grab the one with
	## the greatest soname, which should drop the old compat versions
	#cp -a $(word $(words $(sort $(wildcard /lib*/libnss_dns*))), \
	#  $(sort $(wildcard /lib*/libnss_dns*))) $(ISYS_BINARIES_DIR)/lib
	#
	#
	#XXX trying new code below -BEF- XXX  cp -a $(sort $(wildcard /lib*/libnss_dns-*)) $(ISYS_BINARIES_DIR)/lib
	#XXX we're not concerned about space here, why are we trying to only get the largest .so name?  why not all?
	#XXX simplifying the code.  let's see if anything breaks. -BEF-
	output=`find /lib/ -name libnss_dns*`
	test ! -n "$(output)" || cp -a /lib/libnss_dns*   $(ISYS_BINARIES_DIR)/lib
	mkdir -m 755 -p $(ISYS_BINARIES_DIR)/lib64
	test ! -d /lib64 || cp -a /lib64/libnss_dns* $(ISYS_BINARIES_DIR)/lib64
endif

	#
	# Use the mklibs script from Debian to find and copy libraries and 
	# any soft links.  Note: This does not require PIC libraries -- it will
	# copy standard libraries if it can't find a PIC equivalent.  -BEF-
	#
ifeq ($(USERSPACE64),1)
	# But copy over ld.so* files first.  for some reason these don't always 
	# get copied by mklibs if both /lib/ld* and /lib64/ld* exist) -BEF-
	#
	output=`find /lib/ -name ld*`
	test ! -n "$(output)" || cp -a /lib/ld*   $(ISYS_BINARIES_DIR)/lib
	test ! -d /lib64 || cp -a /lib64/ld* $(ISYS_BINARIES_DIR)/lib64
endif

ifeq ($(USERSPACE64),1)
	cd $(ISYS_BINARIES_DIR) \
		&& $(TOPDIR)/initrd_source/mklibs.bef -L $(SRC_DIR)/$(PARTED_DIR)/libparted/.libs:$(SRC_DIR)/$(LVM_DIR)/libdm:$(SRC_DIR)/$(E2FSPROGS_DIR)/lib:/lib64:/usr/lib64:/usr/kerberos/lib64:/lib:/usr/lib:/usr/kerberos/lib:/usr/local/lib:/opt/gnome/lib:/lib/tls:`find /lib/tls /usr/lib/tls /lib64/tls /usr/lib64/tls -type d 2>/dev/null | tr '\n' :` -v -d lib64 bin/* sbin/* usr/bin/* usr/sbin/* $(INITRD_BUILD_DIR)/*bin/* $(INITRD_BUILD_DIR)/usr/*bin/*
else
	cd $(ISYS_BINARIES_DIR) \
		&& $(TOPDIR)/initrd_source/mklibs.bef -L $(SRC_DIR)/$(PARTED_DIR)/libparted/.libs:$(SRC_DIR)/$(LVM_DIR)/libdm:$(SRC_DIR)/$(E2FSPROGS_DIR)/lib:/lib:/usr/lib:/usr/kerberos/lib:/usr/local/lib:/opt/gnome/lib:/lib/tls:`find /lib/tls /usr/lib/tls -type d 2>/dev/null | tr '\n' :` -v -d lib bin/* sbin/* usr/bin/* usr/sbin/* $(INITRD_BUILD_DIR)/*bin/* $(INITRD_BUILD_DIR)/usr/*bin/*
endif

ifdef IS_PPC64
	# Copy all the libnss*. It seems that with ppc64 these are not 
	# correctly included. -AR-
	[ -d /lib64 ] && cp -a /lib64/libnss* $(ISYS_BINARIES_DIR)/lib64 || true
endif

	#
	#
	# install kernel modules. -BEF-
	#
	$(MAKE) -C $(LINUX_SRC) modules_install INSTALL_MOD_PATH="$(ISYS_BINARIES_DIR)"
	
	#
	# If the build system doesn't have module-init-tools installed, and
	# our modules need it, we need to use the depmod we built.  For now we'll
	# just say, you need to have module-init-tools installed for building.
	#
	# We could get fancy at some point, and test for it with something like this:
	#
	# 	depmod --version | grep -q module-init-tools
	#
	# and build it if it's not there.
	#
	# The find command is to figure out the kernel version string
	#
	ISYS_KERNEL_VERSION=`find $(ISYS_BINARIES_DIR)/lib/modules -mindepth 1 -maxdepth 1 -type d -printf "%f"` ; \
	depmod -b $(ISYS_BINARIES_DIR) $$ISYS_KERNEL_VERSION
	#
	
	#
	# get rid of build, which may exist as a link to the kernel source directory (won't exist in ISYS anyway). -BEF-
	rm -f $(ISYS_BINARIES_DIR)/lib/modules/*/build
	#
	# get rid of source, which may also exist as a link to the kernel source directory (won't exist in ISYS anyway). -BEF-
	rm -f $(ISYS_BINARIES_DIR)/lib/modules/*/source
	#
	# Tar it up, baby! -BEF-
	cd $(ISYS_BINARIES_DIR) && tar -cv * | gzip -9 > $(ISYS_BINARIES_TARBALL)
	#
	# Note: This tarball should be installed to the "boot/$(ARCH)/$(FLAVOR)" directory.


PHONY += isys_binaries_clean
isys_binaries_clean:
	rm -rf $(ISYS_BINARIES_DIR)
	rm -f  $(ISYS_BINARIES_DIR).prep
	rm -f  $(ISYS_BINARIES_TARBALL)
