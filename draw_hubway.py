import networkx as nx
import datetime
from readGraph_hubway import Loader
import matplotlib.pyplot as plt

l = Loader()
#this is a file list that the graph built from, now the list only contians 1 file
fileList = ['hubway_trips.csv', 'hubway_stations.csv'];
starttime = datetime.datetime(2013,7,28,0,0,0);
endtime = datetime.datetime(2013,8,28,0,0,0);
#you are loading di-graph with multiple edges, without weight, which is easy to comput degree
G, pos = l.load_DiGraph(starttime, endtime, fileList)
#you also can load as di-graph with weight.
#G = l.load_DiGraph(starttime, endtime, fileList)
nx.draw(G, pos, node_size = 50,width=0.05)
plt.savefig("out.pdf")
plt.show()