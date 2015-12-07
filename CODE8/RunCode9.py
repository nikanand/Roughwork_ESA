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




def Dumpfile(paretoFront,stime):
    for i in range(len(paretoFront)):
        xTable = PrettyTable()
        sNo = range(1,paretoFront[i].N + 1)
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
    ouputRawFile.write( '_________Time Estimate___________\n' ) 
    ouputRawFile.write( 'Start Time = ' +  stime + '\n' )
    ouputRawFile.write( 'End Time   = ' +  time + '\n' )
    ouputRawFile.write( 'Number of values in paretoFrontier = ' + repr(len(paretoFront)) + '\n' )
    ouputRawFile.write( '_________________________________\n' ) 
    print "###########################################"
 
def CreateOuputFile(Algorithm,model,HV,PF,decisions,objectives):
    ##Print data for this Decision/objective pair
    print "----------------------------------------------------------------"
    fname = ('./data/'+model.__name__+'_'+str(decisions)+'Dec_and_'+str(objectives)+'Obj.txt')
    fo = open(fname, "wb")
    fo.write('Algorith : '+ Algorithm.__name__ + '\n')
    fo.write('Model    : '+ model.__name__ + '\n')
    fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
    fo.write('Decision,Objectives,Energy of all Pareto Values Per Iteration\n')                    
    fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
    fo.write('=====================================================================`\n')
    fo.write('Number of Decisions  = '+str(decisions) +'\n')
    fo.write('Number of Objectives = '+str(objectives) +'\n')
    fo.write('=====================================================================`\n')
    fo.write('HyperVolume Per Iteration\n')
    hvTable = PrettyTable()
    sNo = range(1,numOfIterations + 1)
    hvTable.add_column("Iteration  ",sNo)
    hvTable.add_column("HyperVolume",HV)
    #print hvTable
    fo.write( str(hvTable) + '\n' )
    fo.write('||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||\n')
    ##########
    
    xTable  = PrettyTable()
    fxTable = PrettyTable()
    eTable  = PrettyTable()

    count = 0
    for i in range(len(PF)):
        fo.write('---------------------------------------------------------------------------------------------------------\n')
        fo.write('ITERATION = '+str(i+1)+'\n')
        fo.write('---------------------------------------------------------------------------------------------------------\n')

        for j in  range(len(PF[i])):
            heading = 'Dec, x    [ITERATION='+str(i+1)+'] [PF:'+str(j+1)+']'
            xTable.add_column(heading,PF[i][j].x)
            heading = 'Obj, f(x) [ITERATION='+str(i+1)+'] [PF:'+str(j+1)+']'
            fxTable.add_column(heading,PF[i][j].getObjectives())
            heading = ' Energy   [ITERATION='+str(i+1)+'] [PF:'+str(j+1)+']'
            val = [repr(PF[i][j].eval())]
            eTable.add_column(heading,val)
            count+=1
            if count == 3:
                count = 0
                #print xTable
                #print fxTable
                #print eTable
                fo.write('DECISIONS\n')
                fo.write( str(xTable) + '\n' )
                fo.write('OBJECTIVES\n')
                fo.write( str(fxTable) + '\n' )
                fo.write('ENERGY\n')
                fo.write( str(eTable) + '\n' )
                fo.write('\n#########################################################################################################\n')

                xTable  = PrettyTable()
                fxTable = PrettyTable()
                eTable  = PrettyTable()
        if count >0:            
            #print xTable
            #print fxTable
            #print eTable
            fo.write( str(xTable) + '\n' )
            fo.write( str(fxTable) + '\n' )
            fo.write( str(eTable) + '\n' )

    fo.close()  # Close opend file
    ##############################


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
    print rdivlength
    rdivInput = [[] for i in range(rdivlength)]
    rdivIndex = 0
    
    TotalRounds = len(numOfDecisions) * len(numOfObjectives) * numOfIterations
    fname = "./data/CODE9_output_dump.log"
    ouputRawFile = open(fname, "wb") 
    
    #for model in [DTLZ7,DTLZ1]:
    for model in [DTLZ1,DTLZ3,DTLZ5,DTLZ7]:
        
        ouputRawFile.write( '|||||||||||||||||||||||||||||||||||||||||||||\n' )
        mod = ( "Model    : %s " %model.__name__)
        ouputRawFile.write(mod+'\n')
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
                print "\nStarting processing for number of objectives  =", objectives

                for decisions in numOfDecisions:
                    print "\nStarting processing with number of decisions = " ,decisions
                    
                    time = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                    ouputRawFile.write( '*********************************\n' ) 
                    ouputRawFile.write( 'Start Time = ' +  time + '\n' ) 
                    ouputRawFile.write( 'Number of objectives : ' + repr(objectives) + '\n' ) 
                    ouputRawFile.write( 'Number of decisions  : ' + repr(decisions) + '\n' ) 
                    ouputRawFile.write( '*********************************\n' ) 

                    i = 1
                    HV =[]
                    nPF=[]
                    PF =[]
                    
                    for k in xrange(numOfIterations):
                        ouputRawFile.write( '================================\n' ) 
                        stime = strftime("%Y-%m-%d %H:%M:%S", gmtime())
                        ouputRawFile.write( 'ITERATION NUMBER = ' + repr(i) + '\n' )

                        DifferentSeeds=random.randint(0,10000)
                         
                        paretoFront,HyperVolume=Algorithm(model,decisions=decisions,objectives=objectives,someSeed=DifferentSeeds)
                        Dumpfile(paretoFront,stime)
                        ouputRawFile.write( '================================\n' ) 
       
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

                    CreateOuputFile(Algorithm,model,HV,PF,decisions,objectives)
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
    ouputRawFile.close()  # Close opend file  
    