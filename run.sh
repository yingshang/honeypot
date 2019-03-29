mkdir /usr/share/record
mkdir /usr/share/record/logs
mkdir /usr/share/record/file
mkdir /usr/share/seek
/etc/init.d/rsyslog  start  
/usr/local/sbin/sshd

python3 /usr/share/jiankong.py
