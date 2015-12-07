import Model
import math
import random
import copy
import numpy
import sk
from time import gmtime, strftime




"As per Code 9-10 details"
candidates=100
generations=1000
mutationRate=0.05
lives=5


"Run Baseline"
def baseline(model,decisions=10,objectives=2,num=10000):
    #print"model :",model.__name__
    setOfCandidates=[model(objectives,decisions) for _ in xrange(num)]
    

    maxi = []
    mini = []
    for i in range(objectives) :
        list1=[]
        for each in setOfCandidates:
            ####$print each
            ####$print len(each.getObjectives())
            #list1.append(each.getObjectives()[i])
            list1.append(each.fx[i])

        mini.append(numpy.min(list1))
        maxi.append(numpy.max(list1))
  
    return mini,maxi


"Genetically Crossover parents"
def crossover(child,Parent1,Parent2):
    while True:
        x=random.randint(0,len(Parent1.x))
        ####$print "cut chromosome at index = ",x
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
    #for i,(xi,yi) in enumerate(zip(model1.getObjectives(),model2.getObjectives())):
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
    else:
        return lives
        
        
def type2(list1, list2):

    if (sk.a12(list1, list2) <= 0.56):
        return -1
    else:
        return 5
        
"True if samples dominated by the front"
def Dominates(pfPoint,someObjectives):
    #pfObjectives=pfPoint.getObjectives()
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

    ###$print "calculating hypervolume......"
    for i in xrange(sample):
        someObjectives = []
        for i in xrange(m):
            someObjectives.append(random.uniform(min[i],max[i]))

        for pfPoint in paretoFront:
            if Dominates(pfPoint,someObjectives):
                 count=count+1

    return float(count/(sample))

"Start of GA"
def GeneticAlgorithm(model,decisions=4,objectives=2,someSeed=30,candidates=100,generations=1000,mutationRate=0.05,lives=5):
    
    random.seed(someSeed)
    #########$$$$$$$print "\nstart Baseline:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
    min,max=baseline(model,decisions=decisions,objectives=objectives,num=10000)
    #########$$$$$$$print "end Baseline:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

    
    ###$print "#####model : ",model.__name__
    
    ###$print "Start creating list of candidates"

    listOfCandidates=[model(objectives,decisions) for _ in xrange(candidates)]
    
    ###$print "Length of candidate list:",len(listOfCandidates)
    #########$$$$$$$print "\nstart finding first best:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

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
    #########$$$$$$$print "end :",strftime("%Y-%m-%d %H:%M:%S", gmtime())
    #########$$$$$$$print "$$$$$$$$$$$$Best PF points:",len(bestPF)

    
    life=0
    ###$print "\ngenerations...",
    for i in xrange(generations):
        ###$print i,",",
        newCandidateList=[]
        for j in xrange(candidates):
            child=model(objectives,decisions)
            choose=numpy.random.choice(len(PF),2,replace=True)
            Parent1=PF[choose[0]]
            Parent2=PF[choose[1]]
            #print "\nstart crossover:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
            child = crossover(child,Parent1,Parent2) #"Genetically Crossover parents"
            ##########$$$$print "End:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

            if random.random()<mutationRate:#  *(2**life):
                #########$$$$$$$print "\nstart mmutate:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
                child.setDecisions() #Genetically mutate child
                #########$$$$$$$print "Endnd:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

            newCandidateList.append(child)
            
        newPF=[]
        
        
        #########$$$$$$$print "\nstart finding new pf:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
        for cand1 in listOfCandidates:
            flag=True
            for cand2 in listOfCandidates:
                if binaryDomination(cand2,cand1):
                    flag=False
                    break
            if flag:
                newPF.append(cand1)
                
        #########$$$$print "End:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

        #########$$$$$$$print "\nstart updating:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

        updated=updateParetoFrontier(bestPF,newPF,lives)
        #########$$$$$$$print "$$$$$$$$$$$$Best updates PF points:",len(bestPF)

        if updated == 0:
            #########$$$$$$$print "lives = ",lives," terminating early"
            lives = 5
            #########$$$$print "End:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
            break
        #########$$$$print "End:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

        '''
        if updated:
            life=0
        else:
            life=life+1
        if life==lives:
            break
        '''

        listOfCandidates=newCandidateList
        pf=newPF
    ###$print ""
    #########$$$$$$$print "Start HVcaluculations:",strftime("%Y-%m-%d %H:%M:%S", gmtime())
    HyperVolume = hypervolume(bestPF,min,max,10000)
    #########$$$$$$$print "End:",strftime("%Y-%m-%d %H:%M:%S", gmtime())

    return bestPF,HyperVolume
