# import sys for get to command line arguments
import sys
# import os, to find file/directory exists
import os

#get the file path from the arguments
file_path = sys.argv[1]

while True:
	#check if file exits
	file_exists = os.path.exists(file_path)
    # if file does not exist
	if file_exists == False:
		print('Alert')
	print(file_exists)

	
	

