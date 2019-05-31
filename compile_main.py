import subprocess as sb
import sys
import time
import os,shutil

clist = []
depend = 'lib/uml-homework-1.0.0-raw-jar-with-dependencies.jar'

def find():
    global clist
    with open('compile.bat','w') as f:
        f.write('@echo off\n')
        f.write('findstr /S "\<public.static.void.main\>" *.java > compile_list.txt\n')
    p = sb.Popen(['compile.bat'])
    p.wait()
    with open('compile_list.txt', 'r') as f:
        clist = f.readlines()
    for i in range(len(clist)):
        q = clist[i].split(':')
        clist[i] = q[0].strip()
    if (clist[-1] == ''):
        del clist[-1]


def compile(root,name):
    rootlist = root.split('\\')
    i = 0
    k = False
    package = ''
    while (i < len(rootlist)):
        if (k):
            plist = rootlist[i].split('.')
            if (len(plist) == 1):
                package += plist[0].strip() + '.'
            else:
                package += plist[0].strip()
        else:
            if (rootlist[i].strip() == name):
                k = True
        i += 1
    # print(package)
    p = sb.Popen(['javac','-cp',depend,'-d','classes\\'+name,'-sourcepath','classes\\'+name,root,'-encoding','utf8'])
    p.wait()
    if (p.poll() == 0):
        print('compile success!')
        with open('classes\\'+name+'\\mainclass.txt','w') as f:
            f.write(package)
    print()

def make():
    find()
    with open('namelist.txt','r') as f:
        namelist = f.readlines()
    for i in range(len(namelist)):
        name = namelist[i].strip()
        t = False
        for j in range(len(clist)):
            if (name in clist[j]):
                root = clist[j]
                t = True
                break
        if (t):
            print('compile ' + name)
            compile(root,name)
        else:
            print('Error: can not find src of '+name)
            print()

if __name__ == "__main__":
    make()