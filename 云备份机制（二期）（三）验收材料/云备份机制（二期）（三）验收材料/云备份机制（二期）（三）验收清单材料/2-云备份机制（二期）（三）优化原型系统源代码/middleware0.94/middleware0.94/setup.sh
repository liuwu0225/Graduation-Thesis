#!/bin/sh

PYTHON=python

isroot()
{
	if [ "$USER" != "root" ];
	then
		echo  -e "The user must be root, and now your user is $USER, please su to root"
		exit 1
	else
		#echo -e "check root... OK."
		return 0
	fi
}

do_stop()
{
    isroot
    PROC_NAME="python mwserver.py"
    bash_ppid=$(ps -ef | grep "$PROC_NAME" | grep -v grep | awk '{print $2}')
	#ProcNumber=ps -ef | grep $PROC_NAME | grep -v grep | wc -l
	#echo "$bash_ppid"
	if [ "$bash_ppid" = "" ];
    then 
        return 0
    else
        kill "$bash_ppid"
        rm /tmp/daemon.pid
        rm /var/log/mwlog.db
    fi
    echo "mwserver stop"
}

do_start()
{
    isroot
    do_stop
    $PYTHON mwserver.py
    echo "mwserver start."
}


do_install()
{
    isroot
    INSTALL=apt-get
    type apt-get > /dev/null 2>&1 || exit "please install apt-get first." 
    $INSTALL install curl
    if [ ! type pip > /dev/null 2>&1 ]; then
        $INSTALL install python-pip
        fi
    pip install rsa
    dpkg -P libcrypto
    dpkg -i libsecrypto.deb
    file="/usr/lib/libsecrypto.so"
    if [ ! -f "$file" ]; then
        echo "install failed"
        return 0
    fi
    echo "install finished."
}

do_status()
{
    echo "status"    
}

usage()
{
    echo "Nothing to do."
}

if [ $# -gt 0 ]; then
    CMD=$1
    case $CMD in
        install)
            do_install $@
            exit $?;;
        start)
            do_start $@
            exit $?;;
        stop)
            do_stop $@
            exit $?;;
        restart)
            do_stop $@
            do_start $@
            exit $?;;
        status)
            do_status $@
            exit $?;;
        *)
            usage;;
        esac
else
    usage
fi
exit 255



