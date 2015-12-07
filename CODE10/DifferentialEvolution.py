import Model
import math
import random
import copy
import numpy
import sk

def DifferentialEvolution(model):
    # print "Model: ",model.__name__

    F=0.75
    CR=0.3
    maxtries=10
    NumCandidates=100
    best=model()
    candidates=[best]
    
    lives = 5
    currentEra = []
    previousEra = []
    for _ in xrange(best.objectives):
        currentEra.append([])
        previousEra.append([])
    eraLength = 1*NumCandidates

    
    for i in range(1,NumCandidates):
        candidate=model()
        candidates.append(candidate)
        if type1(candidate, best):
            best=copy.deepcopy(candidate)
    # print "Number Of Candidates:", len(candidates)      
    # print "Best Before TRIES in List of candidates:",best.x
    
    def mutate(candidates,F,CR,best):
        for i in range(len(candidates)):
            tmp=range(len(candidates))
            tmp.remove(i)
            while True:
                choice=numpy.random.choice(tmp,3)
                X = candidates[choice[0]]
                Y = candidates[choice[1]]
                Z = candidates[choice[2]]
                
                old=candidates[i]
                r=random.randint(0,old.decisions-1)
                new=model()
                for j in range(old.decisions):
                    if random.random()<CR or j==r:
                        new.x[j]=X.x[j] + F*(Y.x[j] - Z.x[j])  #Mutate: X + F*(Y - Z)
                    else:
                        new.x[j]=old.x[j]
                if new.constraints(): break
            if type1(new, best):
                best=copy.deepcopy(new)
            elif (not type1(new, old)):
                new=old
            yield new,best

    for tries in range(maxtries):
        newcandidates = []
        for new,best in mutate(candidates,F,CR,best):
            newcandidates.append(new)
        candidates = newcandidates

        if (len(currentEra[0]) < eraLength):
            for tempVal in candidates:
                temp = tempVal.getObjectives()
                for _ in xrange(0,len(temp)):
                    currentEra[_].append(temp[_])
        else:
            if (previousEra[0] != []):
                for _ in xrange(0,len(previousEra)):
                    lives += type2(previousEra[_], currentEra[_])
                if (lives <= 0):
                    break
            for _ in xrange(0,len(currentEra)):
                previousEra[_] = list(currentEra[_])
            currentEra = []

            for _ in xrange(0,len(previousEra)):
                currentEra.append([]) 

    return best.x,best.getObjectives(),best.eval()

def gt(x,y): return x > y
def lt(x,y): return x < y

def type1(model1, model2):
    bettered = False
    for i,(xi,yi) in enumerate(zip(model1.getObjectives(),model2.getObjectives())):
        if lt(xi,yi):
            bettered = True
        elif (xi != yi): 
            return False # not better and not equal, therefor worse
    return bettered


#def type1(model1, model2):
#    return (model1.eval() < model2.eval())
    
def type2(list1, list2):

    if (sk.a12(list1, list2) <= 0.56):
        return -1
    else:
        return 5
