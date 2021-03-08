import networkx as nx
import matplotlib.pyplot as plt
import community
import math
import matplotlib.cm as cm
from networkx.algorithms.community import centrality as c

def drawGraph(g, node_colors=["Red"], with_labels=True):
	pos = nx.spring_layout(g)
	plt.figure(figsize=(10,10))
	nx.draw_networkx(g, pos=pos, with_labels=with_labels, node_color=node_colors)
	plt.axis('off')
	plt.show()

'''
################################################
Step 1:
Create and display graph
################################################'''
fin=open("GameOfThrones.txt", 'rb')
G = nx.read_edgelist('GameOfThrones.txt', nodetype=str, delimiter=",", data=(("weight", int),("season", int)))
fin.close()

# drawGraph(G)


'''
################################################
Step 2 output:
a) No. of maximal cliques
b) Size of largest maximal clique
c) No. of maximal cliques of the largest size
##################################################'''
maxCliques = nx.find_cliques(G)
biggestClique = 0
numBiggestCliques = 0

ctr = 0
for clique in maxCliques:
	ctr += 1
	if(len(clique) > biggestClique):
		biggestClique = len(clique)	
	
print("Number of Maximal Cliques: " + str(ctr))
print("Size of Largest Maximal Clique: " + str(biggestClique))

#Could only loop through generator once, so just remake it
maxCliques = nx.find_cliques(G)
ctr=0
for clique in maxCliques:
	if(len(clique) == biggestClique):
		ctr += 1
print("Number of maximal cliques of largest size: " + str(ctr))



'''
################################################
Step 3 output:
a) No. of nodes in the main core
b) K-value that gives the main core
c) Display main core with nodes labeled
##################################################'''
mainCore = nx.k_core(G).nodes()
mainCoreEdges = nx.k_core(G).edges()
nodeCoreDict = nx.core.core_number(G)

print("\nNumber of nodes in main core: " + str(len(mainCore)))

maxKValue = 0
for node in nodeCoreDict:
	if(nodeCoreDict[node] > maxKValue):
		maxKValue = nodeCoreDict[node]
		
print("K value that gives the main core: " + str(maxKValue))

#Create subgraph that contains just the main core
coreGraph = nx.Graph()
for edge in mainCoreEdges:
	coreGraph.add_edge(edge[0], edge[1])
# drawGraph(coreGraph)



'''
################################################
Step 4 output:
a) Number of nodes in the main crust
##################################################'''
print("\nNumber of nodes in the main crust: " + str(len(nx.k_crust(G).nodes())))


'''
################################################
Step 5 output:
a) Number of nodes in the k-corona where k is the max k-val (main core kval)
##################################################'''
print("\nNumber of nodes in the k-corona: " + str(len(nx.k_corona(G, k=maxKValue).nodes())))



'''
################################################
Step 6 output:
a) Number of nodes in the main shell
##################################################'''
mainShell = nx.k_shell(G).nodes()
mainShellEdges = nx.k_shell(G).edges()
print("\nNumber of nodes in main shell: " + str(len(mainShell)))

#Create subgraph that contains just the main shell
mainShellGraph = nx.Graph()
for edge in mainShellEdges:
	mainShellGraph.add_edge(edge[0], edge[1])
# drawGraph(mainShellGraph)


'''
################################################
Step 7 output:
a) Display graph with red main core and blue main crust, no labels
##################################################'''
crustNodes = nx.k_crust(G).nodes()
coreNodes = mainCore
node_colors = list()

#Create color list for displaying the graph
for node in G.nodes():
	if node in coreNodes:
		node_colors.append("Red")
	else:
		node_colors.append("Blue")

# drawGraph(G, node_colors, False)



'''
######################################################################################################################################
Step 8 output: Louvain Method
a) Output the number of communities, the size of largest community, size of smallest community, and modularity of this partitioning
######################################################################################################################################'''
partition = community.best_partition(G)
modularity = community.modularity(partition, G)


numPartitions = 0
populationList = dict()

#Loop through the Louvain partition
for node in partition:
	if(partition[node] > numPartitions):		#Get the number of partitions
		numPartitions = partition[node]

	if(partition[node] not in populationList):	#Count the number of people in each partition
		populationList[partition[node]] = 1
	else:
		populationList[partition[node]] += 1


#Loop through the population list of each community
maxPop = 0
minPop = len(list(G.nodes()))+1
for key in populationList:
	if(populationList[key] > maxPop):
		maxPop = populationList[key]
	if(populationList[key] < minPop):
		minPop = populationList[key]


print("\nThere are " + str(numPartitions) + " communities using the Louvain method.")
print("The smallest community has " + str(minPop) + " people.")
print("The largest community has " + str(maxPop) + " people.")
print("The modularity of the Louvain partitioning is " + str(modularity))


'''
#######################################################################
Step 9 output:
a) Display the Louvain graph color coded 
#######################################################################'''
color_list = list()
for node in G.nodes():
	if(partition[node] == 0):
		color_list.append("Red")
	elif(partition[node] == 1):
		color_list.append("Blue")
	elif(partition[node] == 2):
		color_list.append("Orange")
	elif(partition[node] == 3):
		color_list.append("Blue")
	elif(partition[node] == 4):
		color_list.append("Purple")
	elif(partition[node] == 5):
		color_list.append("Green")
	elif(partition[node] == 6):
		color_list.append("Brown")

