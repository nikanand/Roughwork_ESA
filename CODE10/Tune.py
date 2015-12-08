import Model
import math
import random
import copy
import numpy
import sk

from Model import GAtune,DTLZ1,DTLZ3,DTLZ5,DTLZ7,Schaffer,Fonseca,Osyczka2,Kursawe,Golinski
#from DifferentialEvolution import DifferentialEvolution as de
from GeneticAlgorithm import GeneticAlgorithm as ga
from PT import PrettyTable
from time import gmtime, strftime


def deTuner(model,what,decisions,objectives):
    ###$print "\nTuner: ",model.__name__
    ###$print "Tuning: ",what.__name__

    F=0.75
    CR=0.3
    maxtries=10
    NumCandidates=10
    
    best=model(what,decisions,objectives)
    ###$print "\n Runing ",best.__name__
    
    candidates=[best]
    ###$print "First Candidate Value:",candidates[0].x
    
    for i in range(1,NumCandidates):
        #print "\nCANDIDATE NUMBER: ",i
        candidate=model(what,decisions,objectives)
        candidates.append(candidate)
        ###$print "candidate is",candidate.__name__
        ###$print "best is",best.__name__
        if candidate.eval()<best.eval():
            ###$print"updating best"
            best=copy.deepcopy(candidate)
    ####$print "Number Of Candidates:", len(candidates)      
    ####$print "Best Before TRIES in List of candidates:",best.x
    
    def mutate(candidates,F,CR,best):
        ###$print "length:::",len(candidates)
        for i in range(len(candidates)):
           # print "Len::",len(candidates)
            #print "i = ",i
            tmp=range(len(candidates))
            tmp.remove(i)
            while True:
                choice=numpy.random.choice(tmp,3)
                ####$print "choice",choice
                X = candidates[choice[0]]
                Y = candidates[choice[1]]
                Z = candidates[choice[2]]
                
                old=candidates[i]
                #print "~~~~old",old.x
                r=random.randint(0,old.decisions-1)
                #print"@@@@@@"
                new=model(what,decisions,objectives)
                
                for j in range(old.decisions):
                    if random.random()<CR or j==r:
                        new.x[j]=int(round(X.x[j] + F*(Y.x[j] - Z.x[j])))  #Mutate: X + F*(Y - Z)
                    else:
                        new.x[j]=old.x[j]
                if new.constraints(): 
                    #print "Breaking..."
                    break
            
            #print "\n------------"
            a = new.eval()
            b = best.eval()
            c = old.eval()
            #print "\n------------"

            if a<b:
                best=copy.deepcopy(new)
                #printList.append("!")
                #printList.append (str(best.x)) ##New Best Found
            elif a<c:
                #printList.append("+")
                new=new
            elif a==c:
                new=new
                #printList.append("?")
            else:
                new=old
                #printList.append(".")
            ####$print "~~~~new",new.x
            yield new,best

    for tries in range(maxtries):
       # print "\nTry: ",tries+1

        newcandidates = []
        for new,best in mutate(candidates,F,CR,best):
            newcandidates.append(new)
        candidates = newcandidates
    ###$print "Best Candidate Value:",best.x
    return best.x



def TuneGAparametersUsingDE(model,decisions=0,objectives=0):

    if decisions==0 or objectives==0:
        ###$print "ISSUE with tuning parameters"
        return 

    for tuner in [GAtune]:
        ###$print "Tuning Start"
        ###$print "Tuner",tuner.__name__

        
        decs = deTuner(tuner,model,decisions,objectives)
        
        ###$print "Tuning Done"
        
        ###$print "Best decisionss: "
        ###$print "~~~~~~~~~~~~~~~~~~~~~"
        ###$print decisions
    
        lives = decs[0]
        mutationRate = decs[1]
        candidates = decs[2]
    
        ###$print "Lives         = %02d" %lives
        ###$print "mutation Rate = %02d" %mutationRate
        ###$print "Candidates    = %02d" %candidates
    
        return lives,mutationRate,candidates
    
    
    
    



    