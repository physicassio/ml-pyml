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
import json

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
				return chosen_file
				break
		except IndexError:
	
			print(colored("Please, type in a whole number in the range 1-"+str(len(file_list)-1),'red',attrs=['bold']))
		except KeyboardInterrupt:
			sys.exit('Exitting...')

	return chosen_file

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

	#Prompting user for what kind of regression to perform
	x,y,regression_type,cols,target = an.get_columns(chosen_file)

	result_files = chosen_file.rstrip('.csv') + '_results'
	
	if (regression_type == 'logistic'):
	
		theta,accuracy = an.logistic(x,y)

		#checking for past results and exporting the current ones if the accuracy is greater than the past one
		#in case the past accuracy is better than current one, current results are dismissed
		past_accu = aux.check_past_result(result_files+'.json')
		if (accuracy > past_accu):
			output_dict = {'theta':theta,'columns':cols,'accuracy':accuracy}
			aux.export_json(result_files+'.json',output_dict)
		
		else:
			print(colored('Your previous result had %.3f accuracy and the current %.3f. Current one will not be saved'%(past_accu,accuracy),'yellow',attrs=['bold']))
			
	else:
		theta = an.linear(x,y,cols)
		output_dict = {'theta':theta,'columns':cols}
		aux.export_json(result_files+'.json',output_dict)
		
	test_hip = input(colored('Do you want to apply your model to a different dataset? ','green',attrs=['bold']))
	
	if (test_hip == 'y'):
		
		test_file = get_files(os.path.dirname(chosen_file))
		test_data = pd.read_csv(test_file)[cols[1:]]
		an.add_bias(test_data)
		an.check_data(test_data,regression_type)
		
		if (regression_type == 'logistic'):
			res = aux.sig(np.dot(test_data,theta))
			res[res > 0.5 ] = 1
			res[res <= 0.5] = 0
		else:
			res = np.dot(x,theta)
		res_file = open(result_files+'_log_reg.csv','w')
		res_file.write(target+'\n')
		res_file.write('\n'.join([str(x) for x in res]))
		res_file.close()

		
		

if __name__ == '__main__':
	main()

