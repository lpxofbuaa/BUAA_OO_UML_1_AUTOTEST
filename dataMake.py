from randomUmlMake import randomUmlMake
from randomUmlMake import methodsName
import sys

def createClassCount():
    return 'CLASS_COUNT'

def createClassOpCount(className):
    modes = ['NON_RETURN','RETURN','NON_PARAM','PARAM','ALL']
    result = []
    for i in modes:
        result.append('CLASS_OPERATION_COUNT '+className+' '+i)
    return result

def createClassAttrCount(className):
    modes = ['ALL','SELF_ONLY']
    result = []
    for s in modes:
        result.append('CLASS_ATTR_COUNT '+className+' '+s)
    return result

def createClassAssoCount(className):
    return 'CLASS_ASSO_COUNT '+className

def createClassAssoClassList(className):
    return 'CLASS_ASSO_CLASS_LIST '+className

def createOpVisibility(className,methodName):
    return 'CLASS_OPERATION_VISIBILITY '+className+' '+methodName

def createAttrVisibility(className,AttrName):
    return 'CLASS_ATTR_VISIBILITY '+className+' '+AttrName

def createClassTop(className):
    return 'CLASS_TOP_BASE '+className

def createImpleInterList(className):
    return 'CLASS_IMPLEMENT_INTERFACE_LIST '+className

def createInfoHidden(className):
    return 'CLASS_INFO_HIDDEN '+className 

def dataMake(count='1'):
    instrs = []
    with randomUmlMake(count) as m:
        model = m[0]
        datafile = m[1]
        classidMap = model.getClass()
        interfaceidMap = model.getInterface()
        instrs.append(createClassCount())
        for i in classidMap:
            className = classidMap[i]
            instrs.extend(createClassOpCount(className))
            instrs.extend(createClassAttrCount(className))
            instrs.append(createClassAssoCount(className))
            instrs.append(createClassAssoClassList(className))
            instrs.append(createClassTop(className))
            instrs.append(createImpleInterList(className))
            instrs.append(createInfoHidden(className))
            classid = i
            methods = list(methodsName)
            for method in methods:
                instrs.append(createOpVisibility(className,method))
            attrnames = []
            while (classid != None):
                attrnames.extend(model.getClassAttributes(classid))
                classid = model.getClassParentId(classid)
            attrnames = set(attrnames)
            for s in attrnames:
                instrs.append(createAttrVisibility(className,s))
        for i in range(len(instrs)):
            if (i != len(instrs)-1):
                datafile.write(instrs[i]+'\n')
            else:
                datafile.write(instrs[i])

if __name__ == "__main__":
    if (len(sys.argv)<2):
        dataMake()  
    else:
        dataMake(sys.argv[1])



        
    
