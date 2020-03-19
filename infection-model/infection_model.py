# A simple infection model, similar to the Schelling Model but with different rules.

import matplotlib.pyplot as plt
import numpy as np
import itertools
import random 
import copy 
from list_funcs import intersection


class VirusModel(object):
	"""A model of virus spreading"""
	def __init__(self, height, width, mortality, cycle_time, ratio_empty, ratio_infected, num_iter, max_range=1):
		super(VirusModel, self).__init__()
		self.height = height
		self.width = width
		self.mortality = mortality
		self.ratio_empty = ratio_empty
		self.ratio_infected = ratio_infected
		self.cycle_time = cycle_time
		self.num_iter = num_iter
		self.max_range = max_range


		self.infected_agents = {}
		self.healthy_agents = {}
		# tracks the number of healthy vs infected people at each timestep
		self.infected_population = []
		self.healthy_population = []
		self.deaths_per_iter = []


	def populate(self):
		"""
		This method is used to initially populate a grid with randomly
		distributed people that can move around.
		"""
		# create the grid
		self.grid = list(itertools.product(range(0,self.height), range(0,self.width)))
		random.shuffle(self.grid)

		# initialize populations
		self.n_empty = int(self.ratio_empty * len(self.grid))
		self.empty_spots = self.grid[:self.n_empty]
		self.inhabited = self.grid[self.n_empty:]

		self.n_infected = int(ratio_infected*len(self.inhabited))
		healthy = self.inhabited[self.n_infected:]
		infected = self.inhabited[:self.n_infected]

		self.healthy_agents = dict(list(self.healthy_agents.items()) + list(dict(zip(healthy, 
			[0]*len(healthy))).items()))

		self.infected_agents = dict(list(self.infected_agents.items()) + list(dict(zip(infected, 
			[0]*len(infected))).items()))


	def contracted(self, agent):
		"""
		This method checks if any of an agent contracts the virus
		by checking if any of the neighbors are infected
		"""
		x = agent[0]
		y = agent[1]

		# get the neighbors of the agent
		neighbors = list(itertools.product(range(x-1,x+2), range(y-1,y+2)))
		neighbors.remove((x,y)) # remove the current agent
		inf_neighbors = intersection(neighbors, self.infected_agents) # get inhabited neighbors list

		if len(inf_neighbors) > 0:

			self.infected_agents[agent] = 0
			del self.healthy_agents[agent]
			return True
		else: 
			return False


	def recovered(self, agent):
		days_ill = self.infected_agents[agent]
		if days_ill > cycle_time: 
			self.healthy_agents[agent] = 0
			del self.infected_agents[agent]
			return True		
		else:
			self.infected_agents[agent] += 1
			return False


	def update(self):
		"""
		This method executest an asynchronous update for the model
		"""

		# add initial population
		self.infected_population.append(len(self.infected_agents))
		self.healthy_population.append(len(self.healthy_agents))

		for i in range(self.num_iter):
			n_deaths = 0
			# create a copy of the old agents
			self.old_h_agents = copy.deepcopy(self.healthy_agents)
			self.old_i_agents = copy.deepcopy(self.infected_agents)


			for agent in self.old_i_agents:
				roll = random.random()
				if roll <= self.mortality: 
					del self.infected_agents[agent]
					n_deaths += 1

				elif self.recovered(agent):
					self.move_to_empty(agent, False)

				else: 
					self.move_to_empty(agent, True)

			for agent in self.old_h_agents:
				# check if agent gets sick
				if self.contracted(agent):
					# move agent
					self.move_to_empty(agent, True) 
				else:
					# move agent
					self.move_to_empty(agent, False) 


			self.healthy_population.append(len(self.healthy_agents))
			self.infected_population.append(len(self.infected_agents))
			self.deaths_per_iter.append(n_deaths)
			if len(self.infected_agents) == 0:
				# simulation stops if there are no more infected people
				break


	def move_to_empty(self, agent, inf):
		"""
		This method moves the agent to an empty nearby square
		"""

		x = agent[0]
		y = agent[1]

		neighbors = list(itertools.product(range(x-self.max_range,x+(self.max_range+1)), 
			range(y-self.max_range,y+(self.max_range+1))))
		# neighbors.remove((x,y)) # remove the current agent --> forces movement
		neighbors = intersection(neighbors, self.empty_spots) # get inhabited neighors list

		# select a random new empty spot
		if len(neighbors) > 0:
			new_spot = random.choice(neighbors)
		else:
			return
		if not inf:
			self.healthy_agents[new_spot] = 0
			del self.healthy_agents[agent]
		else: 
			self.infected_agents[new_spot] = self.infected_agents[agent]
			del self.infected_agents[agent]

		self.empty_spots.remove(new_spot)
		self.empty_spots.append(agent)



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

		for agent in self.healthy_agents: 
			ax.scatter(agent[0]+0.5, agent[1]+0.5, color='g')
		for agent in self.infected_agents: 
			ax.scatter(agent[0]+0.5, agent[1]+0.5, color='b')


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
		x1 = np.arange(0, len(self.healthy_population), 1)
		x2 = np.arange(0, len(self.infected_population), 1)
		x3 = np.arange(0, len(self.deaths_per_iter), 1)
		ax.plot(x1, self.healthy_population, label="Healthy Population", color='g')
		ax.plot(x2, self.infected_population, label="Infected Population", color='b')
		ax.plot(x3, np.array(self.deaths_per_iter).cumsum(), label="Cumulative Deaths", color='r')

		ax.legend()
		ax.set_xlabel("Iteration Number")
		ax.set_ylabel("Population")
		ax.set_title(title, fontsize=10, fontweight='bold')
		plt.savefig(file_name)


