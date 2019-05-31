import subprocess as sb
import sys
import time
import os,shutil
from spec_judge import spec_judge

depend = 'lib/uml-homework-1.0.0-raw-jar-with-dependencies.jar'


def run_pro(cp,mc,name,infile):
    global depend
    fin = open(infile,'r')
    start_time = time.time()
    errout = open("out\\"+name+'.err','w')
    with open("out\\"+name+".out", "w") as fout:
        p = sb.Popen(["java", "-cp", depend+";"+cp, mc], stdin=fin, stdout=fout, stderr=errout)
        if p == None:
            print("open on %s failed" %(name))
            return -1
        else:
            try:
                p.wait(35)
            except:
                end_time = time.time()
                p.kill()
                if (end_time - start_time >= 33):
                    print(name + ' run over, time is ' + str(end_time - start_time))
                    errout.close()
                    return None
                else:
                    errout.close()
                    return 99999
    end_time = time.time()
    fin.close()
    print(name + ' run over, time is ' + str(end_time - start_time))
    errout.close()
    if (end_time - start_time >= 20):
        return None
    return p.poll()

def main(max = 0,datamode = 'random'):
    f = open('namelist.txt','r')
    names = f.readlines()
    f.close()
    for i in range(len(names)):
        names[i] = names[i].strip()
    mc = []
    for i in names:
        with open('classes\\'+i.strip()+'\\'+'mainclass.txt','r') as f:
            mc.append(f.readline().strip())
    counter = max 
    k = True
    print()
    nre = ''
    
    print('NO.'+str(counter))
    end = []
    for i in range(len(names)):
        re = run_pro('classes\\'+names[i],mc[i],names[i],'data/data' +str(counter) + '.txt')
        end.append(re)
    k = True
    print('results:')
    rnames = []
    for i in range(len(names)):
        t = True
        with open('out\\'+names[i] +'.err','r') as err:
            if (err.readline().strip() != ''):
                end[i] = -1
        if (end[i] != 0)&(end[i] != None):
            if (end[i] == 99999):
                return
            k = False
            t = False
            print('\t' + names[i] + ' : RE')
            nre += names[i] + '_RE'
        elif (end[i] == None):
            t = False
            k = False
            print('\t' + names[i] + ' : TLE')
            nre += names[i] + '_TLE'
        if (t):
            rnames.append(names[i])
    # if (k != False):
    sp = spec_judge()
    k = sp.run(rnames)
    print()
    if (k == False):
        nre += 'WA'
        
    if (k == False):
        with open('result.bat','w') as out:
            out.write('@echo off\n')
            out.write('color 4f')
    else:
        print('Run Finish.')
        with open('result.bat','w') as out:
            out.write('@echo off\n')
            out.write('color 2f\n')
            out.write('del out\*.out')
    sb.Popen(['result.bat'])

main(int(sys.argv[1]))

