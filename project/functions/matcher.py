#import everything we need
import networkx as nx
import itertools
from Event import Event 

<<<<<<< HEAD
def findPerfectGroup(Event,node, size):									#Update swipe occurs, giving a first and second ID
	List = nx.cliques_containing_node(Event.G, node)						
	for j in List:															#Checks the size of each clique, ignore if not of size n
		if len(j) is size:
			for i in j:														#removes nodes from the clique
				Event.remove_user(i)
			return j; 															#break when the first valid clique is found

def forceGroups(): #Makes groups based on current criterium

	possibleGroups = list(itertools.combinations(list(DiG), n))            #All combinations of the Node list in groups of length n are stored in list
	i = 0
																		   #Nested loops build a combination of groups (disjoint is used to make sure the same person doesnt end up in a group twice)
=======
def findPerfectGroup(Graph,ID_1,ID_2) 									   #Update swipe occurs, giving a first and second ID
	List = cliques_containing_node(Graph.G, nodes=[ID_1,ID_2])						
	for j in List:														   #Checks the size of each clique, ignore if not of size n
		if len(j) is n
			for i in j:													   #removes nodes from the clique
				Graph.remove_user(i)
			return j													   #break when the first valid clique is found

def forceGroups(DiGraph) #Makes groups based on current criterium

	possibleGroups = list(itertools.combinations(list(DiGraph), n))        #All combinations of the Node list in groups of length n are stored in list
	i = 0                                                                  #Nested loops build a combination of groups (disjoint is used to make sure the same person doesnt end up in a group twice)
>>>>>>> 147a7b083f7c727d69692eac6f7816e6efa173eb
	while not set(possibleGroups[0]).isdisjoint(possibleGroups[i]):
		groupCombo[i].append(possibleGroups[i])                            #Add first group
		scoreList[i] += computeScore(possibleGroups[i])                    #Add score of first group
		j = i + 1
		while j < len(possibleGroups):
			for k in groupCombo[i]:                                        #Checks if any shared members in current running groupCombo
				if not set(groupCombo[i][k]).isdisjoint(possibleGroups[j]):
					break												   #Breaks if shared members
				groupCombo[i].append(possibleGroups[j])                    #If there is no break then group is added to combo
				scoreList[i] += computeScore(possibleGroups[j])            #Score is added as well
			j+=1
		i+=1

	temp = 0
	for k in scoreList:													   #Finds best group combo (highest score)
		if scoreList[k] > scoreList[temp]:
			temp = k

<<<<<<< HEAD
	#for k in groupCombo[temp]:                                             #Groups from combo are added
		#groupCombo[temp][k] is added to the database
=======
	for k in groupCombo[temp]:                                             #Removes groups from graph
		for l in groupCombo[temp][k]:
			Digraph.remove_user(groupCombo[temp][k][l])

	groupCombo[temp].append(list(Digraph))

	return groupCombo[temp]

>>>>>>> 147a7b083f7c727d69692eac6f7816e6efa173eb
	
def computeScore(L):													   #For a given group computes the score, which is the number edges

	score = 0
	for i in L:
		for j in L:
			if L[i] in DiG.neighbors(L[j]):
				score+=1;
	return score