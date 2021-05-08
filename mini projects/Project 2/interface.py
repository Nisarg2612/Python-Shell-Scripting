from wsgiref.simple_server import make_server
import html
import os
import searcher
import load
import crawler
import pickle
import threading

#server base class
class Server:
	#initialize class with port
	@classmethod
	def __init__(self, port):
		self.port = port
		self.httpd = None

	# Starts the web server
	@classmethod
	def start_server(self):
		self.httpd = make_server('', self.port, self.server_engine)
		print("Serving on port " + str(self.port) + "...")
		self.httpd.serve_forever()

	#the server engine to override
	@classmethod
	def server_engine(self, environ, start_res):
		message = ""
		status = '200 OK'
		headers = [('Content-type', 'html; charset=utf-8')]
		start_res(status, headers)

		message += '<!DOCTYPE html><html><body>'
		message += 'Server is running.'
		message += '</body></html>'

		return[bytes(message, 'utf-8')]

	#parse get forms
	@staticmethod
	def get_form_vals(get_str):
		form_vals = {item.split("=")[0]: item.split("=")[1]
            for item in get_str.split("&")}
		return form_vals

	#parse post forms
	@staticmethod
	def post_form_vals(post_str):
		form_vals = {item.split("=")[0]: item.split("=")[1]
        	for item in post_str.decode().split("&")}
		return form_vals


class SearchEngine(Server):
	@classmethod
	def server_engine(self, environ, start_res):
		#print("ENVIRON:", environ)
		message = ""
		status = '200 OK'
		headers = [('Content-type', 'html; charset=utf-8')]
		start_res(status, headers)

		message += '<!DOCTYPE html>'
		message += '<html>'
		message += '<body>'
		message += '<center>'
		message += "<h1>"
		message += '<font color="#000080">Search</font>'
		message += "</h1>"
		message += '<form action="search" method="GET">'
		message += '<input type="text" name="query">'
		message += '<input type="submit" value="Search">'
		message += '</form>'
		message += '</center>'
		message += '</br>'
		message += '</br>'

		if(len(environ['QUERY_STRING']) > 1):
			form_vals = Server.get_form_vals(environ['QUERY_STRING'])
			query = form_vals["query"]
			query = html.unescape(query)  # convert %20,+, etc back to spaces
			query = query.replace("+", " ")  # convert %20,+, etc back to spaces

			results = searcher.search(query)

			

			for i, link in enumerate(results):

				p = open(os.path.join(os.getcwd(), "unh_data.pickle"), "br")
				file_list = pickle.load(p)
				p.close()

				print("Result " + str(i + 1) + ": " + link)
				message += '<a href="' + link + '">' + link + '</a></br>'

				#print the first 100 characters from the original text
				for i in range(len(file_list)):
					if(file_list[i][0] == link):
						print("\t  Text Found: " + str(file_list[i][1])[:100] + "...")
						
				message += '</br>'
				message += '</br>'

		message += '</body>'
		message += '</html>'

		return[bytes(message, 'utf-8')]


#url = "ws://localhost:8765"

def start_Search_Server():
	x = SearchEngine(8765)
	x.start_server()


t2 = threading.Thread(target=start_Search_Server)
t2.start()