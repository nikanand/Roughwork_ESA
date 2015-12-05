#from __future__ import absolute_import, division
import Model
import math
import random
import copy
import numpy
import sk
#import os
#from PT import PrettyTable
#from time import gmtime, strftime


"As per Code 9-10 details"
candidates=100
generations=1000
mutation_rate=0.05
lives=5


"Run Baseline"
def baseline(model,decisions=10,objectives=2,num=10000):
    setOfCandidates=[model(objectives,decisions) for _ in xrange(num)]

    maxi = []
    mini = []
    for i in range(objectives) :
        list1=[]
        for each in setOfCandidates:
            list1.append(each.getObjectives()[i])
        mini.append(numpy.min(list1))
        maxi.append(numpy.max(list1))
  
    return mini,maxi


"Genetically Crossover parents"
def crossover(child,Parent1,Parent2):
    while True:
        x=random.randint(0,len(Parent1.x))
        #print "cut chromosome at index = ",x
        X = list(numpy.array(Parent1.x)[:x])
        Y = list(numpy.array(Parent2.x)[x:])
        child.x= X + Y
        if child.constraints():
            return child

"Denfing types"

def gt(x,y): return x > y
def lt(x,y): return x < y 

"Update pereto frontier"

def compete(pf_best,pf_new):
    tmp=[]
    for a in pf_new:
        for b in pf_best:
            if binaryDomination(a,b):
                tmp.append(a)
                pf_best.remove(b)
    if tmp:
        pf_best.extend(tmp)
        return True
    else:
        return False
        
        
def type2(list1, list2):

    if (sk.a12(list1, list2) <= 0.56):
        return -1
    else:
        return 5

        
"Check Binary Domination"
def binaryDomination(Parent1,Parent2):
    try:
        obj_a=Parent1.getObjectives()
    except:
        obj_a=Parent1
    try:
        obj_b=Parent2.getObjectives()
    except:
        obj_b=Parent2
    if obj_a==obj_b:
        return False
    for i in xrange(Parent1.objectives):
        if obj_b[i]<obj_a[i]:
            return False
    return True

    
def type1(model1, model2):
    bettered = False
    for i,(xi,yi) in enumerate(zip(model1.getObjectives(),model2.getObjectives())):
        if lt(xi,yi):
            bettered = True
        elif (xi != yi): 
            return False # not better and not equal, therefor worse
    return bettered

    

    
    
'''
Approximates the hypervolume of a Pareto frontier. First, it generates 
random samples in the hypercuboid defined by the utopia and antiutopia 
points. Second, it counts the number of samples dominated by the front. 
The hypervolume is approximated as the ratio 'dominated points / total 
points'. 
Inputs: 
- paretoFront: the Pareto front to evaluate 
- min: antiutopia point 
- max: utopia point 
- number of sample for the approximation
Outputs: 
- hv : hypervolume = count/(sample)
REFERENCE: http://www.mathworks.com/matlabcentral/fileexchange/50517-hypervolume-approximation


SAMPLE SIZE:

Hypervolume-Based Search for Multiobjective Optimization: Theory and Methods 
PAGE: 138 : 
10000 samples are required to get error rate less than 5%

REFERENCE: https://books.google.com/books?id=6K3zflc_bNkC&pg=PA138&lpg=PA138&dq=how+many+choose+sample+size+for+hypervolume+calculation&source=bl&ots=ZlqfiANho3&sig=CHWzgRpvzqj3A7H1J21OnP8FHpw&hl=en&sa=X&ved=0ahUKEwiXwOPyp8HJAhUK6SYKHe93C-MQ6AEIMjAD#v=onepage&q=how%20many%20choose%20sample%20size%20for%20hypervolume%20calculation&f=false
'''
def hypervolume(paretoFront,min,max,sample=10000):
    count=0.0    
    #print "!!!!!!! Number of solutions in paretoFront = ",len(paretoFront)
    m=paretoFront[0].objectives
    for i in xrange(sample):
        #print "Sample number",i
        #print "!!!!!!! len: min =",len(min)," max =",len(max)
        #someValue=[random.uniform(min[k],max[k]) for k in xrange(m)]
        
        someValue = []
        for i in xrange(m):
            someValue.append(random.uniform(min[i],max[i]))

        for value in paretoFront:
             if binaryDomination(value,someValue):
                 count=count+1

    return float(count/(sample))

"Start of GA"
def GeneticAlgorithm(model,decisions=4,objectives=2,someSeed=30):
    random.seed(someSeed)
    min,max=baseline(model,decisions=decisions,objectives=objectives,num=10000)
    listOfCandidates=[model(objectives,decisions) for _ in xrange(candidates)]

    
    pf=[]
    for cand1 in listOfCandidates:
        flag=True
        for cand2 in listOfCandidates:
            if binaryDomination(cand2,cand1):
                flag=False
                break
        if flag:
            pf.append(cand1)
    pf_best=pf[:]
    
    
    life=0
    for i in xrange(generations):
        can_new=[]
        for j in xrange(candidates):
            child=model(objectives,decisions)
            choose=numpy.random.choice(len(pf),2,replace=True)
            Parent1=pf[choose[0]]
            Parent2=pf[choose[1]]
            child = crossover(child,Parent1,Parent2)

            if random.random()<mutation_rate*(2**life):
                child.setDecisions() #Genetically mutate child
            can_new.append(child)
            
        pf_new=[]
        for a in listOfCandidates:
            flag=True
            for b in listOfCandidates:
                if binaryDomination(b,a):
                    flag=False
                    break
            if flag:
                pf_new.append(a)
                
        change=compete(pf_best,pf_new)
        if change:
            life=0
        else:
            life=life+1
        if life==lives:
            break

        listOfCandidates=can_new
        pf=pf_new
    
    solution = hypervolume(pf_best,min,max,10000)
    return pf_best,solution
