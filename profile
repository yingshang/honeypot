PS1="`whoami`@`hostname`:"'[$PWD]'
history
USER_IP=`who -u am i 2>/dev/null| awk '{print $NF}'|sed -e 's/[()]//g'`
if [ "$USER_IP" = "" ]
then
USER_IP=`hostname`
fi
if [ ! -d /usr/operation ]
then
mkdir /usr/operation
chmod 777 /usr/operation
fi
if [ ! -d /usr/operation/${LOGNAME} ]
then
mkdir /usr/operation/${LOGNAME}
chmod 300 /usr/operation/${LOGNAME}
fi
export HISTSIZE=4096
DT=`date "+%Y-%m-%d_%H:%M:%S"`

if [ ! -d /usr/operation/${LOGNAME}/${USER_IP} ]
then
mkdir /usr/operation/${LOGNAME}/${USER_IP}
chmod 300 /usr/operation/${LOGNAME}/${USER_IP}
fi


export HISTFILE="/usr/operation/${LOGNAME}/${USER_IP}/$DT"
chmod 600 /usr/operation/${LOGNAME}/${USER_IP}/** 2>/dev/null