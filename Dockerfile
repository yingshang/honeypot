FROM ubuntu:14.04
RUN apt-get update -y   
RUN apt install -y  gcc openssl wget  rsyslog zlib1g-dev  libssl-dev make vim   apache2    default-jre

#ssh
RUN cd /opt && wget https://ftp.eu.openbsd.org/pub/OpenBSD/OpenSSH/portable/openssh-6.2p1.tar.gz && tar zxvf openssh-6.2p1.tar.gz
RUN sed -i '1i\sshd:x:74:74:Privilege-separated SSH:/var/empty/sshd:/sbin/nologin'  /etc/passwd
RUN cd /opt/openssh-6.2p1 && sed -e 's/struct passwd \* pw = authctxt->pw;/logit("Username: %s, Password: %s", authctxt->user, password);\nstruct passwd \* pw = authctxt->pw;/' -i auth-passwd.c  && ./configure && make && make install  
COPY sshd_config  /usr/local/etc/sshd_config
RUN echo root:123456 | chpasswd
RUN touch /var/log/auth.log && chmod 777 /var/log/auth.log
COPY profile /etc/profile
RUN rm -rf /op/*

#mysql
RUN apt-get install software-properties-common -y
RUN  apt-key adv --recv-keys --keyserver hkp://keyserver.ubuntu.com:80 0xcbcb082a1bb943db
RUN add-apt-repository 'deb http://sfo1.mirrors.digitalocean.com/mariadb/repo/10.0/ubuntu trusty main'
RUN apt update -y
RUN apt install -y mariadb-server
RUN sed -i "47s/127.0.0.1/0.0.0.0/g" /etc/mysql/my.cnf
RUN sed -i "51s/100/100000/g" /etc/mysql/my.cnf
RUN /etc/init.d/mysql start && mysql -uroot -e "set password for root@localhost = password('123456'); GRANT ALL PRIVILEGES ON *.* TO 'root'@'%' IDENTIFIED BY '123456' WITH GRANT OPTION;flush privileges; " 

#jiankong
RUN apt install -y python3 python3-pip
RUN pip3 install pyinotify
#RUN mkdir /usr/share/record  && mkdir /usr/share/record/file/ &&  mkdir /usr/share/record/logs/
COPY jiankong.py /usr/share/

#run
COPY run.sh /run.sh
RUN chmod +x /run.sh

RUN rm -rf /opt/*

EXPOSE 22
ENTRYPOINT /run.sh
