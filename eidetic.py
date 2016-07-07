# sample commande
# eidetic /vid/wiki saveFilename searchName

import sys
def parseInfoFile(infoFilename):
	openedInfoFile = open("infoFilename")
	#This should return baseUrl, searchUrl, and regEx

def searchSite(baseUrl, searchUrl, regEx, searchTerm):
	#This should return a located page url

def getMediaFromPage(pageUrl, saveName):
	# This function figures out media url then calls wget
	# wget mediaUrl -O filename

def main(args):
	baseUrl, searchUrl, regEx = parseInfoFile(args[0])
	pageUrl = searchSite(baseUrl, searchUrl, regEx, args[2:])
	getMediaFromPage(pageUrl, args[1])

if __name__ == "__main__"
	main(sys.argv[1:])
