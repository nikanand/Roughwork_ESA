import Model
import math
import random
import copy
import sk

def MaxWalkSat(model):
    
    # print "Model : ",model.__name__
    eval=0
    evalx=0
    maxtries=100
    maxchanges=50
    threshold=-10000
    p=0.5
    step=10

    lives = 5
    currentEra = []
    previousEra = []
    eraLength = 10

    for i in range(0,maxtries):
        s=model()
        if i==0:
            sbest=model()
            sbest=copy.deepcopy(s)
            for _ in xrange(s.objectives):
                currentEra.append([])
                previousEra.append([])
        for j in range(0,maxchanges):
            eval+=1
            if s.eval()<threshold:# and len(previousEra) == eraLength:
                return sbest.x,sbest.getObjectives(),sbest.eval()

            which=random.randint(0,s.decisions-1)
            score_old=s.eval()
            if p<random.random():
                s=neighbor(s,which,model)
            else:
                s=optc(s,which,step,model)

            if type1(s, sbest):
                sbest=copy.deepcopy(s)
                evalx=eval

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

    return sbest.x,sbest.getObjectives(),sbest.eval()
 
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


def optc(s,index,step,model):
    sn=model()
    sn=copy.deepcopy(s)
    snbest=model()
    snbest=copy.deepcopy(sn)
    dis=(sn.domainMax[index]-sn.domainMin[index])/step
    if dis != 0:
        for i in range(-int((s.x[index]-s.domainMin[index])/dis),int((s.domainMax[index]-s.x[index])/dis)+1):
            sn.x[index]=sn.x[index]+i*dis
            if not sn.constraints(): continue
            if sn.eval()<snbest.eval():
                snbest=copy.deepcopy(sn)
    return snbest
    
def neighbor(s,index,model):
    sn=model()
    sn=copy.deepcopy(s)
    while True:
        sn.x[index]=random.uniform(sn.domainMin[index],sn.domainMax[index])
        if sn.constraints(): break
    return sn
