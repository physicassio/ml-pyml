import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import sys
import math
import aux
from termcolor import colored
import random
import visualize as vi
import time

__author__ = 'Cássio Alves'

#Disable pandas' alert when inserting arrays in columns
pd.options.mode.chained_assignment = None

#Function to get columns in selected file
def get_columns(in_file):#,reg_type):

	try:
		data = pd.read_csv(in_file,encoding='latin1')
		
	except:
		sys.exit(colored('File '+str(in_file)+' does not seem to be a valid CSV file','red',attrs=['bold']))
	#selecting only numeric columns in selected file
	dataint = data[data.columns[data.dtypes=='int64']]
	datafloat = data[data.columns[data.dtypes=='float64']]
	
	#setting a dummy name for row index so the data can be merged based on this index
	data.index.name = 'dummy_index'
	data = pd.merge(dataint,datafloat,on='dummy_index')
	columns = data.columns
	
	
	
	print(colored('Numeric columns in file %s'%(in_file),'blue',attrs=['bold']))
	for i in range(len(columns)):
		
		#+1 so user does not need to type in 0
			print(colored(str(i+1)+'-'+columns[i]+' '+str(data[columns[i]].dtypes),'green',attrs=['bold']))

	inp = ''
	chosen_columns = []
	while (inp != 'q'):
		inp = input(colored('Choose one column and press Enter or type in \'0\' to finish selecting. (Type in \'a\' to choose all columns at once) ','white',attrs=['bold']))	

			
		if (inp == 'a'):
			
			chosen_columns = list(columns)
			break
			

		elif (int(inp) == 0):
			break
			
		elif (int(inp) in range(1,len(columns)+1)):
		
			data[columns[int(inp)-1]]
			chosen_columns.append(columns[int(inp)-1])
		
		else:
		
			print(colored('Invalid column. Please, select a valid column name ','red',attrs=['bold']))


	selected_data = data[chosen_columns]
	
	#Prompting user for what kind of regression to perform
	mod = ''
	print(colored("1 - Logistic\n2 - Linear",'green',attrs=['bold']))
	mod = int(input(colored("Which type of regression do you want to perform? ",'white',attrs=['bold'])))
	while (1>0):
		if (mod == 1):		
			reg_type = 'logistic'
			break
		elif (mod == 2):
			reg_type = 'linear'
			break
		else:
			print(colored("Invalid option. Please, select [1] for logistic regression or [2] for linear regression ",'red',attrs=['underline','bold']))
			mod = int(input(colored("Which type of regression do you want to perform? ",'cyan',attrs=['bold'])))	
	check_data(selected_data,reg_type)

	print(colored("Chosen columns:",'blue',attrs=['bold']))

	for i in range(len(chosen_columns)):
		print(colored(str(i+1)+'-'+chosen_columns[i],'green',attrs=['bold']))
	
	#asks the user for the dependent variable column
	target = int(input(colored('Choose the target column ','white',attrs=['bold'])))
	tar = selected_data[chosen_columns[target-1]]
	target_name = chosen_columns[target-1]
	
	print(colored("You chose '"+str(chosen_columns[target-1])+"' as your target column ",'yellow',attrs=['bold']))
	
	#removing target column from the chosen columns list, so the function can return x and y arrays separately
	chosen_columns.pop(target-1)
	final_data = pd.DataFrame(selected_data[chosen_columns])

	check_data(selected_data,reg_type)
	#plotting features against target column
	plo = ''
	plo = str(input(colored("Do you want to visualize your data before analyzing it? [y/n]",'white',attrs=['bold'])))
	#mod = int(input(colored("Which type of regression do you want to perform? ",'white',attrs=['bold'])))
	while (1>0):
		if (plo == 'y'):		
			vi.main(final_data,tar)
			break
		elif (plo == 'n'):
			#reg_type = 'linear'
			break
		else:
			print(colored("Invalid option. Please, select y or n ",'red',attrs=['underline','bold']))
			plo = str(input(colored("Do you want to visualize your data before analyzing it? [y/n] ",'cyan',attrs=['bold'])))	
	
	
	#adding bias column to x array
	add_bias(final_data)
	chosen_columns.insert(0,'bias')

	return np.array(final_data),np.array(tar),reg_type,chosen_columns,target_name

	
#Function to add bias column to dataframe
def add_bias(data):
	size = data.shape[0]
	data.insert(0,'bias',np.ones(size))

#Function to check if x-columns have NaN values and asks if user wants to replace with column Gaussian distributed values(based in the column properties themselves)
#Might be a good idea to implement replacing with values other the mentioned above
def check_data(data,reg_type):

	for column in data:
		col = data[column]
		
		#variable to calculate how much data is missing
		missing = len(col[pd.isna(col)])/len(col)

		if (col.dtypes == np.float64) and (missing != 0.0):

			warning = str(col) + " is missing %.2f%s of its total length (NaN values)"%(missing*100,'%')
			new_column = np.array(col)
			feed = np.random.normal(col.mean(),col.std(),len(col[pd.isna(col)]))
			new_column[(pd.isna(new_column))] = feed
			print(colored(warning,'red'))
			decision = input(colored("Do you want to fill NaN values with Gaussian distributed values based on the column's properties themselves?(y/n) ",'white',attrs=['bold']))
			while (1>0):

				if (decision == 'y'):

					new_column = np.array(col)
					feed = np.random.normal(col.mean(),col.std(),len(col[pd.isna(col)]))
					new_column[(pd.isna(new_column))] = feed
					data[column] = new_column
					break
				elif (decision == 'n'):
					break
				else:
					print(colored("Please type in 'y' or 'n'",'white',attrs=['bold']))
					decision = input(colored("Do you want to fill NaN values with Gaussian distributed values based on the column's properties themselves?(y/n) ",attrs=['bold']))
			
			#plt.plot(col,np.exp(-((col-col.mean())**2)/(4*col.std()**2)),'ro')
			#plt.show()


	if (reg_type == 'logistic'):

		aux.regularize(data)

