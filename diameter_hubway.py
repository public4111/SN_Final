#This script shows the densifacation law. 
#We could also analyse the effect of the seasonal fluctuation.

import networkx as nx
import datetime
from readGraph_hubway import Loader
from collections import defaultdict
l = Loader()
fileList = ['hubway_trips.csv'];
gap = datetime.timedelta(days=30)
duration = datetime.timedelta(days=30)
starttime = datetime.datetime(2011,7,28,0,0,0)
lasttime = datetime.datetime(2013,10,31,23,59,59)
endtime = starttime + duration

while starttime<lasttime:
#you are loading di-graph with multiple edges, without weight, which is easy to comput degree
	G = l.load_MultiDiGraph(starttime, endtime, fileList)
#you also can load as di-graph with weight.
#G = l.load_DiGraph(starttime, endtime, fileList)
	#print G.number_of_nodes() ,  G.number_of_edges(), "Histo:"

	p = nx.shortest_path_length(G)
	hist = [0,0,0,0,0,0,0,0,0,0]
	sz = len(p)
    
	if (sz==0):
		starttime = endtime + gap
		endtime = starttime + duration
		continue

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

	theta = 0.90
	dia = 0
	for path in range(9):
		hist[path+1] = hist[path+1]+hist[path]
		if(hist[path+1]>theta):
			dia = path + 1.0*(theta-hist[path])/(hist[path+1]-hist[path])
			break

	print G.number_of_nodes(), dia

	starttime = endtime + gap
	endtime = starttime + duration
