import urllib.request
from urllib.error import URLError
import re
import os
import pickle


def visit_url(url, domain):
	global crawler_backlog
	global url_list

	if(len(crawler_backlog) > 30):
		return

	if(url in crawler_backlog and crawler_backlog[url] == 1):
		return
	else:
		crawler_backlog[url] = 1
		print("Processing:", url)
	try:
		page = urllib.request.urlopen(url)
		code = page.getcode()
		if(code == 200):
			content = page.read()
			content_string = content.decode("utf-8", "ignore")
			regexp_title = re.compile('<title>(?P<title>(.*))</title>')
			regexp_body = re.compile('<body[^>]*>(?P<body>([\s\S]*))<\/body>')
			#regexp_keywords = re.compile('<meta name="keywords" content="(?P<keywords>(.*))" />')
			regexp_url = re.compile("https?://\w*"+domain+"[/\w+]*")

			# remove extra spaces from crawled content
			regexp_space = re.compile('\s{2,}')
			# remove java script from crawled content
			regexp_js = re.compile('<script([^\'"]|"[^"]*"|\'[^\']*\')*?</script>')
			# remove the tags < > and &amp; &nbsp; html encoding
			regexp_text = re.compile('(<.*?>\\s*)+|&[#A-z0-9]+;')
			# remove unnecessary character from the crawled content
			regexp_junk = re.compile("{[A-z0-9'\\;:,\s-]+}{1,2}|{}|(\\[A-z0-9]+\\[A-z0-9]+)/g")
			
	
			result = regexp_title.search(content_string, re.IGNORECASE)

			if result:
				title = result.group("title")
				print("\n", title)

			# get text with the body tag
			result = regexp_body.search(content_string, re.IGNORECASE)

			if result:
				result = result.group("body")
				result = regexp_space.sub(" ", result)
				result = regexp_js.sub(" ", result)
				result = regexp_text.sub(" ", result)
				result = regexp_junk.sub(" ", result)

				if result:
					url_list.append((url, result))
					print("\n", result)

			for (urls) in re.findall(regexp_url, content_string):
				if(urls not in crawler_backlog or crawler_backlog[urls] != 1):
					crawler_backlog[urls] = 0
					visit_url(urls, domain)

		return url_list
	except URLError as e:
		print("error")


url_list = []
crawler_backlog = {}

seed = "http://www.newhaven.edu/"

crawler_backlog[seed] = 0

#visit_url(seed, "\.newhaven\.edu")


def get_data(filename):

	# get the data from seed website
	visit_url(seed, "\.newhaven\.edu")

	#read pickled data
	print("Reading pickle Data from: " + filename)
	pickle_file = open(os.path.join(os.getcwd(), filename), "br")
	file_list = pickle.load(pickle_file)
	pickle_file.close()

	file_list.extend(url_list)

	# pickle it
	print("Storing File Data to: " + filename)
	pickle_file = open(os.path.join(os.getcwd(), filename), "bw")
	pickle.dump(file_list, pickle_file)
	pickle_file.close()

