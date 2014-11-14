# /bin/bash
#- Build packages:
#- Upload packages, source tarball and PDF manual
 

build(){
echo "Building..."
PWD=$(pwd)
cd autoconf && ./bootstrap && rm -rf autom4te.cache aclocal.m4

# Not on a debian build system at the moment
#cd .. && make source_tarball && make deb && make rpm && make docs
cd .. && make source_tarball && make rpm && make docs

}

bump_rev(){
#AC_INIT(rsyphon, 0.$MAJOR.$VERSION, william@a9group.net)
CONFIGAC="autoconf/configure.ac"
VERSION=$(grep AC_INIT autoconf/configure.ac | awk -F" " -F"," '{print $2}' | sed 's/^ //g')
RELEASE=$(grep AC_INIT autoconf/configure.ac | awk -F" " -F"," '{print $2}' | sed 's/^ //g')
MAJOR=$(grep AC_INIT autoconf/configure.ac | awk -F" " -F"," '{print $2}' | sed 's/^ //g' | cut -f1 -d.)
MINOR=$(grep AC_INIT autoconf/configure.ac | awk -F" " -F"," '{print $2}' | sed 's/^ //g' | cut -f2 -d.)
VERSION=$(grep AC_INIT autoconf/configure.ac | awk -F" " -F"," '{print $2}' | sed 's/^ //g' | cut -f3 -d.)
NEWMAJOR=$[MAJOR +1]
NEWVERSION=$[VERSION +1]

# Bump major version
major_bump(){
	echo "New Major release version $NEWMAJOR"
}

if [ $VERSION -ge 98 ]
then
	echo "Major revision bump needed."
	major_bump
else
	sed 's/rsyphon, $RELEASE/rsyphon, 0.$NEWMAJOR.$NEWVERSION/g' $CONFIGAC
	if [ $? -ne 0 ]
	then
		echo "Failed to change autoconf/configure.ac"
		exit 1
	else	
	echo "Version 0.$NEWMAJOR.$NEWVERSION"
	build
	fi
fi
}

bump_rev
