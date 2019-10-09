import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
import pandas as pd
import sys
from mpl_toolkits.mplot3d import Axes3D

def main(columns,target):
#	print(columns)
	print(target.name)
	fig = plt.figure()
	qtd = columns.shape[1]
	#print(qtd)
	#exit()
	n_rows = np.ceil(qtd/2)
	print(n_rows)

	for column in columns:
		frame_pos = lambda x: 1 if(x%2 == 1) else 2
		#print(columns.columns.get_loc(column))
		#print(columns.index(column))
		col_ind = columns.columns.get_loc(column)
		#print(frame_pos(col_ind))
		#print(col_ind)
		
		ax = fig.add_subplot(n_rows,2,col_ind+1)
		ax.plot(columns[column],target,'ro')
		ax.set_ylabel(target.name)
		ax.set_xlabel(column)
		#exit()
		#continue	
		#plt.xlabel(column)
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()
	input(colored('Press Enter to continue...',attrs=['bold']))

def visualize_result(theta,columns,target):
	"""fig=plt.figure()
	ax = fig.add_subplot(111,projection='3d')
	x = np.linspace(min(columns[1]),max(columns[1]),np.size(columns[1]))
	y = np.linspace(min(columns[2]),max(columns[2]),np.size(columns[2]))
	X = np.outer(np.ones(np.size(x)),x)
	Y = np.outer(np.ones(np.size(y)),y)
	z = np.outer(np.ones(np.size(target)),target)
	#ax.scatter(columns[1],columns[2],target)
	#ax.plot(columns[1]*theta[1],target,zdir='y')
	#ax.plot(columns[2]*theta[2],target,zdir='x')
	
	ax.scatter(list(columns[1]),list(columns[2]),target)
	#X,Y = np.meshgrid(columns[1],columns[2])
	#plt.plot(theta[1]*columns[1],target)
	#plt.plot(theta[2]*columns[2],target)
	#Z = columns.dot(theta)
	#fig = plt.figure()
	#ax = fig.add_subplot(111,projection='3d')
	ax.plot_surface(X,Y,z)
	plt.show()
	#print(columns)"""
	for column in columns:
		#ax.plot_surface(x,y,z)
		plt.plot(columns[column],target,'o')
		plt.plot(columns[column],theta[0]+theta[column]*columns[column])
		plt.show()
		
if __name__ == '__main__':
	main(columns,target)
