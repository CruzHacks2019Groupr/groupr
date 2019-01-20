#import everything we need
import networkx as nx
import itertools
from .Event import Event 

def findPerfectGroup(Event, node, size):								   						#Update swipe occurs, giving a first and second ID
	List = nx.cliques_containing_node(Event.G, node)						
	for j in List:														  					 	#Checks the size of each clique, ignore if not of size n
		if len(j) is size:
			for i in j:													   						#removes nodes from the clique
				Event.remove_user(i)
			return j; 													   						#break when the first valid clique is found

def forceGroups(Event, size):								 									#Makes groups based on current criterium

	possibleGroups = list(itertools.combinations(list(Event.DG), size))    						#All combinations of the Node list in groups of length n are stored in list
	i = 0
	groupCombo = [list(list())]	
	scoreList = []										  										#Nested loops build a combination of groups (disjoint is used to make sure the same person doesnt end up in a group twice)
	while i < len(possibleGroups) and not set(possibleGroups[0]).isdisjoint(possibleGroups[i]):
		groupCombo.append([])
		groupCombo[i].append(possibleGroups[i])                         						#Add first group
		scoreList.append(computeScore(Event, possibleGroups[i]))           						#Add score of first group
		j = i + 1
		while j < len(possibleGroups):
			for k in groupCombo[i]:                                        						#Checks if any shared members in current running groupCombo
				if not set(k).isdisjoint(possibleGroups[j]):
					break												   						#Breaks if shared members
				groupCombo[i].append(possibleGroups[j])                    						#If there is no break then group is added to combo
				scoreList[i] += computeScore(Event, possibleGroups[j])            				#Score is added as well
			j+=1
		i+=1

	BestIndex = 0
	for k in range(len(scoreList)):													   			#Finds best group combo (highest score)
		if scoreList[k] > scoreList[BestIndex]:
			BestIndex = k

	for k in range(len(groupCombo[BestIndex])):                                        			#Removes groups from graph
		for l in range(len(groupCombo[BestIndex][k])):								   
			Event.remove_user(groupCombo[BestIndex][k][l])

	groupCombo[BestIndex].append(list(Event.DG))							   					#All remaining people are put into a group

	return groupCombo[BestIndex]

	
def computeScore(Event, L):													   					#For a given group computes the score, which is the number edges

	score = 0
	for i in L:
		for j in L:
			if i != j and i in Event.DG.neighbors(j):
				score+=1;
	return score