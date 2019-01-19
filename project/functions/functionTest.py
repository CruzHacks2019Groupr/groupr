from Event import Event

def event_test():
	numNodes = int(input("num nodes?"))
	numEdges = int(input("num edges?"))

	nodes = []
	edges = []

	for x in range(numNodes):
		nodes.append(int(input("node#" + str(x) + "?")))

	for x in range(numEdges):
		a = int(input("edge#" + str(x) + "? (a)"))
		b = int(input("edge#" + str(x) + "? (b)"))

		edges.append((a,b));

	print(nodes)
	print(edges)

	testEvent = Event()

	for x in nodes:
		testEvent.add_user(x)

	for x in edges:
		testEvent.add_edge(x[0],x[1])

	print(testEvent.export_users())
	print(testEvent.export_edges_directed())
	print(testEvent.export_edges_undirected())

	testEvent.visualize();

if __name__ == "__main__":
    event_test()