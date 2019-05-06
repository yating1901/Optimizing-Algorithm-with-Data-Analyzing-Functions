#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import xml.etree.ElementTree as ET
import numpy as np
import random
from IPython import get_ipython
import os
from random import shuffle
import sys
import textwrap as tw
from StigSim import StigSim
import matplotlib.pyplot as plt
import json 

def MatchPinXML(pop): 
    DNA=pop['DNA']
    parameters=[]
    length=[]
    fitness=[]
    for chrosome in range(len(DNA)):
        parameters=DNA[chrosome,:]
        ex_config_file_path="configuration.xml"
        tree = ET.parse(ex_config_file_path)
        root = tree.getroot() 
        subnode=tree.findall("objects/object/rules/rule/actions")
        index=0
        for node in subnode:
            node.set('p',str(parameters[index]))
            index=index+1
#            print(node.get('p'))                              
        et = ET.ElementTree(root)  
        et.write("configuration.xml", encoding="utf-8", xml_declaration=True, short_empty_elements=False)
        simulator= StigSim("configuration.xml")
        world=simulator.world_record[99]
        simulator.run("testresults")
        length=MeasureWorld(world)
#        print(length)
        fitness.append(length)
    return fitness


def MeasureWorld(world):
    
    length=[]
    condition1=(world-2)==0
    condition2=(world-3)==0
    count1=world[condition1]
    count2=world[condition2]
    length=len(count1)+len(count2)
#    print(length)
    return length

class ES:
    
    def __init__(self, ga_config_file_path):
        self.parameterdict={}  
        self.ga_config_file_path=ga_config_file_path     
        tree = ET.parse(ga_config_file_path)
        root = tree.getroot() #this is the xml node
        for sub_node in root:
            node_type = sub_node.tag
#            print(node_type)
            if (node_type == "parameters"):
                for sub_sub_node in sub_node:   
                    self.parameterdict[sub_sub_node.get('parameter')]=sub_sub_node.get('value')
        
    def ImportData(self):
            
        self.DNA_SIZE=int(self.parameterdict["DNA_SIZE"])
        self.POP_SIZE=int(self.parameterdict["POP_SIZE"])
        self.CROSS_RATE=float(self.parameterdict["CROSS_RATE"]) 
        self.MUTATION_RATE=float(self.parameterdict["MUTATION_RATE"])
        self.N_GENERATIONS=int(self.parameterdict["N_GENERATIONS"])
        self.N_KID=int(self.parameterdict["N_KID"])
        self.pop= dict(DNA=np.random.rand(self.POP_SIZE,self.DNA_SIZE),  # initialize the pop DNA values 
                       mut_strength=np.random.rand(self.POP_SIZE,self.DNA_SIZE)) 
        
    def crossover(self):
        crossindex=np.empty((self.DNA_SIZE,)).astype(np.bool)
        self.kids = {'DNA': np.empty((self.N_KID,self.DNA_SIZE))}
        self.kids['mut_strength'] = np.empty_like(self.kids['DNA'])
        for kidsvalue, kidsstrength in zip(self.kids['DNA'], self.kids['mut_strength']):
            p1, p2 = np.random.choice(np.arange(self.POP_SIZE), size=2, replace=False) # crossover (roughly half p1 and half p2)
            for i in range(self.DNA_SIZE):
                crossindex[i]= True if np.random.rand() < self.CROSS_RATE else False  
            kidsvalue[crossindex] = self.pop['DNA'][p1, crossindex]
            kidsvalue[~crossindex] = self.pop['DNA'][p2, ~crossindex]
            kidsstrength[crossindex] = self.pop['mut_strength'][p1, crossindex]
            kidsstrength[~crossindex] = self.pop['mut_strength'][p2, ~crossindex]  
        
    def mutation(self):
        # mutate (change DNA based on normal distribution)
        for kidsvalue, kidsstrength in zip(self.kids['DNA'], self.kids['mut_strength']):
            kidsstrength[:] = np.maximum(kidsstrength + (np.random.rand(*kidsstrength.shape)-0.5), 0.)    # must > 0
            kidsvalue += kidsstrength * np.random.randn(*kidsvalue.shape)
            kidsvalue[:] = np.clip(kidsvalue,0,1)    # clip the mutated value
       
    def get_fitness(self):
        
        
        fitness=MatchPinXML(self.pop)
