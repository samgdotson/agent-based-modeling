# schelling model adapted from 
# 'https://www.binpress.com/simulating-segregation-with-python/'

# import necessary libraries

import matplotlib.pyplot as plt
import numpy as np
import itertools
import random 
import copy 
from list_funcs import intersection

class Schelling(object):
	"""This is the class that describes a Schelling Segregation
	Model."""
	def __init__(self, width, height, ratio_empty, tolerance, num_iter, num_races = 2):
		super(Schelling, self).__init__()
		self.width = width
		self.height = height
		self.ratio_empty = ratio_empty
		self.tolerance = tolerance
		self.num_iter = num_iter
		self.num_races = num_races
		self.empty_houses = []
		self.agents = {}
		self.changes_per_iter = []
	
	def populate(self):
		"""
		This method initializes the population at the start of 
		the simulation. Agents are randomly distributed on the 
		grid.
		"""
		
		# initialize the grid
		self.all_houses = list(itertools.product(range(self.width), range(self.height)))

		# mix it up
		random.shuffle(self.all_houses)


		# how many are empty?
		self.n_empty = int(self.ratio_empty * len(self.all_houses))
		# create list of empty house locations
		self.empty_houses = self.all_houses[:self.n_empty]

		# create list of inhabited house locations
		self.inhabited = self.all_houses[self.n_empty:]

		# where do members of each race live?
		houses_by_race = [self.inhabited[i::self.num_races] for i in range(self.num_races)]

		# create "agents" for each race
		for i in range(self.num_races):
			# keys are locations
			# values are race
			self.agents = dict(list(self.agents.items()) + list(dict(zip(houses_by_race[i], 
				[i+1]*len(houses_by_race[i]))).items()))



	def is_unsatisfied(self, x, y):
		"""
		The method checks if an agent is satisfied based on 
		the @tolerance parameter. The (x,y) coordinates are
		the keys of the agents dictionary.

		Parameters:
		-----------
		x : integer
			The x-coordinate of a particular agent
		y : integer
			The y-coordinate of a particular agent
		"""

		# select the agent at the location (x,y)
		# print("checking if unhappy")
		race = self.agents[(x,y)]

		# initialize the counts 
		num_similar = 0
		num_different = 0

		# get the neighbors of the agent
		neighbors = list(itertools.product(range(x-1,x+2), range(y-1,y+2)))
		neighbors.remove((x,y)) # remove the current agent
		neighbors = intersection(neighbors, self.agents) # get inhabited neighors list

		# update race counts
		for neighbor in neighbors: 
			neighbor_race = self.agents[neighbor]
			if neighbor_race == race:
				num_similar += 1
			else:
				num_different += 1

		if (num_different + num_similar) == 0:
			# we cannot be unhappy if we have no neighbors
			return False

		else: 
			# we can be either happy or unhappy if we have neighbors
			return (num_similar/(num_similar+num_different)) < self.tolerance



	def update(self):
		"""
		This method executes each iteration for num_iter
		"""

		for i in range(self.num_iter):
			# create a copy of the old agents
			self.old_agents = copy.deepcopy(self.agents)
			n_changes = 0
			for agent in self.old_agents:
				# check if agent is unhappy
				# I don't love this implementation... why not just pass (x,y)?
				if self.is_unsatisfied(agent[0], agent[1]): 
					# print("updating")
					self.move_to_empty(agent)
					n_changes += 1
			self.changes_per_iter.append(n_changes)
			if n_changes == 0:
				# n_changes is zero if everyone is happy
				break

	def move_to_empty(self, key):
		"""
		This method moves the agent to a new house if it is
		unsatisfied.
		"""
		# get the race
		agent = key
		agent_race = self.agents[agent]
		# find a new location
		new_house = random.choice(self.empty_houses)
		# add new location to agents
		self.agents[new_house] = agent_race
		# delete the old agent
		del self.agents[agent]
		# remove the newly filled house from empty houses
		self.empty_houses.remove(new_house)
		# add the old house to the empty_houses list
		self.empty_houses.append(agent)

	def plot(self, title, file_name):
		"""
		This method plots the population of agents on a graph.

		Parameters:
		-----------
		title : string
			The title of the graph
		file_name : string
			The file name of the graph
		"""
		fig, ax = plt.subplots()

		agent_colors = {1:'b', 2:'r', 3:'g', 4:'c', 5:'m', 6:'y', 7:'k'}
		for agent in self.agents: 
			ax.scatter(agent[0]+0.5, agent[1]+0.5, color=agent_colors[self.agents[agent]])

		ax.set_title(title, fontsize=10, fontweight='bold')
		ax.set_xlim(0, self.width)
		ax.set_ylim(0, self.height)
		ax.set_xticks([])
		ax.set_yticks([])
		plt.savefig(file_name)

	def plot_nchanges(self, title, file_name):
		"""
		This method plots how many agents move per iteration

		Parameters:
		-----------
		title : string
			The title of the graph
		file_name : string
			The file name of the graph
		"""
		fig, ax = plt.subplots()
		x = np.arange(0, len(self.changes_per_iter), 1)
		ax.plot(x, self.changes_per_iter, label="Number of Changes per Iteration")
		ax.set_title(title, fontsize=10, fontweight='bold')
		plt.savefig(file_name)


if __name__ == "__main__":

	# first simulation 
	w = 50
	h = 50
	empty_ratio = 0.3
	tol = 0.3
	max_iter = 500
	n_race = 2

	schelling1 = Schelling(w,h, empty_ratio, tol, max_iter, n_race)
	schelling1.populate()

	# initial plot
	schelling1.plot("Two Races: Initial State", '../schelling_1_init.png')

	schelling1.update()
	# final plot
	schelling1.plot("Two Races: Final State", '../schelling_1_final.png')
	schelling1.plot_nchanges("Tolerance = {}%".format(tol*100), '../schelling_1_changes.png')

	# second simulation
	w = 50
	h = 50
	empty_ratio = 0.3
	tol = 0.5
	max_iter = 500
	n_race = 2

	schelling2 = Schelling(w,h, empty_ratio, tol, max_iter, n_race)
	schelling2.populate()

	# initial plot
	schelling2.plot("Two Races: Initial State", '../schelling_2_init.png')

	schelling2.update()
	# final plot
	schelling2.plot("Two Races: Final State", '../schelling_2_final.png')
	schelling2.plot_nchanges("Tolerance = {}%".format(tol*100), '../schelling_2_changes.png')


	# third simulation 
	w = 50
	h = 50
	empty_ratio = 0.3
	tol = 0.8
	max_iter = 500
	n_race = 2

	schelling3 = Schelling(w,h, empty_ratio, tol, max_iter, n_race)
	schelling3.populate()

	# initial plot
	schelling3.plot("Two Races: Initial State", '../schelling_3_init.png')

	schelling3.update()
	# final plot
	schelling3.plot("Two Races: Final State", '../schelling_3_final.png')
	schelling3.plot_nchanges("Tolerance = {}%".format(tol*100), '../schelling_3_changes.png')