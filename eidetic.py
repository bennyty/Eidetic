# Sample command
# eidetic vid/wiki saveFilename searchName

import sys
import re
import socket
from urllib.parse import urlparse 
from requests import get

def parseInfoFile(infoFilename):
	with open(infoFilename, 'r') as openedInfoFile:
		lines = list(openedInfoFile)
		#returns baseUrl,  searchUrl, whitespace-seperator, finalRegex, rest of the nested regexes
		return lines[0], lines[1], lines[2], lines[3], lines[4:]


def searchSite(baseUrl, searchUrl, whiteSpaceSeperator, finalRegex, regexs, searchTerm):
	concatURL = (baseUrl + searchUrl + (''.join(str(n) for n in searchTerm)).replace(" ", whiteSpaceSeperator)).replace("\r", "").replace("\n", "")
	html = getHTMLFromURL(concatURL).text
	
	return concatURL

def getUrlData(url, filename, bufferSize = 4096):
	"""
	filename needs to include the extension of the streamed file
	"""
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	parsedUrl = urlparse(url)
	sock.connect(parsedUrl.netloc, 80)

	request = 'GET %s HTTP/1.0\n\n' % parsedUrl.path
	sock.sendall(bytes(request, 'ascii'))

	dataFile = open(filename, 'wb')
	data = sock.recv(bufferSize)
	while data:
		dataFile.write(data)
	dataFile.close()
	sock.close()

	return dataFile

def userInteractionLayer(data):
	print("We found these results:")
	arrs = []
	for x in range(0, len(data)):
		element = list(data[x])
		element.insert(0, str(x+1))
		arrs.append(element)
	col_width = max(len(word) for row in data for word in row) + 2
	for row in arrs:
		print("".join(word.ljust(col_width) for word in row))

	userInput = input("Please select the number in left column that best matches your item: ")
	return userInput


def getHTMLFromURL(url):
	return get(url)

def searchStringForRegex(html, regex):
	"""
	Return a tuple of all **capture groups**
	>>> searchHTMLForRegex("Hello this is all", '\w*ll\w*')
	['Hello', 'all']
	"""
	match = re.findall(regex, html)
	return match

def printUsageInstructions():
	print("""\
Usage:
	eidetic vid/wiki saveFilename searchName
""")

class downloadThread(threading.Thread):
 	def __init__(url, filename, bufferSize = 4096):
 		self.url = url
 		self.filename = filename
 		self.bufferSize = bufferSize

 	def run():
		sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		parsedUrl = urlparse(self.url)
		sock.connect(parsedUrl.netloc, 80)

		request = 'GET %s HTTP/1.0\n\n' % parsedUrl.path
		sock.sendall(bytes(request, 'ascii'))

		dataFile = open(self.filename, 'wb')
		data = sock.recv(self.bufferSize)
		while data:
			dataFile.write(data)
		dataFile.close()
		sock.close()

def main(args):
	if len(args) != 3:
		printUsageInstructions()
		sys.exit()
	baseUrl, searchUrl, whiteSpaceSeperator, finalRegex, regexs = parseInfoFile(args[0])
	pageUrl = searchSite(baseUrl, searchUrl, whiteSpaceSeperator, finalRegex, regexs, args[2:])
	getMediaFromPage(pageUrl, args[1])
	# print(searchStringForRegex(html, searchExpresssion))
	# print(searchStringForRegex(testString, searchExpresssion))

if __name__ == "__main__":
	main(sys.argv[1:])