#This is where the fun really begins :)
def logistic(x,y):	

	train_x = x[:int(0.7*len(x))]
	train_y = y[:int(0.7*len(y))]
	
	test_x = x[int(0.7*len(x)):]
	test_y = y[int(0.7*len(y)):]
	
	#Reading alpha, number of iterations and lambda
	alpha = ' '	
	while (type(alpha) is not int) or (type(alpha) is not float):
		try:
			alpha = float(input(colored("What learning rate do you want to use?(It's recommended values in range [0.0001-1.0]) ",'white',attrs=['bold'])))
			break
		except KeyboardInterrupt:
			sys.exit('Exitting...')
		except:
			print(colored("The learning rate must be a number",'red',attrs=['bold']))
	n = ''
	while (type(n) is not int):
		try:
			n = int(input(colored("How many iterations do you want to run? ",'white',attrs=['bold'])))
			break
		except KeyboardInterrupt:
			sys.exit('Exitting...')
		except:
			print(colored("Number of iterations must be a whole number",'red',attrs=['bold']))
	lamb = ''
	while (type(lamb) is not float) or (type(lamb) is not int):
		try:
			lamb = float(input(colored("What regularization parameter(lambda) do you want to use? ",'white',attrs=['bold'])))
			break
		except KeyboardInterrupt:
			sys.exit('Exitting...')
		except:
			print(colored("lambda must be a number",'red',attrs=['bold']))

	theta = (np.ones(train_x.shape[1])).T		
	grad,theta = aux.grad_desc_log(train_x,train_y,theta,alpha,lamb,n)
	
	
	#Checking whether there are any NaN values in weights' array
	for value in theta:
		if (np.isnan(value)):
			sys.exit(colored('Nan values found in weights\' array. Try changing your parameters (e.g. lambda and/or alpha) ','red',attrs=['bold']))
			
	#theta = (np.ones(train_x.shape[1])).T
	print(colored("Final values for grad="+str(grad)+"\ttheta="+str(theta)+" obtained by using Gradient Descent",'green',attrs=['bold']))
	
	#array for plotting sigmoid function to with the learned weights	
	xp = np.linspace(min(test_x.dot(theta)),max(test_x.dot(theta)),len(test_y))
	result = aux.sig(test_x.dot(theta))

	#setting threshold for success or failure
	result[(result > 0.5 )] = 1
	result[(result <= 0.5)] = 0
	
	accu = np.mean(result == test_y)
	print(colored("The model predicted %d samples right (out of %d), resulting in an accuracy = %.3f"%(len(result[result == test_y]),len(test_y),accu),'white',attrs=['bold']))
		
	#plots for comparison
	#vi.visualize_result(x,y,cols)	
	plt.plot(xp,aux.sig(xp),label = 'sigmoid function')	#sigmoid function
	plt.plot(test_x.dot(theta),test_y,'ro',label = 'testing set')	#original data
	plt.plot(test_x.dot(theta),result,'b+',label = 'predictions')#data using learned weights
	plt.legend()
	plt.show()
	return(list(theta),accu)

def linear(x,y,cols):

	#Reading alpha and number of iterations
	alpha = ' '	
	while (type(alpha) is not int) or (type(alpha) is not float):
		try:
			alpha = float(input(colored("What learning rate do you want to use?(It's recommended values in range [0.0001-1.0]) ",'white',attrs=['bold'])))
			break
		except KeyboardInterrupt:
			sys.exit('Exitting...')
		except:
			print(colored("The learning rate must be a number",'red',attrs=['bold']))
	n = ''
	while (type(n) is not int):
		try:
			n = int(input(colored("How many iterations do you want to run? ",'white',attrs=['bold'])))
			break
		except KeyboardInterrupt:
			sys.exit('Exitting...')
		except:
			print(colored("Number of iterations must be a whole number",'red',attrs=['bold']))

	#getting exponents for linear regression, in case there is any non-linear polinomial feature
	exp,coe = aux.get_expo(pd.DataFrame(x).drop(0,1),y)

	exp.insert(0,1)

	for i in range(len(exp)):

		if exp[i] > 1.0:
			x[:,i] = x[:,i]**exp[i]

	theta = 0*(np.ones(x.shape[1])).T	
	
	grad,theta = aux.grad_desc_linear(x,y,theta,alpha,n,exp)

	#Checking whether there are any NaN values in weights' array	
	for value in theta:
		if (np.isnan(value)):
			sys.exit(colored('Nan values found in weights\' array. Try changing your parameters (e.g. lambda and/or alpha) ','red',attrs=['bold']))
			
	print(colored("Final values for grad="+str(grad)+"\ttheta="+str([theta[i]**(1./exp[i]) for i in range(len(theta))])+" obtained by using Gradient Descent",'green',attrs=['bold']))

	#Computing theta using the normal equation
	xtx = np.linalg.inv((x.T).dot(x))
	normal_theta = xtx.dot((x.T).dot(y))
	print(colored("Final value for theta using the Normal Equation\t"+str([normal_theta[i]**(1./exp[i]) for i in range(len(normal_theta))]),'green',attrs=['bold']))
		
	vi.visualize_result(theta,x,y,exp,cols)
	return(list(theta))
		
if __name__ == '__main__':
	main()
