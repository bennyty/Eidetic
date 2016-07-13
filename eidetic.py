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


def searchSite(baseUrl, searchUrl, whiteSpaceSeperator, finalRegex, regexes, searchTerm):
	concatURL = (baseUrl + searchUrl + (''.join(str(n) for n in searchTerm)).replace(" ", whiteSpaceSeperator)).replace("\r", "").replace("\n", "")
	html = getHTMLFromURL(concatURL).text

	currentRegex = 0
	# Loop until the finalRegex does match
	while len( searchStringForRegex(html, finalRegex, False) ) == 0:
		print("Did not match final regex\n\tnow matching " + regexes[currentRegex % len(regexes)])
		capturesInOrder = searchStringForRegex(html, regexes[currentRegex % len(regexes)], True)
		userChoice = userInteractionLayer(capturesInOrder[:10])
		url = capturesInOrder[int(userChoice)][0] # Get the url from first element
		html = getHTMLFromURL(concatURL).text
		currentRegex += 1
	

	#This returns a located page url
	return searchStringForRegex(html, finalRegex, False)

def userInteractionLayer(data):
	print("We found these results:")
	print(data)
	arrs = []
	for x in range(0, len(data)):
		element = list(data[x])
		element.insert(0, str(x+1))
		arrs.append(element)
	# col_width = max(len(word) for row in data for word in row) + 2
	print(arrs)
	col_width = max(len(word) for row in arrs for word in row) + 2
	for row in arrs:
		print("".join(word.ljust(col_width) for word in row))

	userInput = input("Please select the number in left column that best matches your item: ")
	return userInput


def getHTMLFromURL(url):
	return get(url)

def searchStringForRegex(html, regex, useIter):
	"""
	Return a tuple of all **capture groups**
	>>> searchStringForRegex("Hello this is all", '\w*ll\w*')
	['Hello', 'all']
	"""
	if useIter:
		itr = re.finditer(regex, html)
		arr = []
		for match in itr:
			element = []
			element.append(match.group('url'))
			element.append(match.group('name'))
			arr.append(element)
		return arr
	else:
		return re.findall(regex, html)

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
