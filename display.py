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

from Tkinter import *
import sys, os
import random
import flock

num_birds       =  100
cw              = 1000
ch              =  600
cycle           =   50

cohesion_rate   =  1.0
alignment_rate  =  2.3
separation_rate =  0.2
		
fl = flock.flock(cw, ch, num_birds, cohesion_rate, alignment_rate, separation_rate)
root = Tk()
root.title("flocking alogithm")

cnv = Canvas(root, width=cw, height=ch, background="black")
cnv.grid(row=0, column=0)
posn_x = 0.0
posn_y = 0.0

while 1 :
	
	fl.fream()
	for i in range(0, num_birds):
		posn_x = fl.birds[i].location[0]
		posn_y = fl.birds[i].location[1]
		x = fl.birds[i].valocity[0]
		y = fl.birds[i].valocity[1]
		d = (x * x + y * y) ** 0.5
		sinx = 0.0
		cosx = 0.0
		
		if d != 0.0:
			sinx = x / d
			cosx = y / d
		
		x1 = 0.0
		y1 = 0.0
		
		if x*y >= 0.0:
			x1 = posn_x + 10.0 * cosx
			y1 = posn_y + 10.0 * sinx
		else:
			x1 = posn_x - 10.0 * cosx
			y1 = posn_y - 10.0 * sinx
			
		x2 = posn_x + 2.0 * sinx
		y2 = posn_y - 2.0 * cosx
		
		x3 = posn_x - 2.0 * sinx
		y3 = posn_y + 2.0 * cosx
		
		points = [x1, y1, x2, y2, x3, y3]
		cnv.create_polygon(points, outline="green", fill='yellow', width=1)
		
	cnv.update()                
	cnv.after(cycle)                                        
	cnv.delete(ALL)
    	
root.mainloop()
