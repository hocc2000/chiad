import shutil
import time
import os
import sys
from datetime import datetime

bufferPaths = ['/home/rb/shared']
farmPaths   = ['/media/rb/F036CD5B36CD2406', '/media/rb/FC441AE4441AA206', '/media/rb/BA0A81E90A81A34D', '/media/rb/0802409002408522']

plotMinSize = 108000000000
plotMaxSize = 109000000000
beforeMove  = 5




def getNow():
    now = time.localtime()
    return "%04d.%02d.%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)


try:
    print('Start CHIA moving...')
    while 1:
        for bufferPath in bufferPaths:
        #for bufferPath in farmPaths:
            bufferFileLists = os.listdir(bufferPath)
            if len(bufferFileLists) == 0:
                print('[%s] No any completed plots.' % getNow())
            else:
                for bufferFileName in bufferFileLists:
                    fileSize = os.path.getsize('%s/%s' % (bufferPath, bufferFileName))
                    if os.path.isfile("chia-move-stop"):
                        sys.exit('Stop working!')
                    if fileSize > plotMinSize:
                        if bufferFileName.endswith('.plot'):
                            for farmPath in farmPaths:
                                total, used, free = shutil.disk_usage(farmPath)
                                if free > plotMaxSize:
                                    print('[%s] Wait %s secs before move.' % (getNow(), beforeMove))
                                    time.sleep(beforeMove)
                                    #print(bufferFileName)
                                    print('[%s] Move files from %s to %s. (%s)' % (getNow(), bufferPath, farmPath, bufferFileName))
                                    shutil.copy(bufferPath + '/' + bufferFileName, farmPath + '/' + bufferFileName + '.copy')
                                    time.sleep(2)
                                    os.rename(farmPath + '/' + bufferFileName + '.copy', farmPath + '/' + bufferFileName)
                                    time.sleep(2)
                                    os.remove(bufferPath + '/' + bufferFileName)
                                    print('[%s] File move is complete. (%s)' % (getNow(), bufferFileName))
                                    break
                                else:
                                    print('[%s] No any free space. (%s)' % (getNow(), farmPath))
        time.sleep(30)

except KeyboardInterrupt:
        print ('')
