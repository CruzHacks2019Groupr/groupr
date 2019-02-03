import networkx as nx
import itertools
from .dbHandler import UserHandler
from .dbHandler import EventHandler

def findPerfectGroup(Event, User):
	PerfectGroups = nx.cliques_containing_node(Event.G(), User)
	for i in PerfectGroups:
		if len(i) is Event.groupSize:
			for j in i:
				Event._removeUserFromGraph(j)
			return createGroup(i, Event)

def forceGroups(Event):
	possibleGroups = list(itertools.combinations(list(Event.DG()), Event.groupSize))    		#All combinations of the Node list in groups of length n are stored in list
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
			Event._removeUserFromGraph(groupCombo[BestIndex][k][l])

	groupCombo[BestIndex].append(list(Event.DG()))							   					#All remaining people are put into a group

	groupList = []
	for k in groupCombo[BestIndex]:
		groupList.append(createGroup(k, Event))

	return groupList

def computeScore(Event, L):													   				#For a given group computes the score, which is the number edges
	score = 0
	for i in L:
		for j in L:
			if i != j and i in Event.DG().neighbors(j):
				score+=1;
	return score