if __name__ == '__main__':
	
	width, height = 50, 50
	death_rate = 0.03
	cycle_time = 14
	max_iter = 500
	ratio_empty = 0.9
	ratio_infected = 0.01
	max_range = 1

	virus1 = VirusModel(height, width, death_rate, cycle_time, 
		ratio_empty, ratio_infected, max_iter, max_range)

	virus1.populate()
	virus1.plot("Onset of Outbreak", "./figures/virus1_init.png")
	virus1.update()
	virus1.plot("End of Outbreak", "./figures/virus1_final.png")
	virus1.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus1_populations.png")

	ratio_empty = 0.95
	virus1_2 = VirusModel(height, width, death_rate, cycle_time, 
	ratio_empty, ratio_infected, max_iter, max_range)

	virus1_2.populate()
	virus1_2.plot("Onset of Outbreak", "./figures/virus1_2_init.png")
	virus1_2.update()
	virus1_2.plot("End of Outbreak", "./figures/virus1_2_final.png")
	virus1_2.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus1_2_populations.png")

	death_rate = 0.06
	ratio_empty = 0.9
	virus2 = VirusModel(height, width, death_rate, cycle_time, 
		ratio_empty, ratio_infected, max_iter, max_range)

	virus2.populate()
	virus2.plot("Onset of Outbreak", "./figures/virus2_init.png")
	virus2.update()
	virus2.plot("End of Outbreak", "./figures/virus2_final.png")
	virus2.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus2_populations.png")

	ratio_empty = 0.95
	virus2_2 = VirusModel(height, width, death_rate, cycle_time, 
	ratio_empty, ratio_infected, max_iter, max_range)

	virus2_2.populate()
	virus2_2.plot("Onset of Outbreak", "./figures/virus2_2_init.png")
	virus2_2.update()
	virus2_2.plot("End of Outbreak", "./figures/virus2_2_final.png")
	virus2_2.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus2_2_populations.png")


	death_rate = 0.12
	ratio_empty = 0.9
	virus3 = VirusModel(height, width, death_rate, cycle_time, 
		ratio_empty, ratio_infected, max_iter, max_range)

	virus3.populate()
	virus3.plot("Onset of Outbreak", "./figures/virus3_init.png")
	virus3.update()
	virus3.plot("End of Outbreak", "./figures/virus3_final.png")
	virus3.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus3_populations.png")

	ratio_empty = 0.95
	virus3_2 = VirusModel(height, width, death_rate, cycle_time, 
	ratio_empty, ratio_infected, max_iter, max_range)

	virus3_2.populate()
	virus3_2.plot("Onset of Outbreak", "./figures/virus3_2_init.png")
	virus3_2.update()
	virus3_2.plot("End of Outbreak", "./figures/virus3_2_final.png")
	virus3_2.plot_nchanges("Population Trends: Death Rate={}%, Sparsity={}%".format(death_rate*100, ratio_empty*100), 
		"./figures/virus3_2_populations.png")