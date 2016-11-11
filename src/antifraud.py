#!/bin/python
import sys

'''
	Author: Chandra S. Nepali 
	Date: November 10, 2016
	Summary: example of program that detects suspicious transactions fraud detection algorithm
			 Each id (id1 and id2) in the input data is represented by the a class "Node". Each Node has a list of its first degree friends.
			 Nodes are stored in a dictionary to map its "id" with the list of its first degree friends.
'''

# class to hold one node/vertex and a list of its first degree friends
class Node:
	def __init__(self, idd):
		self.friends = []		
		self.friends.append(idd)

	def addFriend(self, idd):
		self.friends.append(idd)

	def getFriends(self):
		return self.friends
#-----------------------------------------------------------


# search whether id1 has transection with id2 before or not
def find(Nodes, id1, id2, lv):
#	if not id1 in Nodes: return 0		# id1 is not in the list, unknown id1

	# first look-up in first degree friends
	if lv == 1:
		if id2 in Nodes[id1].getFriends(): 
			return 'trusted'
		return 'unverified'

	# look-up in second degree friends
	if lv == 2:
		for fr1 in Nodes[id1].getFriends():
			if id2 in Nodes[fr1].getFriends():
				return 'trusted'
		return 'unverified'

	# look-up in fourth degree friends
	if lv == 3:
		for fr1 in Nodes[id1].getFriends():
			for fr2 in Nodes[fr1].getFriends():
				for fr3 in Nodes[fr2].getFriends():
					if id2 in Nodes[fr3].getFriends():
						return 'trusted'
		return 'unverified'
#-----------------------------------------------------------

# read the input data and write in a graph
def init(Nodes, fl):
	print 'initializing the graph, please wait ........'
	fl.readline()

	for line in fl:
		line = line.strip()
		lines = line.split(',')
		id1 = lines[1].strip()
		id2 = lines[2].strip()

		if id1 in Nodes: 
			if not id2 in Nodes[id1].getFriends(): 
				Nodes[id1].addFriend(id2)
		else:
			Nodes[id1] = Node(id2)
			Nodes[id1].addFriend(id1)		

		if id2 in Nodes:
			if not id1 in Nodes[id2].getFriends():
				Nodes[id2].addFriend(id1)
		else:
			Nodes[id2] = Node(id1)
			Nodes[id2].addFriend(id2)

	print 'done'
#------------------------------------------------------------



#--------  main function  --------

Nodes = {}					# dictionary to hold nodes and list of their first degree friends

arg = sys.argv

# read input data and initialize the graph
flBatch = open(arg[1], 'r')
init(Nodes, flBatch)		
flBatch.close()
#-----------------------------------------

flStream = open(arg[2], 'r')
flOut1 = open(arg[3], 'w')
flOut2 = open(arg[4], 'w')
flOut3 = open(arg[5], 'w')

# Read the stream data and output
flStream.readline()

for line in flStream:
	line = line.strip()
	lines = line.split(',')
	id1 = lines[1].strip()
	id2 = lines[2].strip()

	# Feature 1
	mess = find(Nodes, id1, id2, 1)
	flOut1.write(mess)

	# Feature 2
	mess = find(Nodes, id1, id2, 2)
	flOut2.write(mess)

	# Feature 3
	mess = find(Nodes, id1, id2, 3)
	flOut3.write(mess)

	# update the graph: put their second/third/fourth degree friends in the list of first degree friends 
	# after the transection because this will improve the future search speed.
	if mess > 1:
		if not id2 in Nodes[id1].getFriends(): Nodes[id1].addFriend(id2)
		if not id1 in Nodes[id2].getFriends(): Nodes[id2].addFriend(id1)

flStream.close()
flOut1.close()
flOut2.close()
flOut3.close()
