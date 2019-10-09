import numpy as np
import sys
import os

def clean_file(lines,in_file):
		new_file_name = 'clean_'+in_file
		new_file = open(new_file_name,'wb')
		for line in lines:
			try:
				line.decode('utf-8')
				new_file.write(line)
			except UnicodeDecodeError:
				i = 0
				l = []
				while (i<len(line)):		
					
					try:
						l.append(line[i])
						i+=1
					except UnicodeDecodeError:
						i+=2
					print(i)
				#print(line)
				new_file.write(bytearray(l))
				#new_file.write(''.join([chr(x) for x in l]))
				#print(''.join([chr(x) for x in l]))
		new_file.close()
				#print(''.join([chr(x) for x in l]))
				#print(line)
		print('Data cleaned successfuly. File '+new_file_name+' has been written')
def check_file(in_file):

		a = open(in_file,'rb')
		#lines = a.readlines()
		#a.close()
		#for line in lines:
		while True:	
			try:
				a.read().decode('utf-8')
			except UnicodeDecodeError:
				
				decision = input('File '+in_file+' contains malformed characters. Do you want to remove them?(y/n) ')
				while (1>0):
			
					if (decision == 'y'):
						#print(a.readli)
						clean_file(open(in_file,'rb').readlines(),in_file)
						break
					elif (decision == 'n'):
						break
					else:
						decision = input("Invalid option. Please type in 'y' or 'n' ")
				break
			#break
			

def write_bin_file(fil,content):
	
	#try:
		#text_content = ''.join([chr(x) for x in content])
		#ontent = np.array(content)	
		file_size = os.path.getsize(fil)
		buff = open(fil,'r')
		
			
		
		#for char in content:
		#	if chr(char).decode('utf-8'):
		#		continue
		#	else:
		#		print(char)
		new_bin_file = open('clean_'+str(fil),'wb').write(bytearray(content))
	#except:
	#	sys.exit('Crap')
		
def main(in_file):
	check_file(in_file)

if __name__ == '__main__':
	main(input('Type in the file name to check '))
#in_file(input('Type in the file name to check '))
#print(content[content > 130])
#print(chr(0xa0))#.encode('utf-8'))

