import networkx as nx
import datetime
from readGraph_hubway import Loader
import matplotlib.pyplot as plt

l = Loader()
#this is a file list that the graph built from, now the list only contians 1 file
fileList = ['hubway_trips.csv', 'hubway_stations.csv'];
starttime = datetime.datetime(2013,5,28,0,0,0);
endtime = datetime.datetime(2013,8,28,0,0,0);
#you are loading di-graph with multiple edges, without weight, which is easy to comput degree
G, pos = l.load_DiGraph(starttime, endtime, fileList)

for n in G.nodes():
	n_adj = 0
	this_loc = pos[n]
	min = 1000000000000
	min_no = -1
	for station_id in pos:
		if(station_id==n or not G.has_node(station_id)):
			continue
		loc = pos[station_id]
		dis = (loc[0]-this_loc[0])*(loc[0]-this_loc[0])+(loc[1]-this_loc[1])*(loc[1]-this_loc[1])
		if dis<min:
			min_no = station_id
			min = dis

	n_adj = min_no
	n_adj_adjlist = G.edges(n_adj,data=True)
	n_adjlist = G.edges(n,data=True)
	n_adj_wsum = 0
	for e in n_adj_adjlist:
		n_adj_wsum = n_adj_wsum + e[2]['w']

	n_wsum = 0
	for e in n_adjlist:
		for ee in n_adj_adjlist:
			if(e[1]==ee[1]):
				n_wsum = n_wsum + e[2]['w']
				break

	print n_wsum, n_adj_wsum, 1.0*n_wsum/n_adj_wsum


