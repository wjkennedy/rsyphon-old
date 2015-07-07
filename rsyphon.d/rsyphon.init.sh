#!/bin/bash
#
# rsyphon init file
#
# Thu Apr 23 20:00:08 PDT 2015
# william@a9group.net
#
########################################

hello(){

	clear
	
	echo "rsyphon"

	sleep 1
}

rs_init(){

	echo "installing..."
	sleep 1
	rsync -Rav * /

	echo "initializing..."
	touch /etc/rsyphon/rsyncd.conf
	/etc/init.d/rsyphon-server-rsyncd start
	if [ $? -ne 0 ]
	then
		echo "system 500 is not supported."
		sleep 1
		exit 1
	else
		echo "attempting to prepare client for image retrieval..."
		sleep 1
		rs_prepareclient --server localhost 
	fi
	
}

hello

rs_init
