import os
import time


bufferPath  = ['/home/chiad/buffer']
tempPaths   = ['/home/chiad/temp1', '/home/chiad/temp2', '/home/chiad/temp3', '/home/chiad/temp4', '/home/chiad/temp5', '/home/chiad/temp6']
logsPath    = '/home/chiad/logs'


plotType    = 32
threadNum   = 4
bufferSize  = 3408
pollingTime = 30
plottingMax = 4
farmerKey   = '-f '
poolKey     = '-p '
plotMinSize = 108000000000
plotMaxSize = 109000000000


def getNow1():
    now = time.localtime()
    return "%04d.%02d.%02d %02d:%02d:%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

def getNow2():
    now = time.localtime()
    return "%04d_%02d_%02d_%02d_%02d_%02d" % (now.tm_year, now.tm_mon, now.tm_mday, now.tm_hour, now.tm_min, now.tm_sec)

try:
    print('Start CHIA plotting...')

    if not os.path.isdir(logsPath):
        os.mkdir(logsPath)

    while 1:
        totalJobs = 0
    
        result = os.popen('ps -ax | grep /home/chiad/chia-blockchain/venv/bin/python').read()
        lines  = result.split('\n')

        for tempPath in tempPaths:
            jobCount = 0
            minDelayCount = 0
            for line in lines:
                if tempPath in line:
                    totalJobs += 1
                    jobCount += 1
                    lineSplits = line.split(' ')
                    for lineSplit in lineSplits:
                        if ':' in lineSplit:
                            timeSplit = lineSplit.split(':')
                            if int(timeSplit[0]) < runDelay:
                                minDelayCount += 1
                    


            print('[%s] %s : %d' % (getNow1(), tempPath, jobCount))
            if jobCount < maxPlotJob:
                if minDelayCount == 0:
                    os.popen('cd ~/chia-blockchain; . ./activate; nohup chia plots create ' + farmerKey + poolKey + '-n 1 -k 32 -b 6500 -r 4 -u 128 -t ' + tempPath + ' -2 ' + tempPath + ' -d ' + bufferPath + ' > ' + logsPath + '/' + getNow2() + '.log 2>&1 &')
                    print('[%s] Start a new job. (%s)' % (getNow1(), tempPath))
                    time.sleep(120)
    
        print('[%s] Total Jobs : %d' % (getNow1(), totalJobs))

        time.sleep(60)

except KeyboardInterrupt:
    print ('')
