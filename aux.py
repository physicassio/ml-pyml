__author__ = 'Cássio Alves'
import sys
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from termcolor import colored
import json
#import time

#function to regularize data when logistic regression is selected.
#Might be a good idea to use for linear regression as well.
def regularize(matrix):
	for column in matrix.columns:
		#regularizes all columns with standard deviation greater than 1(not really sure if 1 is a good value)
		try:	

			st_dev = matrix[column].describe()['std']
			if (st_dev > 1.0):
				matrix[column] = (1./st_dev)*(matrix[column] - matrix[column].mean())
				

		except KeyError:
			continue
#Sigmoid function
def sig(x):
	return np.array(1./(1+np.exp(-x)))

#Function for calculation cross-entropy for logistic regression
def cost_log(x,y,theta,lamb):

	m = len(y)
	g = sig(np.dot(x,theta))
	tt = theta	#array for taking into account regularization 
	tt[0] = 0 	#(recall that the second sum in cross entropy starts at j =1)
	cost = 0.0
	cost = (2./m)*sum(-y*np.log(g)-(1-y)*np.log(1-g))+(lamb/m)*(tt*tt)#+(0.5*lamb/m)*(tt/np.abs(tt))
	#r = (lamb/m)*sum(tt*tt)
	#print(r)
	#for i in range(m):
	#	if (y[i] == 0): 
	#		cost+=(1./m)*np.log(1-g[i])+r#+(0.5*lamb/m)*np.dot(tt,tt)#[i]**2#(np.dot(tt,tt))#+sum(abs(tt)))
	#	else:
	#		cost+=(1./m)*np.log(g[i])+r#+(0.5*lamb/m)*np.dot(tt,tt)#[i]**2#(np.dot(tt,tt))#+sum(abs(tt)))
	#print("cost=",cost)
	return cost

#Function for calculating cost function for linear regression
def cost_linear(x,y,theta):
	
	m = len(y)
	h = np.dot(x,theta)
	cost = (1./m)*(sum((h-y).dot(x)))**2
	return cost

#Gradient descent for linear regression
def grad_desc_linear(x,y,theta,alpha,n_iter,exp):

	m = len(y)
	c = []	
	for i in range(n_iter+1): 

		h = x.dot(theta)
		grad = (2./m)*np.dot((h-y).T,x)
		theta = theta - alpha*grad
		c.append(cost_linear(x,y,theta))
		if i%100 ==0:
			
			print(colored("grad="+str(grad)+"\ttheta="+str([theta[i]**(1./exp[i]) for i in range(len(theta))])+" in the "+str(i)+"th iteration",'green'))

	plt.plot(range(len(c)),np.array(c),'--')
	plt.ylabel('Cost Function')
	plt.xlabel('Iterations')
	plt.show()
	return(grad,theta)

#Gradient descent for logistic regression
def grad_desc_log(x,y,theta,alpha,lamb,n_iter):
	
	m = len(y)
	#print(x)
	c = []
	cost = []
	for i in range(int(n_iter+1)):
		g = sig(x.dot(theta))

		tt = np.array(list(theta))
		#print(theta)
		tt[0] = 0
		
		
		grad = (1./m)*(np.dot((g-y).T,x))+(lamb/m)*(tt.T)#+(0.5*lamb/m)*(tt/np.sqrt(tt))
		theta = theta - alpha*grad
		#print(theta)
		#sys.exit()
		#c.append(np.dot(grad,grad)) #Useful for checking gradient convergence
		c.append(cost_log(x,y,theta,lamb))
		if i%100 ==0:
			print(colored("grad="+str(grad)+"\ttheta="+str(theta)+" in the "+str(i)+"th iteration",'green'))
	plt.plot(range(len(c)),np.array(c),'--')
	plt.ylabel('Cost Function')
	plt.xlabel('Iterations')
	plt.show()
	return (grad,theta)

#function to get features' exponents (generalize to arbitrary order polinomials)
def get_expo(x,y):
	n = len(y)
	expos = []
	coeffs = []
	Y = np.log10(y)
	for column in x.columns:
		column = np.log10(x[column])
		den = n*np.dot(column,column)-sum(column)**2
		expo = (n*np.dot(column,Y)-sum(column)*sum(Y))/den
		coef = (sum(y)*np.dot(column,column)-sum(column)*np.dot(y,column))/den
		#down = n*np.dot(column,column)-sum(column)**2#sum(column)
		expos.append(np.round(expo,2))
		coeffs.append(np.round(10**coef,2))
	return expos,coeffs

#function to export results to a json file	
def export_json(fil,dic):
	open(fil,'w').write(json.dumps(dic))
	
#function to look for past results for logistic regression performed on the same data file
#this function is called in pyml.py and if the past accuracy is greater than the current one, the current results are dismissed.
def check_past_result(fil):

	try:
		past_results = json.load(open(fil,'r'))
		return(past_results['accuracy'])
		
	
	except FileNotFoundError:
		return(-1)
	
	
	
	
