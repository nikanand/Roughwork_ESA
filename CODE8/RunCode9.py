from Model import DTLZ1,DTLZ7,Schaffer,Osyczka2,Kursawe,Golinski
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

def PrintAndDumpfile(paretoFront,stime):
    'Print output'
    for i in range(len(paretoFront)):
        xTable = PrettyTable()
        sNo = range(1,paretoFront[i].n + 1)
        xTable.add_column("#",sNo)
        xTable.add_column("decisions, x",paretoFront[i].x)
        #print xTable
        fxTable = PrettyTable()
        sNo = range(1,paretoFront[i].objectives + 1)
        fxTable.add_column("#",sNo)
        fxTable.add_column("objectives,f(x)", paretoFront[i].getObjectives())
        #print fxTable
        ## dump in file
        try:
            ouputRawFile.write( '________________________________\n' ) 
            ouputRawFile.write( 'paretoFrontier# :' + repr(i+1) + '\n' ) 
            ouputRawFile.write( 'objectives = ' +  repr(paretoFront[i].objectives) + '\n' )  # No of objectives f[0]f[1],f[2],...,f[M-1]
            ouputRawFile.write( 'decisions  = ' +  repr(paretoFront[i].decisions) + '\n' )   # decision variables  
            ouputRawFile.write( 'Energy     = ' +  repr(paretoFront[i].eval()) + '\n' )
            ouputRawFile.write( str(xTable) + '\n' )
            ouputRawFile.write( str(fxTable) + '\n' )
            #print "Successfully written in FILE: ",fname
        except:
            print "somthing went wrong while writting in FILE: ",fname
    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
    print "Start Time = ", stime
    print "End Time   = ", time
    ouputRawFile.write( '________________________________\n' ) 
    ouputRawFile.write( 'Start Time = ' +  stime + '\n' )
    ouputRawFile.write( 'End Time   = ' +  time + '\n' )
    ouputRawFile.write( 'Number of values in paretoFrontier = ' + repr(len(paretoFront)) + '\n' )
    ouputRawFile.write( '________________________________\n' ) 

    print "###########################################"

if __name__ == '__main__':
    '''
    numOfIterations = 20
    numOfDecisions=[10,20,40]
    numOfObjectives=[2,4,6,8]
    '''
    numOfIterations = 2
    numOfDecisions=[10]
    numOfObjectives=[2,4,6,8]
    
    solutions={}
    TotalRounds = len(numOfDecisions) * len(numOfObjectives) * numOfIterations
    fname = "./data/OUTPUT-RAWDATA.txt"
    ouputRawFile = open(fname, "wb") 
    
    for model in [DTLZ1,DTLZ7]:
        ouputRawFile.write( '|||||||||||||||||||||||||||||||||||||||||||||\n' )
        mod = ( "Model    : %s " %model.__name__)
        ouputRawFile.write(mod+'\n')
        solutions[model.__name__]={}
        for Algorithm in [ga]:
            algo = ("Algorithm: %s " %Algorithm.__name__)
            ouputRawFile.write(algo)
            time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
            print "\nStart Time = ", time 
            ouputRawFile.write( '\nStart Time = ' +  time + '\n' ) 
            ouputRawFile.write( '|||||||||||||||||||||||||||||||||||||||||||||\n' )
            print "###################################################################################"
            print mod
            print "###################################################################################"
            print "Number of Iterations : " ,numOfIterations
            perc = 1.0
            for objectives in numOfObjectives:
                solutions[model.__name__][objectives]={}
                for decisions in numOfDecisions:
                    
                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    ouputRawFile.write( '*********************************\n' ) 
                    ouputRawFile.write( 'Start Time = ' +  time + '\n' ) 
                    ouputRawFile.write( 'Number of objectives : ' + repr(objectives) + '\n' ) 
                    ouputRawFile.write( 'Number of decisions  : ' + repr(decisions) + '\n' ) 
                    ouputRawFile.write( '*********************************\n' ) 
                    
                    print '*********************************'
                    print "Number of objectives : ", objectives
                    print "Number of decisions  : " ,decisions
                    print "Start Time = ", time
                    print '*********************************\n'

                    solutions[model.__name__][objectives][decisions]=[]
                    i = 1
                    for k in xrange(numOfIterations):
                        
                        ouputRawFile.write( '================================\n' ) 
                        stime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        print "ITERATION NUMBER : ", i
                        ouputRawFile.write( 'ITERATION NUMBER = ' + repr(i) + '\n' )

                        DifferentSeeds=random.randint(0,10000)
                         
                        paretoFront,HyperVolume=Algorithm(model,decisions=decisions,objectives=objectives,someSeed=DifferentSeeds)
                        PrintAndDumpfile(paretoFront,stime)
                        ouputRawFile.write( '================================\n' ) 
       
                        progress = (float(perc)/TotalRounds)*100.0
                        print "\nprocessing: %6.2f" %progress,"% Complete...........\n"
                        solutions[model.__name__][objectives][decisions].append(HyperVolume)
                        i += 1
                        perc +=1
                    
            print "----------------------------------------------------------------"
            print "Processing 100% Complete for model",model.__name__,"!!!!"
            print "----------------------------------------------------------------"
            ####################
            'Print output'
            print "\nBest solutions: "
            print "######################"
            print solutions
            print "######################"
            try:
                fname = ('./data/'+Algorithm.__name__+'_'+model.__name__+'.txt')
                fo = open(fname, "wb")  # Open a file
                fo.write(repr(solutions))
                fo.close()  # Close opend file  
                print "Successfully written in FILE: ",fname
            except:
                print "somthing went wrong while writting in FILE: ",fname
    
    
    ouputRawFile.close()  # Close opend file  

