#import everything we need
import networkx as nx
import itertools

def newSwipe(ID_1, ID_2) 												   #Update swipe occurs, giving a first and second ID

	#DiG is digraph from database
	#G is undirected graph from database
	DiG.add_edge(ID_1, ID_2)
	if ID_1 in DiG.neighbors(ID_2)
		G.add_edge(ID_1, ID_2)
	List = cliques_containing_node(G, nodes=None)
	if not List
		return None;
	else
		for i in List[0]:
			G.remove_node(i)
			DiG.remove_node(i)
		#List[0] is added to the database

def forceGroups() #Makes groups based on current criterium

	possibleGroups = list(itertools.combinations(list(DiG), n))            #All combinations of the Node list in groups of length n are stored in list
	i = 0
	                                                                       #Nested loops build a combination of groups (disjoint is used to make sure the same person doesnt end up in a group twice)
	while not set(possibleGroups[0]).isdisjoint(possibleGroups[i]):
		groupCombo[i].append(possibleGroups[i])                            #Add first group
		scoreList[i] += computeScore(possibleGroups[i])                    #Add score of first group
		j = i + 1
		while j < len(possibleGroups):
			for k in groupCombo[i]:                                        #Checks if any shared members in current running groupCombo
				if not set(groupCombo[i][k]).isdisjoint(possibleGroups[j])
					break												   #Breaks if shared members
				groupCombo[i].append(possibleGroups[j])                    #If there is no break then group is added to combo
				scoreList[i] += computeScore(possibleGroups[j])            #Score is added as well
			j++
		i++

	temp = 0
	for k in scoreList:													   #Finds best group combo (highest score)
		if scoreList[k] > scoreList[temp]
			temp = k

	for k in groupCombo[temp]:                                             #Groups from combo are added
		#groupCombo[temp][k] is added to the database
	
def computeScore(L) 													   #For a given group computes the score, which is the number edges

	score = 0
	for i in L:
		for j in L:
			if L[i] in DiG.neighbors(L[j])
				score++
	return score