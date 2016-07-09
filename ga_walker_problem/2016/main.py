#!/usr/bin/env python2.7

from walker import walker
from simulation import simulation
import genetic
from math import *
import pickle

import random

class Robot(genetic.Individual):
	optimization = genetic.MINIMIZE
	def __init__(self, chromosome=None):
		# Constructor
		# Defines the genes and max,min ranges
		self.genes = { \
				'ul':(30.0,80.0), \
				'll':(30.0,80.0), \
				'lua':(-pi/5.0,pi/5.0), \
				'rua':(-pi/5.0,pi/5.0), \
				'lla':(0.0,pi/3.0), \
				'rla':(0.0,pi/3.0), \
				}
		self.bits_per_gene = 9
		self.length = len(self.genes.keys())*self.bits_per_gene
		# Super class constructor
		super(Robot, self).__init__(chromosome)
	def get_gene(self, gene_name):
		i = self.genes.keys().index(gene_name)
		bin_gene = ''
		for int_bit in self.chromosome[i*self.bits_per_gene:\
				(i+1)*self.bits_per_gene]:
			if int_bit:
				bit = '1'
			else:
				bit = '0'
			bin_gene = bin_gene + bit
		int_gene = int(bin_gene, 2)
		float_gene = float(int_gene) / (2**self.bits_per_gene)
		gene_min = float(self.genes[gene_name][0])
		gene_max = float(self.genes[gene_name][1])
		gene = gene_min + float_gene*(gene_max - gene_min)
		return gene
	def evaluate(self, optimum=None):
		# Evaluate the individual
		if random.random() > 0.99:
			show = True
		else:
			show = False
		sim = simulation(show=show) # Create the simulation
		delta = 0.02
		# Create the robot
		pos_x = 500
		pos_y = 350
		w = 15
		wlk = walker(sim.space, \
				(pos_x, pos_y), \
				self.get_gene('ul'), \
				self.get_gene('ll'), \
				w, \
				self.get_gene('lua'), \
				self.get_gene('lla'), \
				self.get_gene('rua'), \
				self.get_gene('rla'))
		# Test the robot in the simulation
		running = True
		while running:
			sim.step(delta)
			ke = sim.get_ke()
			if ke < 4000.0 or ke > 1000000000.0:
				running = False
		# The score minimizes x
		self.score = wlk.lul.body.position[0] + \
				wlk.rul.body.position[0]
	def mutate(self, gene):
		self.chromosome[gene] = not self.chromosome[gene]

class myEnv(genetic.Environment):
	def __init__(self, filename, kind, maxgenerations):
		# Try to load the file
		self.filename = filename
		try:
			data = pickle.load(open(self.filename,'rb'))
		except:
			data = {}
		if 'population' in data:
			population = data['population']
		else:
			population = None
		if 'generation' in data:
			generation = data['generation']
		else:
			generation = 0
		# Initialize the environment super class
		super(myEnv, self).__init__(kind, population=population, \
				maxgenerations=maxgenerations, \
				generation=generation)
	def report(self):
		# Report results and save
		print '='*70
		print "generation: ", self.generation
		print "best:       ", self.best
		data = { \
				'population':self.population, \
				'generation':self.generation, \
		}
		pickle.dump(data, open(self.filename,'wb'))

if __name__ == "__main__":
	env = myEnv('data', Robot, maxgenerations=1000000)
	env.run()

