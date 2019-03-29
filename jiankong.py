import os
import datetime
import pyinotify
import logging
import shutil
import random
import hashlib
import string

import sys
path = "/usr/share/record/file/"


def mylog():
    # 创建一个日志记录器
    log = logging.getLogger("test_logger")
    log.setLevel(logging.INFO)
    # 创建一个日志处理器
    ## 这里需要正确填写路径和文件名，拼成一个字符串，最终生成一个log文件
    logHandler = logging.FileHandler(filename ="/usr/share/record/error.log")
    ## 设置日志级别
    logHandler.setLevel(logging.INFO)
    # 创建一个日志格式器
    formats = logging.Formatter('%(asctime)s %(levelname)s: %(message)s',
                datefmt='[%Y/%m/%d %I:%M:%S]')

    # 将日志格式器添加到日志处理器中
    logHandler.setFormatter(formats)
    # 将日志处理器添加到日志记录器中
    log.addHandler(logHandler)
    return log


def GetFileMd5(filename):
    if not os.path.isfile(filename):
        return
    myhash = hashlib.md5()
    f = open(filename,'rb')
    while True:
        b = f.read(8096)
        if not b :
            break
        myhash.update(b)
    f.close()
    return myhash.hexdigest()


def filecp(source,name,type):
    day_name = path + datetime.datetime.now().strftime('%Y%m%d')
    hour_name = day_name+'/' + datetime.datetime.now().strftime('%H')
    if not os.path.exists(day_name):
        os.mkdir(day_name)
        if not os.path.exists(hour_name):
            os.mkdir(hour_name)

    try:
        source_md5 = GetFileMd5(source)
        status = 0

        for root, dirs, files in os.walk(path, topdown=False):
            for i in files:
                file_md5 = GetFileMd5(os.path.join(root, i))
                if  file_md5 == source_md5:
                    status = 1

        if status ==0:
            fsize = int(os.path.getsize(source))

            if fsize != 0:
                now = datetime.datetime.now().strftime("%M-%S")
                token = ''.join(random.sample(string.ascii_letters + string.digits, 8))
                shutil.copy(source,hour_name+'/'+name + "_" +token+"_"+now+"_"+type)
    except FileNotFoundError:
        pass
    except OSError:
        pass


class MyEventHandler(pyinotify.ProcessEvent):
    logging.basicConfig(level=logging.INFO, filename='/usr/share/record/monitor.log')

    logging.info("Starting monitor...")

    def process_IN_ACCESS(self, event):
        print("ACCESS event:", event.pathname)
        logging.info("ACCESS event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))

    def process_IN_ATTRIB(self, event):
        print("ATTRIB event:", event.pathname)
        logging.info("IN_ATTRIB event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
#        filecp(source=os.path.join(event.path, event.name),name=event.name,type="ATTRIB")


#    def process_IN_CLOSE_NOWRITE(self, event):
#        print("CLOSE_NOWRITE event:", event.pathname)
#        logging.info("CLOSE_NOWRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


#    def process_IN_CLOSE_WRITE(self, event):
#        print("CLOSE_WRITE event:", event.pathname)
#        logging.info("CLOSE_WRITE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
#        filecp(source=os.path.join(event.path, event.name),name=event.name,type="CLOSE_WRITE")


    def process_IN_CREATE(self, event):
        print("CREATE event:", event.pathname)
        logging.info("CREATE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        filecp(source=os.path.join(event.path, event.name),name=event.name,type="CREATE")


    def process_IN_DELETE(self, event):
        print("DELETE event:", event.pathname)
        logging.info("DELETE event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        #filecp(source=os.path.join(event.path, event.name),name=event.name,type="DELETE")


    def process_IN_MODIFY(self, event):
        print("MODIFY event:", event.pathname)
        logging.info("MODIFY event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))
        if event.name != "null":
            filecp(source=os.path.join(event.path, event.name), name=event.name, type="MODIFY")

    def process_IN_OPEN(self, event):
        print("OPEN event:", event.pathname)
        logging.info("OPEN event : %s  %s" % (os.path.join(event.path, event.name), datetime.datetime.now()))


def main():
    # watch manager
    excl_list = [
        '/usr/share/record',
        '/var/log',
    ]
    excl = pyinotify.ExcludeFilter(excl_list)
    wm = pyinotify.WatchManager()
    wm.add_watch('/tmp', pyinotify.ALL_EVENTS, rec=True,exclude_filter=excl)

    eh = MyEventHandler()

    # notifier
    logger = mylog()

    try:
        notifier = pyinotify.Notifier(wm, eh)
        notifier.loop()
    except :
        logger.exception(sys.exc_info())
        logger.info("Error in log")

if __name__ == '__main__':
    main()