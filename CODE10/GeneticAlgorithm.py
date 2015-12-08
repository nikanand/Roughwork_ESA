import Model
import math
import random
import copy
import numpy
import sk
from time import gmtime, strftime



'''
"As per Code 9-10 details"
candidates=100
generations=1000
mutationRate=0.05
lives=5
'''

"Run Baseline"
def baseline(model,decisions=10,objectives=2,num=10000):
    #print"model :",model.__name__
    setOfCandidates=[model(objectives,decisions) for _ in xrange(num)]
    

    maxi = []
    mini = []
    for i in range(objectives) :
        list1=[]
        for each in setOfCandidates:
            
            list1.append(each.fx[i])

        mini.append(numpy.min(list1))
        maxi.append(numpy.max(list1))
  
    return mini,maxi


"Genetically Crossover parents"
def crossover(child,Parent1,Parent2):
    while True:
        x=random.randint(0,len(Parent1.x))
        X = list(numpy.array(Parent1.x)[:x])
        Y = list(numpy.array(Parent2.x)[x:])
        child.x= X + Y
        if child.constraints():
            return child

"Denfing types"

def gt(x,y): return x > y
def lt(x,y): return x < y 

"Check Binary Domination"
#type 1
def binaryDomination(model1, model2):
    bettered = False
    for i,(xi,yi) in enumerate(zip(model1.fx,model2.fx)):

        if lt(xi,yi):
            bettered = True
        elif (xi != yi):
            return False # not better and not equal, therefor worse
    return bettered

"Update pareto frontier"
#type2
def updateParetoFrontier(bestPF,newPF,lives):
    tmpCandList=[]
    for cand1 in newPF:
        for cand2 in bestPF:
            #print "cand1.fx",cand1.fx
            #print "cand2.fx",cand2.fx
            lives+=type2(cand2.fx,cand1.fx)
            if lives == 0:
                return lives
            if binaryDomination(cand1,cand2):
                if cand1 not in tmpCandList:
                    tmpCandList.append(cand1)
                    bestPF.remove(cand2)
                    
    if tmpCandList:
        bestPF.extend(tmpCandList)
    return lives


        
        
def type2(list1, list2):

    if (sk.a12(list1, list2) <= 0.56):
        return -1
    else:
        return 5
        
"True if samples dominated by the front"
def Dominates(pfPoint,someObjectives):
    pfObjectives=pfPoint.fx
    if pfObjectives==someObjectives:
        return False
    for i in xrange(pfPoint.objectives):
        if someObjectives[i]<pfObjectives[i]:
            return False
    return True

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
    m=paretoFront[0].objectives

    for i in xrange(sample):
        someObjectives = []

        for j in xrange(m):
            xyz = random.uniform(min[j],max[j])
            someObjectives.append(xyz)


        for pfPoint in paretoFront:

            if Dominates(pfPoint,someObjectives):
                 count=count+1
                 break
        
        #print "Num=",count  
        #print "DEM=",i
        
    #print "HV is        == ",float(count/(sample))   
    #print "HV should be ==",float(gen * 100 - len(paretoFront)) / (gen * 100)
    
    return float(count/(sample))

"Start of GA"
def GeneticAlgorithm(model,decisions=4,objectives=2,someSeed=30,candidates=100,generations=1000,mutationRate=0.05,lives=5):
    #print "Start of GA"
    #print "someSeed=",someSeed
    random.seed(someSeed)
    min,max=baseline(model,decisions=decisions,objectives=objectives,num=10000)


    listOfCandidates=[model(objectives,decisions) for _ in xrange(candidates)]

    PF=[]
    for cand1 in listOfCandidates:
        flag=True
        for cand2 in listOfCandidates:
            if binaryDomination(cand2,cand1):
                flag=False
                break
        if flag:
            PF.append(cand1)
    bestPF=PF[:]
    #print "lives = ",lives,
    for i in xrange(generations):
        
        newCandidateList=[]
        for j in xrange(candidates):
            child=model(objectives,decisions)
            choose=numpy.random.choice(len(PF),2,replace=True)
            Parent1=PF[choose[0]]
            Parent2=PF[choose[1]]
            child = crossover(child,Parent1,Parent2) #"Genetically Crossover parents"

            if random.random()<mutationRate:#
                child.setDecisions() #Genetically mutate child

            newCandidateList.append(child)
            
        newPF=[]
        
        for cand1 in listOfCandidates:
            flag=True
            for cand2 in listOfCandidates:
                if binaryDomination(cand2,cand1):
                    flag=False
                    break
            if flag:
                newPF.append(cand1)

        lives=updateParetoFrontier(bestPF,newPF,lives)
        #print "... ",lives,
        if lives == 0:
            lives = 5
            break

        listOfCandidates=newCandidateList
        pf=newPF
        #print "pf count = ",len(pf)
    #print "DONE"
    HyperVolume = hypervolume(bestPF,min,max,10000)
    
    return bestPF,HyperVolume
