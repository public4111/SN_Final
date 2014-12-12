import networkx as nx
import csv, re
import datetime
class Loader:

	def load_DiGraph(self, starttime, endtime, fileList):
		G = nx.DiGraph();
		count = 0;
		for file in fileList:
			csvfile = open(file, 'rb')
			reader = csv.DictReader(csvfile)
			for row in reader:
				stime = row['start_date']
				stime = self.timeParse(stime)
				if(starttime<=stime and endtime>=stime):
					count+=1
					#if(count % 1000 == 0):
						#print count
					if (G.has_edge(row['strt_statn'], row['end_statn'])):
						w = G[row['strt_statn']][row['end_statn']]['w']
						w += 1
					else:
						w = 1
					G.add_edge(row['strt_statn'], row['end_statn'], w = w)
				elif (stime>endtime):
					break
		return G

	def load_MultiDiGraph(self, starttime, endtime, fileList):
		G = nx.MultiDiGraph();
		count = 0;
		for file in fileList:
			csvfile = open(file, 'rb')
			reader = csv.DictReader(csvfile)
			for row in reader:
				stime = row['start_date']
				stime = self.timeParse(stime)
				if(starttime<=stime and endtime>=stime):
					count+=1
					#if(count % 1000 == 0):
						#print count
					G.add_edge(row['strt_statn'], row['end_statn'])
				elif (stime>endtime):
					break
		return G


	def timeParse(self, timeString):
		splt = re.split('/| |:', timeString)
		d = datetime.datetime(int(splt[2]),int(splt[0]),int(splt[1]), int(splt[3]), int(splt[4]), int(splt[5]))
		return d

