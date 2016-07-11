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
	#This should return a located page url but currently returns the search url
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
