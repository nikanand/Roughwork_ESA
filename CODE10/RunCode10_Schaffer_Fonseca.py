from Model import GAtune,DTLZ1,DTLZ3,DTLZ5,DTLZ7,Schaffer,Fonseca,Osyczka2,Kursawe,Golinski
from SimulatedAnnealing import SimulatedAnnealing as sa
from MaxWalkSat import MaxWalkSat as mws
from Tune import TuneGAparametersUsingDE as TuneGAparametersUsingDE
from DifferentialEvolution import DifferentialEvolution as de
from GeneticAlgorithm import GeneticAlgorithm as ga
from sk import rdivDemo
from PT import PrettyTable
from time import gmtime, strftime

#####################
import random
initSeed = 30
random.seed(initSeed)
#####################

if __name__ == '__main__':
    '''
    numOfIterations = 20
    numOfDecisions=[10,20,40]
    numOfObjectives=[2,4,6,8]
    numOfModels = 4
    '''
    numOfIterations = 20

    rdivlength = 2
    rdivInput = [[],[]]
    rdivIndex = 0
    
    fname = ('./data/CODE10_Schaffer_Fonseca.log')
    fo = open(fname, "wb")
    
    #for model in [DTLZ1,DTLZ3,DTLZ5,DTLZ7]:
    for model in [Schaffer,Fonseca]: 
        mod = ( "Model    : %s " %model.__name__)
        
        if model.__name__ == "Schaffer":
            numOfDecisions = [1]
            numOfObjectives = [2]
        elif model.__name__ == 'Fonseca':
            numOfDecisions = [3]
            numOfObjectives =[2]
        else:
            print "wrong model"
            break
            
        
        time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
        print "\nStart Time = ", time 
        
        fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
        fo.write('Model    : '+ model.__name__ + '\n')    
        fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
        
        print "###################################################################################"
        print mod
        print "###################################################################################"
        print "Number of Iterations : " ,numOfIterations

        for objectives in numOfObjectives:
            print "\nStarting processing for number of objectives  =", objectives

            for decisions in numOfDecisions:
                print "\nStarting processing with number of decisions = " ,decisions
                
                #print "start tuner..."
                TunedLives,TunedMutationRate,TunedCandidates = TuneGAparametersUsingDE(model,decisions=decisions,objectives=decisions)          
                "Printing Tuned paramenters"
                #print "Tuned:[Lives,MutationRate,Candidates]=",TunedLives,TunedMutationRate,TunedCandidates
                
                i = 1
                HV =[]
                PF =[]
                tunedHV=[]
                tunedPF=[]
                #print "Iteration...."
                for k in xrange(numOfIterations):
                    print k,
                    DifferentSeeds=random.randint(0,10000)
                         
                    paretoFront,HyperVolume=ga(model,decisions=decisions,objectives=objectives,someSeed=DifferentSeeds,candidates=100,generations=1000,mutationRate=0.05,lives=5)
                    #print " START TUNED ONE...................."
                    tunedPF,tunedHyperVolume=ga(model,decisions=decisions,objectives=objectives,someSeed=DifferentSeeds,candidates=TunedCandidates,generations=1000,mutationRate=TunedMutationRate,lives=TunedLives)

                    HV.append(HyperVolume)
                    PF.append(paretoFront)
                    tunedHV.append(tunedHyperVolume)
                    tunedPF.append(tunedPF)
                    i += 1
                    #print k," ITERATIONs DONE...................."

                #Print data for this Decision/objective pair
                print ""
                print "----------------------------------------------------------------"
                print "Finished processing ",model.__name__," with Decisions = ",decisions," and  Objectives = ",objectives
                fo.write('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                fo.write('Finished processing '+str(model.__name__)+' with Decisions = '+repr(decisions)+' and  Objectives = '+repr(objectives)+'\n')
                fo.write('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                print "List of Points in pareto Frontier in each iteration without tuning = ",len(PF)
                #print "HyperVolume      = ",HV
                print "List of Points in pareto Frontier in each iteration with tuning    = ",len(tunedPF)
                #print "Tuned HyperVolume= ",tunedHV             
                   
            ################
                #table print
                Table = PrettyTable()
                sNo = range(1,numOfIterations + 1)
                Table.add_column("Iteration  ",sNo)
                Table.add_column("Original Value",HV)
                Table.add_column("Tuned Value",tunedHV)
                print Table
                fo.write( str(Table) + '\n' )
                fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
            
            ################
                ID1 = (model.__name__+' untuned   ')#+str(decisions)+'-Decisions '+str(objectives)+'-Objectives') 
                ID2 = (model.__name__+' tuned     ')#+str(decisions)+'-Decisions '+str(objectives)+'-Objectives') 


                rdivInput[rdivIndex].append(ID1)
                for each in HV:
                    rdivInput[rdivIndex].append(each)
                rdivIndex += 1

                rdivInput[rdivIndex].append(ID2)
                for each in tunedHV:
                    rdivInput[rdivIndex].append(each)
                rdivIndex += 1
            
                ranks = rdivDemo(rdivInput) 
                
                '''
                print "\nranks",ranks
                print ""
                print ranks[0][0] 
                print ranks[1][0] 
                print ranks[0][1]
                print ranks[1][1] 
                print ""
                '''
                fo.write('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                if ranks[0][1] >= ranks[1][1] :
                    print "No improvement"
                    fo.write('No improvement\n')
                else :
                    print "Visible improvement"
                    fo.write('Visible improvement\n' )
                fo.write('++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++\n')
                fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
                ################
                rdivIndex = 0
                rdivInput = [[],[]]
                

        print "----------------------------------------------------------------"
        print "Processing 100% Complete for model: ",model.__name__,"!!!!"
        print "----------------------------------------------------------------"
        
    fo.close()
           
