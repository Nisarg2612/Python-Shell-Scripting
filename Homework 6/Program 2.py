import json
import os
import shutil


PARENT_DIR = "quotes_output"

with open("quotes.json", 'r') as quotes_file:
	data = json.load(quotes_file)

#if the parent directory already there, we will delete it
if os.path.exists(PARENT_DIR):
	shutil.rmtree(PARENT_DIR)  # os.rmdir(PARENT_DIR)

os.mkdir(PARENT_DIR)  # parent directory
# change directory so that we are inside the parent directory
os.chdir(PARENT_DIR)
print("Created parent directory ", PARENT_DIR)

for node in data:
	corrected_author = node["author"] if node["author"] is not None else "Unknown"
	dir_name = corrected_author.replace(" ", "_")
	os.mkdir(dir_name) if not os.path.exists(dir_name) else print("{} already exists".format(dir_name))
	os.chdir(dir_name)  # go inside the newly created directory
	quote_number = 1
	file_name = "quote_"+str(quote_number)+".txt"
	out = open(file_name, "a")
	out.write(node["text"])
	out.close()
	quote_number += 1
	os.chdir("..")  # go one level up in the directory tree

