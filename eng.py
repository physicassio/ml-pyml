import pandas as pd
import numpy as np
from termcolor import colored


def main(ob_data,tar):

	columns = ob_data.columns
	ob_chosen_columns = []
	
	print(colored('Choose the columns to perform feature engineering on','blue',attrs=['bold']))
	for i in range(len(columns)):
		
		#+1 so user does not need to type in 0
			print(colored(str(i+1)+'-'+columns[i]+' '+str(ob_data[columns[i]].dtypes),'yellow',attrs=['bold']))
	
	while (1>0):
		inp = input(colored('Choose one column and press Enter or type in \'0\' to finish selecting. (Type in \'a\' to choose all columns at once) ','white',attrs=['bold']))	

			
		if (inp == 'a'):
			
			ob_chosen_columns = list(columns)
			break
			

		elif (int(inp) == 0):
			break
			
		elif (int(inp) in range(1,len(columns)+1)):
		
			#data[columns[int(inp)-1]]
			ob_chosen_columns.append(columns[int(inp)-1])
		
		else:
		
			print(colored('Invalid column. Please, select a valid column name ','red',attrs=['bold']))
	encoded_cols = encode(ob_data[ob_chosen_columns],tar)
	
	#print(encoded_cols.drop('target',1))
	return(encoded_cols.drop('target',1))
			

def encode(cols,tar):
	cols.insert(cols.shape[1],'target',tar)
	#print(cols)
	for column in cols.columns.drop('target'):
	
		opt_enc = int(input(colored('Which type of encoding do you want to apply for column \'%s\'\n1-Target Encoding\n2-Count Encoding\n'%(column),'blue',attrs=['bold'])))
		
		if (opt_enc == 1):
			new_col = target_encoding(cols[[column,'target']])
			#print(ob_data.columns.get_loc(column))
			cols[column] = new_col
			
		elif (opt_enc == 2):
			new_col = count_encoding(cols[[column]])
			cols[column] = new_col
	#print(cols)
	return(cols)#.drop())
def target_encoding(col):

	col_name = col.columns[0]
	c = col[col_name]
	idx = col.groupby(col_name).count().index
	for i in idx:

		mean = col['target'][c==i].mean()
		col.replace(i,mean,inplace=True)
		
	#print(col)
	return(col.drop('target',1))

def count_encoding(col):

	col_name = col.columns[0]
	c = col[col_name]
	idx = col.groupby(col_name).count().index
	for i in idx:

		qtd = len(col[c==i])#.count()
		col.replace(i,qtd,inplace=True)
		
	#print(col.index)
	return(col)	

if __name__ == '__main__':
	main([0])
