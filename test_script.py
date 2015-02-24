import subprocess
import os
import glob
from multiprocessing import Process
import time
import re
from datetime import datetime

stresstests = ['test.json']
currentdir = os.getcwd() + '/'

def compactionstats(filename):
    isalive = True
    with open(filename, 'w') as f:
        while isalive:
            args = ['fab/stress/default/bin/nodetool', '-h', 'node1', 'compactionstats']
            p = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            statsout = p.communicate()
            processes =  subprocess.check_output('ps auwx | grep stress', shell=True)
            if 'cstar_perf_stress' not in processes:
                isalive=False
            pendingtasks = re.search('pending tasks: [0-9]+', statsout).group()
            f.write(str(datetime.now()) + "    " + pendingtasks + "\n")

for test in stresstests:
    logname = test[:test.find('.')] + 'compactions.log'
    statsname = test[:test.find('.')] + 'compactionstats.log'
    p = Process(target=compactionstats, args=(statsname,))
    p.start()
    subprocess.call('cstar_perf_stress ' + test, shell=True)
    p.join()
    newestlogs = max(glob.iglob(os.path.join(currentdir + '.cstar_perf/logs', '*.tar.gz')), key=os.path.getctime)
    unziplog = 'tar -xvf ' + newestlogs
    subprocess.call(unziplog, shell=True)
    directname = newestlogs[newestlogs.rfind('/')+1 : newestlogs.find('.tar')]
    directory = currentdir + directname + '/node1/system.log'
    with open(directory, 'r') as syslog, open(logname, 'w') as complog:
        for line in syslog:
            if 'CompactionExecutor' in line:
                complog.write(line)
    subprocess.call("rm -r " + currentdir + directname, shell=True)
