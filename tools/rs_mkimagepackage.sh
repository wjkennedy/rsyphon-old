#!/bin/bash
#
#
###################################
#
# Packages and extracts a Rsyphon image contained in /var/lib/rsyphon/images/
# in such a way that a tarball is generated that can be deployed into another
# Rsyphon server at another time.
#
# All Rsyphon-related files are contained in the generated package.
#
###############################################################################

DATE=$(date +%Y%m%d)
IMAGE_DIR=/var/lib/rsyphon/images/
LOG=/var/log/$0.$DATE.log
PACKAGE=/var/lib/rsyphon/$2.$DATE.image_package.tar.bz2
IMAGE=$2

########################################
# BEGIN create image tarball
create_pkg(){
if [ -z $IMAGE ]
then
    echo "Error 33: Image name not recognized.  Please run 'rs_lsimage' and verify the image name."
    echo "Quitting.  Check the log [$LOG] for details."
    exit 33
fi

# Create image tarball

echo "Creating Image tarball from $IMAGE"

tar -jcf $PACKAGE\
 /var/lib/rsyphon/images/$IMAGE\
 /etc/rsyphon/rsync_stubs/*$IMAGE\
 /var/lib/rsyphon/scripts/$IMAGE.master\
 /var/lib/rsyphon/scripts/$IMAGE.sh\
 /var/lib/rsyphon/overrides/$IMAGE

if [ $? -eq 0 ]
then
    tput bold
    echo "Image $IMAGE compressed as $PACKAGE"
    tput sgr0
    echo
    echo "This image can now be pushed or extracted."
    echo "Re-configuring rsyncd.conf"
    rs_mkrsyncd_conf
    echo
else
    tput bold
    echo "Image $IMAGE COULD NOT be captured."
    echo "Check the available disk space"
    tput sgr0
    echo
    echo -n "View log? [y/n]"; read view_log
      case "$view_log" in
        "y" | "Y")
            echo "Viewing log..  'Q' to quit."
            sleep 1
            less $LOG
        ;;
        "n" | "N")
            echo "Quitting.  Check the log [$LOG] for details."
            exit 1
        ;;
      esac
fi

# Create MD5 sum
IMAGE_SUM=`basename $PACKAGE .tar.bz2`.MD5SUM
md5sum $PACKAGE > $IMAGE_SUM 
}
# END create image tarball
########################################


########################################
# BEGIN extract image tarball
extract_pkg(){
# Extract image package and integrate with SI

echo "Extracting Image tarball - $2"

tar -C / -jxvf $2

echo "Restarting Rsyphon rsync server."
/etc/init.d/rsyphon-server-rsyncd restart
if [ $? = "0" ]
then
    echo "Rsyphon server restarted."
    echo "Verifying new image integration."
    rs_lsimage | grep $2
    echo
        if [ $? != "0" ]
        then
            echo "There seems to be a problem registering this image with Rsyphon."
        else
            echo "$2 seems to be incorporated."
        fi
else
    echo "Rsyphon server could not be restarted."
    error 1
fi
}
# END extract image tarball
########################################

########################################
# BEGIN Main

case "$1" in
    "-e" | "--extract")
    echo "Extracting package.." ; sleep 1 ; clear
    extract_pkg
    ;;

    "-c" | "--create")
    echo "Creating package.." ; sleep 1 ; clear
    echo -e "To extract this package, use:\n '$0 -e tarball.tar.bz2' \n or \n 'tar -C / -jxf tarball.tar.bz2' \n and \n '/etc/init.d/rsyphon-server-rsyncd restart'"
    create_pkg
    ;;

    *)
    clear
    echo "To create an image:"
    echo "Usage: $0 --create [-c] image_name"
    echo
    echo "image_name is the output from $(tput bold)rs_lsimage$(tput sgr0) that corresponds to your image."
    echo
    echo "-----------------------------------------"
    echo "To extract an image:"
    echo "Usage: $0 --extract [-e] tarball.tar.bz2" 
    echo
    echo "'tarball' is the tar.bz2 file with a date and that correspond to your image."
    echo
    echo "Program output information is in $LOG."
    echo
    tput sgr0
    exit 1
    ;;
esac
