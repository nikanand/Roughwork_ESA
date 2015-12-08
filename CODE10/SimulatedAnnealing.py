import Model
import math
import random
import copy
import sk
#import loss

def SimulatedAnnealing(model):
    # print "Model: ",model.__name__
    s=model()
    sb=model()
    sb=copy.deepcopy(s)
    k = 1
    kMax=1000
    
    lives = 5 
    era0 = []
    currentEra = []
    previousEra = []
    for _ in xrange(s.objectives):
        currentEra.append([])
        previousEra.append([])
        era0.append([])
    eraLength = 25
    
    while (k <= kMax):
        sn=neighbor(s,random.randint(0,s.decisions-1),model)
        if (type1(sn,sb)):
            sb=copy.deepcopy(sn)
            s=copy.deepcopy(sn)
        elif (type1(sn, s)):
            s=copy.deepcopy(sn)
        elif (probability(sn.eval(),s.eval(),(k/kMax))<random.uniform(0,1)):
            s=copy.deepcopy(sn)

        k = k + 1
       
        # Type 2 comparator
        if (len(currentEra[0]) < eraLength):
            tempVal = s.getObjectives()
            for _ in xrange(0,len(tempVal)):
                currentEra[_].append(tempVal[_])
 
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
                  
    return sb.x,sb.getObjectives(),sb.eval()

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
    
def neighbor(s,index,model):
    sn=model()
    sn=copy.deepcopy(s)
    while True:
        sn.x[index]=random.uniform(sn.domainMin[index],sn.domainMax[index])
        if sn.constraints(): break
    return sn
    
def probability(en,e,t):
        if t != 0:
            return math.exp((e - en )/t)