#        self.fitness_record.append(fitness)

        return fitness
       
        
    def selection(self):
    # put pop and kids together
        for key in ['DNA', 'mut_strength']:
            self.pop[key] = np.vstack((self.pop[key], self.kids[key]))
        fitness =np.array(self.get_fitness())            # calculate global fitness 
#        print(fitness)
        idx = np.arange(self.pop['DNA'].shape[0])
        good_idx = idx[fitness.argsort()][-self.POP_SIZE:]   # selected by fitness ranking (not value)
#        print(fitness[good_idx])
        self.fitness_record.append(fitness[good_idx])
        
        for key in ['DNA', 'mut_strength']:
            self.pop[key] = self.pop[key][good_idx]


    def plttrend(self,result):
        MeanValueDeposit=[]
        MeanValuePick=[]
        ValueDeposit=[]
        ValuePick=[]
        for _g in range(self.N_GENERATIONS):
             ValueDeposit.append(result[str(_g)][:,0:39])
             ValuePick.append(result[str(_g)][:,40:43])
             MeanValueDeposit.append(np.mean(ValueDeposit))
             MeanValuePick.append(np.mean(ValuePick))
        gen=np.linspace(1,self.N_GENERATIONS,self.N_GENERATIONS)     
        plt.figure()
        plt.ylim(0,1)
        plt.plot(gen,MeanValueDeposit,c='red', alpha=0.5,label='MeanValueDeposit')
        plt.plot(gen,MeanValuePick,c='skyblue', alpha=0.5,label='MeanValuePick')
        plt.legend()
        plt.xlabel("Generations")
        plt.ylabel("Mean value of deposit/pick parameters")
        plt.show()
    
    def pltfitness(self):
        Meanfitness=[]
        Meanfitness=np.mean(self.fitness_record,axis=1)
        gen=np.linspace(1,self.N_GENERATIONS,self.N_GENERATIONS)     
        plt.figure()
        plt.ylim(0,100)
        plt.plot(gen,Meanfitness,c='red', alpha=0.5,label='Meanfitness')
        plt.legend()
        plt.xlabel("Generations")
        plt.ylabel("Mean value of fitness")
        plt.show()
        
        
    def evolve(self): 
        self.ImportData()
        self.fitness_record=[]
        result={}
        
        for _i in range(self.N_GENERATIONS):
            self.crossover()
            self.mutation()
            self.selection()
            result[str(_i)]=self.pop['DNA']
        global fit
        fit=self.fitness_record
        self.pltfitness()        
        return result
    
    
       
fit=[]
ga_config_file_path="GaConfiguration.xml"
ga=ES(ga_config_file_path)
result = ga.evolve()         


#import os
#import json 
results2={}
for i in range(0,100):
    results2[str(i)]=[str(j) for j in result[str(i)]]
os.makedirs("results2")    
json_report = json.dumps(results2, indent=4)
print("saving : ",os.path.join("results2","results.json"))
f = open(os.path.join("results2","results.json"),"w")
f.write(json_report)
f.close()






                
                


#import xml.etree.ElementTree as ET
#import numpy as np
#import random
#from IPython import get_ipython
#import os
#from random import shuffle
#import sys
#import textwrap as tw
#from StigSim import StigSim
#import matplotlib.pyplot as plt
#
# 
#tree = ET.parse("configuration.xml")
#root = tree.getroot() 



#def MeasureWorld(world):
#    
#    length=[]
#    condition1=(world-2)==0
#    condition2=(world-3)==0
#    count1=world[condition1]
#    count2=world[condition2]
#    length=len(count1)+len(count2)
##    print(length)
#    return length
#
#simulator= StigSim("configuration.xml")
#world=simulator.world_record[99]
#simulator.run("testresults")
#length=MeasureWorld(world)
#print(length)