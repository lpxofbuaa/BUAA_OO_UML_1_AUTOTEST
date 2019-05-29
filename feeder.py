import subprocess as sb
import sys
import time
import os,shutil
from spec_judge import spec_judge

depend = 'lib/specs-homework-1-1.1-raw-jar-with-dependencies.jar;lib/specs-homework-2-1.2-raw-jar-with-dependencies.jar;lib/specs-homework-3-1.3-raw-jar-with-dependencies.jar'
eff = 'efficient\\'
effile = None

def openeff():
    global effile
    effile = open(eff + str(int(time.time())) + '.csv','w')

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
                    effile.write(str(end_time - start_time) + ',')
                    errout.close()
                    return None
                else:
                    effile.write(str(end_time - start_time) + ',')
                    errout.close()
                    return 99999
    end_time = time.time()
    fin.close()
    print(name + ' run over, time is ' + str(end_time - start_time))
    effile.write(str(end_time - start_time) + ',')
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
        effile.write(names[i])
        effile.write(',')
        if (i == len(names) - 1):
            effile.write('\n')
    mc = []
    for i in names:
        with open('classes\\'+i.strip()+'\\'+'mainclass.txt','r') as f:
            mc.append(f.readline().strip())
    counter = 0
    k = True
    print()
    nre = ''
    while (k)&(not ((max!=0)&(counter >= max))):
        print('NO.'+str(counter+1))
        counter+=1
        end = []
        datamake = sb.Popen(["python","data_make.py",str(counter),str(datamode)])
        datamake.wait()
        for i in range(len(names)):
            re = run_pro('classes\\'+names[i],mc[i],names[i],'data/data' +str(counter) + '.txt')
            end.append(re)
        effile.write('\n')
        k = True
        print('results:')
        realnames = []
        for i in range(len(names)):
            with open('out\\'+names[i]+'.err','r') as ferr:
                err = ferr.readline()
            if (err.strip() != ''):
                print('\t' + names[i] + ' : RE')
                nre += names[i] + '_RE'
                k = False
                continue
            if (end[i] != 0)&(end[i] != None):
                if (end[i] == 99999):
                    return
                k = False
                print('\t' + names[i] + ' : RE')
                nre += names[i] + '_RE'
            elif (end[i] == None):
                k = False
                print('\t' + names[i] + ' : TLE')
                nre += names[i] + '_TLE'
            else:
                realnames.append(names[i])
        # if (k == False):
            # break
        sp = spec_judge()
        k = sp.run(realnames)
        print()
        if (k == False):
            nre += 'WA'
            break
        if (counter%500 == 0):
            print()
            print('Finished 500 tests, delete datas.')
            with open('del_500.bat','w') as delbat:
                delbat.write('@echo off\n')
                delbat.write('del data\*.txt')
            delbat = sb.Popen(['del_500.bat'])
            delbat.wait()
        # break
        
    if (k == False):
        with open('result.bat','w') as out:
            out.write('@echo off\n')
            out.write('copy data\data'+str(counter)+'.txt keyData'+ '\\' + nre +str(int(time.time()))+'.txt\n')
            out.write('color 4f')
    else:
        print('Run Finish.')
        with open('result.bat','w') as out:
            out.write('@echo off\n')
            out.write('del out\*.out')

openeff()
if (len(sys.argv) < 2):
    main()
elif (len(sys.argv) < 3):
    main(int(sys.argv[1]))
else:
    main(int(sys.argv[1]),sys.argv[2])
effile.close()
