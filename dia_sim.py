import networkx as nx

flst = ['Graph_50.txt', 'Graph_100.txt', 'Graph_150.txt', 'Graph_200.txt', 'Graph_250.txt', 'Graph_300.txt', 'Graph_350.txt', 'Graph_400.txt', 'Graph_450.txt']
for f in flst:
	G = nx.read_adjlist(f)

	p = nx.shortest_path_length(G)
	hist = [0,0,0,0,0,0,0,0,0,0]
	sz = len(p)
    
	pairs = sz*(sz-1)
	for p1 in p:
		for p2 in p[p1]:
			if(p1==p2):
				continue
			leng = p[p1][p2]
			hist[leng] = hist[leng]+1

	for path in range(10):
		hist[path] = 1.0*hist[path]/pairs
		#if(hist[path] != 0):
			#print path, hist[path]

	theta = 0.9
	dia = 0
	for path in range(9):
		hist[path+1] = hist[path+1]+hist[path]
		if(hist[path+1]>theta):
			dia = path + 1.0*(theta-hist[path])/(hist[path+1]-hist[path])
			break

	print G.number_of_nodes(), dia