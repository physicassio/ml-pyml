import numpy as np
import matplotlib.pyplot as plt
from termcolor import colored
import pandas as pd
import sys
from mpl_toolkits.mplot3d import Axes3D

def main(columns,target):

	print(target.name)
	fig = plt.figure()
	qtd = columns.shape[1]
	n_rows = np.ceil(qtd/2)
	print(n_rows)

	for column in columns:

		col_ind = columns.columns.get_loc(column)
		
		ax = fig.add_subplot(n_rows,2,col_ind+1)
		ax.plot(columns[column],target,'ro')
		ax.set_ylabel(target.name)
		ax.set_xlabel(column)
		
	mng = plt.get_current_fig_manager()
	mng.resize(*mng.window.maxsize())
	plt.show()
	input(colored('Press Enter to continue...',attrs=['bold']))

def visualize_result(theta,x,target,exp,cols):

	
#	for column in columns:
#		plt.plot(columns[column]**(1./exp[column]),target,'o')
#		plt.plot(columns[column]**(1./exp[column]),theta[0]+(theta[column]*columns[column]),label='%.3f x_%s + %.3f'%(theta[column]**(1./exp[column]),column,theta[0]))
#		plt.xlabel(cols[column])"""
	#print(columns.shape[1])
	for column in range(x.shape[1]):

		plt.plot(x[:,column]**(1./exp[column]),target,'o')
		plt.plot(x[:,column]**(1./exp[column]),theta[0]+(theta[column]*x[:,column]),label='%.3f x_%s + %.3f'%(theta[column]**(1./exp[column]),column,theta[0]))
		plt.xlabel(cols[column])
		plt.legend()
		plt.show()
		
if __name__ == '__main__':
	main(columns,target)
