"""
Author : Tharindra Galahena (inf0_warri0r)
Project: flocking algorithm
Blog   : http://www.inf0warri0r.blogspot.com
Date   : 14/12/2012
License:
 
     Copyright 2012 Tharindra Galahena

This program is free software: you can redistribute it and/or modify it under the terms of 
the GNU General Public License as published by the Free Software Foundation, either 
version 3 of the License, or (at your option) any later version. This program is distributed
in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied 
warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General 
Public License for more details.
*
You should have received a copy of the GNU General Public License along with This program. 
If not, see http://www.gnu.org/licenses/.

"""

import sys, os
import random

MAX_SPEED          =  10.0
SEPARATION_RADIOUS =  20.0
COHESION_RADIOUS   = 100.0

class bird:
	def __init__(self, w, h, cr, ar, sr):
		self.weight          = w
		self.height          = h  
		self.cohesion_rate   = cr
		self.alignment_rate  = ar
		self.separation_rate = sr
		self.location = [random.randrange(0, self.weight), random.randrange(0, self.height )]
		self.valocity = [random.uniform(-1, 1), random.uniform(-1, 1)]
		
		self.location_new = [random.randrange(0, self.weight), random.randrange(0, self.height)]
		self.valocity_new = [random.uniform(-1, 1), random.uniform(-1, 1)]
		
	def avarage_possition(self, neighbours):
		if len(neighbours) == 0:
			return 0
		x = 0.0
		y = 0.0
		for i in range(0, len(neighbours)):
			x = x + neighbours[i].location[0]
			y = y + neighbours[i].location[1]
			
		return [x / len(neighbours), y / len(neighbours)]
	
	def avarage_valocity(self, neighbours):
		
		x = 0.0
		y = 0.0
		for i in range(0, len(neighbours)):
			x = x + neighbours[i].valocity[0]
			y = y + neighbours[i].valocity[1]
			
		return [x / len(neighbours), y / len(neighbours)]
	
	def distence(self, neighbour):
		d = (self.location[0] - neighbour.location[0] - neighbour.valocity[0]) ** 2
		d = d + (self.location[1] - neighbour.location[1] - neighbour.valocity[1]) ** 2
		return d ** 0.5	
				
	def cohesion(self, neighbours):
		if len(neighbours) == 0:
			return [0, 0]
		d = self.avarage_possition(neighbours);
		v = [0.0, 0.0]
		v[0] = ((d[0] - self.location[0]) / 70.0) * MAX_SPEED
		v[1] = ((d[1] - self.location[1]) / 70.0) * MAX_SPEED
		return v

	def alignment(self, neighbours):
		if len(neighbours) == 0:
			return [0, 0]
		v = self.avarage_valocity(neighbours)
		
		if v[0] > MAX_SPEED:
			v[0] = MAX_SPEED
		elif v[0] < -1.0 * MAX_SPEED:
			v[0] = -1.0 * MAX_SPEED
		if v[1] > MAX_SPEED:
			v[1] = MAX_SPEED
		elif v[1] < -1.0 * MAX_SPEED:
			v[1] = -1.0 * MAX_SPEED
		
		return v
	
	def separation(self, neighbours):
		if len(neighbours) == 0:
			return [0, 0]
		tmp = list()
		for j in range(0, len(neighbours)):
			if self.distence(neighbours[j]) < SEPARATION_RADIOUS:
				tmp.append(neighbours[j])
				
		if len(tmp) == 0:
			return [0, 0]
			
		d = self.avarage_possition(tmp)
		v = [0.0, 0.0]
		if(d[0] - self.location[0] != 0.0): 
			v[0] = -1.0 * (80.0 / (d[0] - self.location[0])) * MAX_SPEED
		else:
			v[0] = 0.0
		if (d[1] - self.location[1] != 0.0):
			v[1] = -1.0 * (80.0 / (d[1] - self.location[1])) * MAX_SPEED
		else:
			v[1] = 0.0
			
		if v[0] == 0.0 and v[1] == 0.0:
			v[0] = -1.0
			v[1] = -1.0
		
		
		return v	
			
	def move(self, neighbours):
		
		self.location_new[0] = self.location[0] + self.valocity[0]
		if self.location_new[0] >= self.weight:
			self.location_new[0] = self.location_new[0] - self.weight
		elif self.location_new[0] < -1:
			self.location_new[0] = self.location_new[0] + self.weight
			
		self.location_new[1] = self.location[1] + self.valocity[1]
		if self.location_new[1] >= self.height :
			self.location_new[1] = self.location_new[1] - self.height 
		elif self.location[1] < -1:
			self.location_new[1] = self.location_new[1] + self.height 
			
		v1 = self.cohesion(neighbours)
		v2 = self.alignment(neighbours)
		v3 = self.separation(neighbours)

		v1[0] = self.cohesion_rate * v1[0]
		v1[1] = self.cohesion_rate * v1[1]
		v2[0] = self.alignment_rate * v2[0]
		v2[1] = self.alignment_rate * v2[1]
		v3[0] = self.separation_rate * v3[0]
		v3[1] = self.separation_rate * v3[1]
		
		self.valocity_new[0] = (0.2*self.valocity[0] + v1[0] + v2[0] + v3[0]) / 2.0
		self.valocity_new[1] = (0.2*self.valocity[1] + v1[1] + v2[1] + v3[1]) / 2.0
		
	def swap(self):
		self.valocity[0] = self.valocity_new[0]
		self.valocity[1] = self.valocity_new[1]
		self.location[0] = self.location_new[0]
		self.location[1] = self.location_new[1]
		
class flock:
	
	def __init__(self, w, h, n, cohesion_rate, alignment_rate, separation_rate):
		self.num = n
		self.birds = list()
		for i in range(0, self.num):
			tmp = bird(w, h, cohesion_rate, alignment_rate, separation_rate)
			self.birds.append(tmp)
	
	def fream(self):
		na = list()
		for i in range(0, self.num):
			tmp = list()
			for j in range(0, self.num):
				if i == j:
					continue
				if self.birds[i].distence(self.birds[j]) < COHESION_RADIOUS:
					tmp.append(self.birds[j])
			na.append(tmp)
		for i in range(0, self.num):
			self.birds[i].move(na[i])
		for i in range(0, self.num):
			self.birds[i].swap()

