from Model import DTLZ1,DTLZ3,DTLZ5,DTLZ7,Schaffer,Osyczka2,Kursawe,Golinski
from SimulatedAnnealing import SimulatedAnnealing as sa
from MaxWalkSat import MaxWalkSat as mws
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
    
    numOfIterations = 20
    numOfDecisions=[10,20,40]
    numOfObjectives=[2,4,6,8]
    numOfModels = 4
    '''
    numOfIterations = 2
    numOfDecisions=[10]
    numOfObjectives=[4,2]
    numOfModels = 2
    '''
    rdivlength = len(numOfDecisions) * len(numOfObjectives) * numOfModels
    #print rdivlength
    rdivInput = [[] for i in range(rdivlength)]
    rdivIndex = 0
    
    TotalRounds = len(numOfDecisions) * len(numOfObjectives) * numOfIterations
    fname = "./data/CODE9_output_dump.log"

    #for model in [DTLZ7,DTLZ1]:
    for model in [DTLZ1,DTLZ3,DTLZ5,DTLZ7]:
        
        mod = ( "Model    : %s " %model.__name__)
        for Algorithm in [ga]:
            algo = ("Algorithm: %s " %Algorithm.__name__)
            ########ouputRawFile.write(algo)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print "\nStart Time = ", time 
            ####ouputRawFile.write( '\nStart Time = ' +  time + '\n' ) 
            ####ouputRawFile.write( '|||||||||||||||||||||||||||||||||||||||||||||\n' )
            print "###################################################################################"
            print mod
            print "###################################################################################"
            print "Number of Iterations : " ,numOfIterations
            perc = 1.0
            for objectives in numOfObjectives:
                print "\nStarting processing for number of objectives  =", objectives

                for decisions in numOfDecisions:
                    print "\nStarting processing with number of decisions = " ,decisions
                    
                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    ####ouputRawFile.write( '*********************************\n' ) 
                    ####ouputRawFile.write( 'Start Time = ' +  time + '\n' ) 
                    ####ouputRawFile.write( 'Number of objectives : ' + repr(objectives) + '\n' ) 
                    ####ouputRawFile.write( 'Number of decisions  : ' + repr(decisions) + '\n' ) 
                    ####ouputRawFile.write( '*********************************\n' ) 

                    i = 1
                    HV =[]
                    nPF=[]
                    PF =[]
                    
                    for k in xrange(numOfIterations):
                        ####ouputRawFile.write( '================================\n' ) 
                        stime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        ####ouputRawFile.write( 'ITERATION NUMBER = ' + repr(i) + '\n' )
                        print "ITERATION:",k," Start Time:", strftime("%Y-%m-%d %H:%M:%S", gmtime())

                        DifferentSeeds=random.randint(0,10000)
                        print "DifferentSeeds:",DifferentSeeds
                        print "decisions",decisions
                        print "objectives",objectives
                        paretoFront,HyperVolume=Algorithm(model,decisions=decisions,objectives=objectives,someSeed=DifferentSeeds)
                        ####ouputRawFile.write( '================================\n' ) 
       
                        progress = (float(perc)/TotalRounds)*100.0
                        print "\nprocessing: %6.2f" %progress,"% Complete...........\n"

                        ##Collect data for this Decision/objective pair
                        HV.append(HyperVolume)
                        nPF.append(len(paretoFront))
                        PF.append(paretoFront)
                        i += 1
                        perc +=1
                    
                    ##Print data for this Decision/objective pair
                    #print "----------------------------------------------------------------"
                    #print "Finished processing ",model.__name__," with Decisions = ",decisions," and  Objectives = ",objectives
                    #print "List of Points in pareto Frontier in each iteration = ",nPF
                    #print "HyperVolume= ",HV

                    #################
                    ID = (model.__name__+' '+str(decisions)+'-Decisions '+str(objectives)+'-Objectives') 

                    rdivInput[rdivIndex].append(ID)
                    for each in HV:
                        rdivInput[rdivIndex].append(each)
                    rdivIndex += 1
                    ################

            print "----------------------------------------------------------------"
            print "Processing 100% Complete for model: ",model.__name__,"!!!!"
            print "----------------------------------------------------------------"
    rdivDemo(rdivInput)        
    ####ouputRawFile.close()  # Close opend file  
    