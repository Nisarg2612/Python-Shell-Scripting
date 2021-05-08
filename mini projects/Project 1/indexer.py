from datetime import datetime
import pickle
import shelve

# Creates dictionary off of pickled file.
def process_datafile(file_name, sh_name):
	print("\nPre-Processing...")
	start_tm = datetime.now()
	#dictionary list of words
	#each word has a set of line numbers
	
	f = open(file_name, "br")
	# load data from the pickle file
	data_list = pickle.load(f)
	# file close 
	f.close()
	
	# create dictionary
	dic = {}
	for i in range(0, len(data_list)):
		t = data_list[i]
		path = str(t[0])
		words = str(t[1]).split(" ")
		for word in words:
			word = word.replace(".", "").replace(",", "").lower()
			if dic.get(word) == None:
				dic[word] = set() #add word to dictionary and create a set
				dic[word].add(t[0]) #add the line number to the set
			else:
				dic[word].add(t[0]) #add line number to the existing set
	end_tm = datetime.now()
	print("Execution Time: " + str(end_tm.microsecond // 1000 - start_tm.microsecond //1000) + " seconds")
	
	#store dictionary in database file
	print("Shelving pre-processed data...")
	sh = shelve.open(sh_name)
	sh["dic"] = dic
	sh.close()
	
	return dic