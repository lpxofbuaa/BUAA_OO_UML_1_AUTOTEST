from model import *

PARENTNAME = 'parent'
CLASSNAME = 'class'
INTERFACENAME = 'inter'
OPERATIONNAME = 'method'
ATTRIBUTENAME = 'attribute'
VISIBILITY = ['public','private','protected','package']
PARA = 'para'

classtotal = 5
interfacetotal = 5
operationtotal = 5
attributetotal = 5
geneclasstotal = classtotal - 1
geneintertotal = interfacetotal - 1
associationtotal = 10
realizationtotal = 5

def makeClassName(num):
    return CLASSNAME + str(num)

def makeInterfaceName(num):
    return INTERFACENAME + str(num)

def makeOperationName(parentnum,num,isClass):
    if (isClass):
        return CLASSNAME + str(parentnum) + OPERATIONNAME + str(num)
    else:
        return INTERFACENAME + str(parentnum) + OPERATIONNAME + str(num)

def makeAttributeName(parentnum,num,isClass):
    if (isClass):
        return CLASSNAME + str(parentnum) + ATTRIBUTENAME + str(num)
    else:
        return INTERFACENAME + str(parentnum) + ATTRIBUTENAME + str(num)

def makeVisibility(randomMode=False):
    if (randomMode):
        if (random.randint(0,4) != 0):
            return 'private'
    return VISIBILITY[random.randint(0,3)]

def makeOperation(builder,parentid,inputcount,isreturn,visibility,opname):
    opid = builder.createOperation(parentid,opname,visibility)
    for i in range(inputcount):
        builder.createParameter(opid,PARA + str(i),'int','in')
    if (isreturn):
        builder.createParameter(opid,'return','int','return')

'''
with ModelBuilder('Model','data1.txt') as builder:
    c1 = builder.createClass('Father','public')
    c2 = builder.createClass('Son','public')
    builder.createGeneralization('none',c2,c1)
    builder.createAttribute(c1,'name','public','String')
    builder.createAttribute(c2,'name','private','String')
    c1op1 = builder.createOperation(c1,'getName','public')
    builder.createParameter(c1op1,'n','String','return')
    c1op2 = builder.createOperation(c1,'setName','public')
    builder.createParameter(c1op2,'s','String','in')
    c1op3 = builder.createOperation(c1,'nothing','public')
    i1 = builder.createInterface('Eat','public')
    builder.createAssociation('noname','public','public',c1,i1)
'''
def randomParent(total,builder,parentlist,void,create,isClass=True):
    for i in range(total):
        parentid = create(void(i),makeVisibility())
        parentlist.append(parentid)
        opcount = 0
        opnum = 0
        oppara = []
        while (opcount < operationtotal):
            opcount += 1
            if (random.randint(0,2) == 0):
                oppara = []
                opnum += 1
            inputcount = random.randint(0,4)
            isreturn = random.choice([True,False])
            visibility = makeVisibility()
            while (str(inputcount)+str(isreturn)+str(visibility) in oppara):
                inputcount = random.randint(0,4)
                isreturn = random.choice([True,False])
                visibility = makeVisibility()
            makeOperation(builder,parentid,inputcount,isreturn,visibility,makeOperationName(i,opnum,isClass))
        attricount = 0
        while (attricount < attributetotal):
            attricount += 1
            parentnum = i
            if (random.randint(0,3) == 0):
                while (parentnum == i):
                    parentnum = random.randint(0,total)
            builder.createAttribute(parentid,makeAttributeName(parentnum,attricount,isClass),makeVisibility(True),'int')

def randomGen(builder,gentotal,parentlist,parenttotal):
    def findfather(a):
        if (parent[a] != a):
            parent[a] = findfather(parent[a])
        return parent[a]

    def link(a,b):
        fa = findfather(a)
        fb = findfather(b)
        if (fa != fb):
            parent[fa] = fb

    parent = {}
    for i in range(parenttotal):
        parent[i] = i
    for i in range(gentotal):
        fa = random.randint(0,parenttotal - 1)
        while (findfather(fa) == findfather(i)):
            fa = (fa+1)%parenttotal
        link(i,fa)
        print(str(i) + ' father is ' + str(fa))
        builder.createGeneralization('gen',parentlist[i],parentlist[fa])
    print()

def randomRealization(builder,classlist,interlist):
    for i in range(realizationtotal):
        source = classlist[random.randint(0,classtotal-1)]
        target = interlist[random.randint(0,interfacetotal-1)]
        builder.createInterfaceRealization('interreal',source,target)

def randomAssociation(builder,list):
    for i in range(associationtotal):
        end1 = random.choice(list)
        end2 = random.choice(list)
        builder.createAssociation('asso','public','public',end1,end2)

def randomData(file):
    with ModelBuilder('random',file) as builder:
        classlist = []
        interfacelist = []
        randomParent(classtotal,builder,classlist,makeClassName,builder.createClass,True)
        randomParent(interfacetotal,builder,interfacelist,makeInterfaceName,builder.createInterface,False)
        randomGen(builder,geneclasstotal,classlist,classtotal)
        randomGen(builder,geneintertotal,interfacelist,interfacetotal)
        randomRealization(builder,classlist,interfacelist)
        randomAssociation(builder,classlist+interfacelist)
        model = builder.getModel()
    return model
        
class randomUmlMake:
    def __init__(self,file):
        self._file = open(file,'w')

    def __enter__(self):
        return (randomData(self._file),self._file)

    def __exit__(self, exc_type, exc_value, exc_tb):
        self._file.close()