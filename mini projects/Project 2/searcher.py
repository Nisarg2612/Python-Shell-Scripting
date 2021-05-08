from datetime import datetime
import shelve
import os
import pickle

def search(query):

	print("Reading shelved data...")
	sh = shelve.open("unh_sh")
	dic = sh["dic"]
	sh.close()

	#query=input("\nSearch Query: ")
	query = query.strip().lower() # normalize, remove spacing, go to lower case
	tokens = query.split(" "); # parse into tokens by spaces
	results = []

	#find operator
	if "or" in tokens:
		if "and" in tokens:
			operator = "AND" #if user enters both 'and' and 'or', then 'and'
		else:
			operator = "OR"
	else:
		operator = "AND"

	#remove operator from tokens
	while("and" in tokens):
		tokens.remove("and")
	while("or" in tokens): 
		tokens.remove("or")

	#remove duplicates using a set
	unique_tokens = set()
	for x in tokens:
		unique_tokens.add(x)

	print("Performing: " + operator + " search for: " + str(unique_tokens) + "\n")

	start_tm = datetime.now()
	if(operator == "OR"):
		bigset = set()
		biglist = []
		for x in unique_tokens:
			if dic.get(x) != None:
				bigset = set(bigset).union(set(dic[x])) #adding all the sets up to get a unique list of line numbers
		biglist = list(bigset)
		biglist.sort()
		results = biglist
	else:
		andlist = []
		for x in unique_tokens:
			if dic.get(x) != None:
				newlist = []
				smlist = []
				if(len(andlist) == 0):
					andlist = list(dic[x]) #initialize the set from the first find.
				else:
					smlist = list(dic[x])
					#keep removing from the first found set.
					for j in smlist:
						if j in andlist:
							newlist.append(j)
					andlist = newlist
		andlist.sort()

		results = andlist

					

		
	#read pickled data
	p = open(os.path.join(os.getcwd(), "unh_data.pickle"), "br")
	file_list = pickle.load(p)
	p.close()
	
	
	for i, x in enumerate(results):
		print("Result " + str(i + 1) + ": " + x)
		
		#print the first 100 characters from the original text
		for i in range(len(file_list)):
			if(file_list[i][0] == x):
				print("\t  Text Found: " + str(file_list[i][1])[:100] + "...") 
				break
		
	end_tm = datetime.now()
	print("\nExecution Time: " + str(end_tm.microsecond // 1000 - start_tm.microsecond //1000) + " seconds")

	return results
