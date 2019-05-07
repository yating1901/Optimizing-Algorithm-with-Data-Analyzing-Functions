# Project Title
Optimizing-Algorithm-with-Data-Analyzing-Functions

## Version Control
The codes are written based on the python 3.7.

## Getting Started
You have to clone the repository with the submodules.
All the script should be put in the same folder, inciuding the reports generated and saved by the codes.

## Excuting Order
* First, write the configuration of optimizing algorithm in the Gaconfiguration.xml, and pass the file to start the algorithm.
```
ga_config_file_path="GaConfiguration.xml"
ga=ES(ga_config_file_path)
```

* Then, start to run population.py to evolve different groups of parameters, each of which ranges from 0 to 1 and represents the probability of rules in the simulation.

* The results of the population.py would be stored as result.json in the folder results2.
```
os.makedirs("results2")    
json_report = json.dumps(results2, indent=4)
print("saving : ",os.path.join("results2","results.json"))
f = open(os.path.join("results2","results.json"),"w")
f.write(json_report)
f.close()
```
* Aferwords, one can use parameterAnalyze.py to import the results, draw the fitness curves, pick up specific DNA, record the rules excuted by two robots and show it as networks.

## Remind
To record the rules chosen by the robots during one simulation, one should add codes in the configuration.xml to save the report as jason file:
```
<save format="report" period="1"></save> 
<save format="npz" period="1"></save>		
```
