from model import *

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