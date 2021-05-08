import searcher
import load
import indexer
import crawler
import interface

traverse = input("Would you like to crawl the data sources? (y/n): ")
if(traverse == "y"):
	
	'''load.get_traversal_data("unh_data.pickle")
	crawler.get_data("unh_data.pickle")  # appends data
	indexer.process_datafile("unh_data.pickle", "unh_sh")
	#searcher.search("unh_data.pickle")'''
interface.start_Search_Server()

