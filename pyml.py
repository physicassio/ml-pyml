import sys
import math
import pandas as pd
import numpy as np
import os
import subprocess as sp
import glob
from termcolor import colored
from colorama import Fore, Back, Style
import analysis as an
import aux
import matplotlib.pyplot as plt

__author__ = "Cássio Alves"
__version__ = "1.0[beta]"

version_string = colored(str(__version__),'red')


print(colored("\t                       _",'yellow',attrs=['dark','bold']))
print(colored("\t _ __  _   _ _ __ ___ | |",'yellow',attrs=['dark','bold']))
print(colored("\t| '_ \| | | | '_ ` _ \| |",'yellow',attrs=['dark','bold']))
print(colored("\t| |_) | |_| | | | | | | |",'yellow',attrs=['dark','bold']))
print(colored("\t| .__/ \__, |_| |_| |_|_|",'yellow',attrs=['dark','bold']))
print(colored("\t|_|    |___/\t"   +version_string,'yellow',attrs=['dark','bold']))

#Function to display files in a directory
def get_files(directory):

	#print(directory)
	while (1>0):
		if (os.path.exists(directory)):
			break
		else :
			directory = input(colored("Invalid path. Please, provide a valid path ",'red',attrs=['bold']))
	if (directory[-1] != '/'):
		directory+='/'
	file_list = glob.glob(directory+'*')
	file_list.insert(0,'offset')
	print(colored("Files in directory"+str(directory),'blue',attrs=['bold']))

	#Printing files in the selected directory for user to choose
	for i in range(1,len(file_list)):
		fil = file_list[i]
		if os.path.isdir(fil):
			print(colored(str(i)+'-'+file_list[i]+' (dir)','blue',attrs=['bold']))
		else:
			print(colored(str(i)+'-'+file_list[i],'green',attrs=['bold']))

	while (1>0) or (os.path.isdir(chosen_file)):

		try:
			chosen_file = file_list[int(input(colored('Which one do you want to open? ','white',attrs=['bold'])))]
			if chosen_file == 'offset':
				raise IndexError
			elif (os.path.isdir(chosen_file)):
				chosen_file = get_files(chosen_file)
				break
			else:
				#files = open_file(chosen_file)
				return chosen_file
				break
		except IndexError:
	
			print(colored("Please, type in a whole number in the range 1-"+str(len(file_list)-1),'red',attrs=['bold']))
		except KeyboardInterrupt:
			sys.exit('Exitting...')

	#files = ''	 
	#while(os.path.isdir(chosen_file)):

	#	files = get_files(chosen_file)
	#	if (os.path.isdir(chosen_file)):
	#		try:

	#			chosen_file = open_file(files[int(input(colored('Which one do you want to open? ','white',attrs=['bold'])))-1])
	#		except IndexError:
	#			print(colored("Please, type in a whole number in the range 1-"+str(len(files)),'red',attrs=['bold']))
	#			continue
	#	else:	
	#		return chosen_file		
	#		break
	return chosen_file


	#return file_list

#Function to open a check if the selected file exits and/or if it is a directory
def open_file(file_path):

	try:

		if os.path.isdir(file_path):
			answer = input(colored('The selected option is a directory. Do you want to list its contents?(y/n) ','white',attrs=['bold']))
			if (answer == 'y'):
				
				return file_path
				
			else:
				sys.exit('Exitting...')
			
		else:
			return(file_path)
	except FileNotFoundError:
		sys.exit('File not found')

def main():

	#Prompting user for directory to list contents and file to open
	chosen_file = get_files(input(colored('\nType in dir path for listing files in it ','white',attrs=['bold'])))	
#	chosen_file = open_file(files[int(input(colored('Which one do you want to open? ','white',attrs=['bold'])))-1])
#	while(os.path.isdir(chosen_file)):

#		files = get_files(chosen_file)
#		if (os.path.isdir(chosen_file)):
#			try:

#				chosen_file = open_file(files[int(input(colored('Which one do you want to open? ','white',attrs=['bold'])))-1])
#			except:# IndexError:
#				print(colored("Please, type in a whole number in the range 1-"+str(len(files)),'red',attrs=['bold']))
#				continue
#		else:			
#			break"""

	#Prompting user for what kind of regression to perform
	x,y,regression_type = an.get_columns(chosen_file)
	#print(regression_type)

	if regression_type == 'logistic':
		an.logistic(x,y)
	else:
		an.linear(x,y)
"""	mod = ''
	print(colored("1 - Logistic\n2 - Linear",'green',attrs=['bold']))
	mod = int(input(colored("Which type of regression do you want to perform? ",'white',attrs=['bold'])))
	while (1>0):
		if (mod == 1):		
			an.logistic(chosen_file)
			break
		elif (mod == 2):
			an.linear(chosen_file)
			break
		else:
			print(colored("Invalid option. Please, select [1] for logistic regression or [2] for linear regression ",'red',attrs=['underline','bold']))
			mod = int(input(colored("Which type of regression do you want to perform? ",'cyan',attrs=['bold'])))"""
	
"""data = pd.read_csv('train.csv')
an.add_bias(data)
#print(data)

aa = data[['bias','Pclass','Sex','Age','Fare','Parch','SibSp']]
an.check_data(aa,'logistic')
#print(aa)
x=np.array(aa)
#print(x.shape)
y = np.array(data['Survived'])
theta = (np.ones(x.shape[1])).T
grad,theta = aux.grad_desc_log(x,y,theta,1,10,500)
#array for plotting sigmoid function to with the learned weights	
xp = np.linspace(min(x.dot(theta)),max(x.dot(theta)),len(y))
result = aux.sig(x.dot(theta))

	#setting threshold for success or failure
result[(result >= 0.5 )] = 1
result[(result < 0.5)] = 0
	#print(np.mean(result))
print("accuracy = ",np.mean(result == y))
		
	#plots for comparison	
plt.plot(xp,aux.sig(xp))	#sigmoid function
plt.plot(x.dot(theta),y,'ro')	#original data
plt.plot(x.dot(theta),result,'b+')#data using learned weights
plt.show()"""
if __name__ == '__main__':
	main()