# drawGraph(G, color_list, False)


'''
#######################################################################
Step 11 output: Girvan-Newman
a) Output the number of communities, the size of largest community, size of smallest community, and modularity of this partitioning
#######################################################################'''
components = c.girvan_newman(G)
i=0
for row in components:
	if(i==0):
		finalResult = row
	# print(row)
	i += 1

minCommunity = len(list(G.nodes))+1
maxCommunity = 0
ctr = 0
partitions = dict()
L = list(finalResult)
p=0
for comp in L:
	for entry in comp:
		partitions[entry] = p
		ctr += 1
	if(ctr < minCommunity):
		minCommunity = ctr
	if(ctr > maxCommunity):
		maxCommunity = ctr
	p += 1
	ctr = 0

print(partitions)

print("\nThere are " + str(p) + " communitites using the Girvan-Newman method.")
print("The smallest community has " + str(minCommunity) + " people.")
print("The largset community has " + str(maxCommunity) + " people.")
print("The modularity of the Girvan-Newman partitioning is " + str(community.modularity(partitions, G)))


'''
#######################################################################
Step 12 output:
a) The Girvan-Newman graph color coded
#######################################################################'''



'''
node_color = list()

pos = nx.spring_layout(g)
plt.figure(figsize=(10,10))
nx.draw_networkx(g, pos=pos, with_labels=True, node_color=node_color)
plt.axis('off')
plt.show()
'''


'''
#(1) Output Degree Stats
def DegreeOutput(g):
	#Init
	for node in g:	 
		minDegree = g.degree[node]
		maxDegree = g.degree[node]
		degreeSum = 0
		break
	
	
	for node in g:
		if(g.degree[node] < minDegree):
			minDegree = g.degree[node]
		if(g.degree[node] > maxDegree):
			maxDegree = g.degree[node]
			
		degreeSum += g.degree[node]
	
	print("=============== #1 ===============")
	print("Max Degree: ", maxDegree)
	print("Min Degree: ", minDegree)
	print("Average Degree: ", degreeSum/len(g.nodes))
	
	
	
def CharacteristicPathLength(g):
	print("\n=============== #2 ===============")
	print("Average Shortest Path Length: ", nx.average_shortest_path_length(g))
	
def Diameter(g):
	print("\n=============== #3 ===============")
	print("Diameter: ", nx.diameter(g))
	
def CenterAndPeripheral(g):
	print("\n=============== #4 ===============")
	print("Center Nodes: ", nx.center(g))
	print("Peripheral Nodes: ", nx.periphery(g))

	
#I think you can calculate it if you take the entries in the apsp matrix (minus the ones along the diagonal), sort them, and take the average of the top 90%. Try that on the example we did in class.
def EffectiveEccentricity(g):
	print("\n=============== #5 ===============")
	totalDolphins = len(list(g.nodes))
	dolphinsToKeep = math.floor(totalDolphins * 0.9)

	#Calculate every shortest path for every dolphin
	spaths = dict(nx.all_pairs_shortest_path_length(g))

	paths = list()
	ctr = 0
	
	for node1 in spaths:
		for node2 in spaths[node1]:
			if(node1 != node2):
				paths.append(spaths[node1][node2])

	#Sort in descending order
	paths.sort(reverse=True)

	for i in range(len(paths)):
		if(paths[i] == 1):
			ctr = ctr+1

	#Keep top 90% highest values
	paths = paths[:math.floor(len(paths)*.9)]

	#Average of this list (consisting of top 90% of shortest path values)
	print("Effective Eccenctricity: ", sum(paths)/len(paths))
	
	
def Density(g):
	print("\n=============== #6 ===============")
	print("Density: ", nx.density(g))
	

def ClusterCoeff(g):
	#A graph is small-worldif C is significantly higher than it would be for a random graph constructed on the same vertex set with approximately the same diameter
	c = nx.clustering(g)
	
	# compute overall coefficient
	sum = 0
	for x in c:
		sum = sum + c[x]
		
	print("\n=============== #7 ===============")
	print("Cluster Coefficient: ", sum/g.number_of_nodes())
	
	
def Transitivity(g):
	print("\n=============== #8 ===============")
	print("Transitivity: ", nx.transitivity(g))
	
	
def BetweennessCentrality(g):
	BC = nx.betweenness_centrality(g, normalized=True)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 10000 for v in BC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()
	
def EigenvectorCentrality(g):
	EC = nx.eigenvector_centrality(g)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 6000 for v in EC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()


def ClosenessCentrality(g):
	CC = nx.closeness_centrality(g)
	node_color = [5000 * g.degree(v) for v in g]
	node_size = [v * 3500 for v in CC.values()]
	
	plt.figure(figsize=(20,20))
	nx.draw_networkx(g, with_labels=True, node_color=node_color, node_size=node_size, font_size=9, font_color="black")
	plt.axis('off')
	plt.show()

							
#1-8 drivers
DegreeOutput(DolphinGraph)
CharacteristicPathLength(DolphinGraph)
Diameter(DolphinGraph)
CenterAndPeripheral(DolphinGraph)
EffectiveEccentricity(DolphinGraph)
Density(DolphinGraph)
ClusterCoeff(DolphinGraph)
Transitivity(DolphinGraph)

#9 Drivers
BetweennessCentrality(DolphinGraph)
EigenvectorCentrality(DolphinGraph)
ClosenessCentrality(DolphinGraph)
'''