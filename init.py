import compile_main as cp
import subprocess as sb
import sys

def inputname():
    print('pleast input count of names')
    n = int(input())
    with open('namelist.txt','w') as f:
        for i in range(n):
            print('\tplease input No.' + str(i+1) + ' player\'s name:')
            print('\t',end='')
            name = input()
            name = name.strip()
            f.write(name)
            if (i != n-1):
                f.write('\n')
    print('now compile begin')
    print()
    cp.make()
    print('compile finish!')

def run():
    inputname()
    try:
        sb.Popen(['main.bat',sys.argv[2],sys.argv[3]])
    except:
        helpbook()
        s = ''
        while (s != 'y')&(s != 'n')&(s != 'yes')&(s != 'no'):
            print('you miss some args of default mode, continue to run non-limited random mode test?(y/n)')
            s = input()
            if (s == 'y')|(s == 'yes'):
                sb.Popen(['main.bat','0','random'])
            elif (s == 'n')|(s == 'no'):
                return

def run_noninit():
    try:
        sb.Popen(['main.bat',sys.argv[2],sys.argv[3]])
    except:
        s = ''
        while (s != 'y')&(s != 'n')&(s != 'yes')&(s != 'no'):
            print('you miss some args of run mode, continue to run non-limited random mode test?(y/n)')
            s = input()
            if (s == 'y')|(s == 'yes'):
                sb.Popen(['main.bat','0','random'])
            elif (s == 'n')|(s == 'no'):
                return
        

def onlycompile():
    cp.make()

def helpbook():
    print('Here are some help for you:')
    print('\t-r     :  run only, requires that you have already compiled all the src and create the \'namelist.txt\' ')
    print('\t          you also need some args for runing mode : first arg is the count of tests, 0 means non-limited; second arg is data mode')
    print('\t          data modes : random or jml3test or shortmain')
    print('\t-c     :  compile only, requires that you have created \'namelist.txt\' ')
    print('\t-cr    :  compile and run, requires that you have created \'namelist.txt\' ,args are the same as -r')
    print('\t-inputc:  input the names and compile them')
    print('\tdefault:  input names and compile and run, need the same args as -r')

if __name__ == "__main__":
    with open('main.bat','w') as f:
        f.write('@echo off\n')
        f.write('del result.bat\n')
        f.write('del del_500.bat\n')
        f.write('del out\*.err\n')
        f.write('del out\*.out\n')
        f.write('del data\*.txt\n')
        f.write('color 2f\n')
        f.write('python feeder.py %1 %2\n')
        f.write('result.bat')
    if (len(sys.argv) < 2):
        run()
    elif (sys.argv[1] == '-c'):
        onlycompile()
    elif (sys.argv[1] == '-r'):
        run_noninit()
    elif (sys.argv[1] == '-cr'):
        onlycompile()
        run_noninit()
    elif (sys.argv[1] == '-inputc'):
        inputname()
    elif (sys.argv[1] == '--help'):
        helpbook()
    else:
        helpbook()
