# Optimizing-Algorithom-and-Data-Analyze-Functions

# you have to clone the repository with the submodules, whcih simulates the block building by robots and pass an array of the world to Optimizing algorithm to measure the fitness.

# the codes are written based on the python 3.7.

#All the script should be put in the same folder, inciuding the reports generated and saved by the codes.


# First, write the configuration of optimizing algorithm in the Gaconfiguration.xml.
# Then, start to run population.py to evolve different groups of parameters, each of which ranges from 0 to 1 and represents the probability of rules in simulation.
# The results of the population.py would be stored as result.json in the folder results2.
# Aferwords, one can use parameterAnalyze.py to import the results, draw the fitness curves, pick up specific DNA, record the rules excuted by two robots and show it as networks.


#remind: to record the rules chosen by the robots during one simulation, one should add codes in the configuration.xml to save the report as jason file:
<save format="report" period="1"></save> 
<save format="npz" period="1"></save>		

