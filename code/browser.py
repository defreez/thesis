#!/usr/bin/python

# todo: support huffman types greater than two bytes
#       modify Record class so that it can be subclassed for different types of records
# 	fields: description, bookmark, favicon, thumbnail, touch_icon, user_entered

import time
import argparse
from SQLite import Record, InvalidRecord

class BrowserRecord(Record):
	def __init__(self, rawData):
		schema = [Record.SQLITE_TYPE["TEXT"],	# title
			  Record.SQLITE_TYPE["TEXT"],	# url
			  Record.SQLITE_TYPE["INT8"],	# visits
			  Record.SQLITE_TYPE["INT48"], 	# date
			  Record.SQLITE_TYPE["INT48"],  # created
			  Record.SQLITE_TYPE["TEXT"],	# description
			  Record.SQLITE_TYPE["INT8"],   # bookmark
			  Record.SQLITE_TYPE["BLOB"],   # favicon
			  Record.SQLITE_TYPE["BLOB"],   # thumbnail
			  Record.SQLITE_TYPE["BLOB"],   # touch_icon
			  Record.SQLITE_TYPE["INT8"] ]  # user_entered

		Record.__init__(self, rawData, schema, sliceSz=(len(rawData)//2), searchField=1)
		self.interpret()

	def interpret(self):
		
		self.title   = str(self.fieldVals[0], encoding='utf-8')
		self.url     = str(self.fieldVals[1], encoding='utf-8')
		self.visits  = self.fieldVals[2][0]
	
		timeInt = BrowserRecord.bytesToInt(self.fieldVals[3])
		timeInt = int(str(timeInt)[:10])
		if timeInt > 0:
			self.date = time.ctime(timeInt)
		else:
			self.date = 'Unknown'

		self.created      = self.fieldVals[4][0]
		self.description  = str(self.fieldVals[5], encoding='utf-8')

		if self.fieldVals[6][0] == 1:
			self.bookmark = True
		else:
			self.bookmark = False

		self.favicon      = self.fieldVals[7]
		self.thumbnail    = self.fieldVals[8]
		self.touch_icon   = self.fieldVals[9]
		
		if len(self.fieldVals[10]) == 1 and self.fieldVals[10][0] == 1:
			self.user_entered = True
		else:
			self.user_entered = False
		

	def bytesToInt(bStr):
		"""Transforms a binary string into an integer.
		This is a really ugly hack, but I don't know of a better way"""	
	                                                                        
		strHex = '0x'                                                   
		for b in range(0, len(bStr)):                                   
			strHex += hex(bStr[b])[2:4]                             
		return int(strHex, 16)                                          

	def __str__(self):
		strTitle 	= "Title: %s\n"	% self.title 
		strUrl		= "URL: %s\n" % self.url 
		strVisits	= "Visits: %d\n" % self.visits
		strDate 	= "Date: %s\n"	% self.date 
		strCreated	= "Created: %d\n" % self.created
		strDesc		= "Description: %s\n" % self.description
		strBookmark     = "Bookmark: %s\n" % self.bookmark
		strUserEntered	= "User_Entered: %s\n" % self.user_entered
		strDivider	= "---------------------------\n"

		return 	strTitle + strUrl + strVisits +  strDate + strCreated + strDesc + strBookmark + strUserEntered + strDivider

###### MAIN ######

def doIt(imgPath): 
		f = open(imgPath, 'rb')
		image = f.read()
		f.close()

		# Find all http locations
		records = []
		found = 0
		while found != -1:
			found = image.find(b'http://', found + 1)
			if found != -1:	
				try:
					r = BrowserRecord(image[found - 128 : found + 128])
					records.append(r)
				except InvalidRecord:
					pass

		for r in records:
			if(r.user_entered):
				print(r)

parser = argparse.ArgumentParser(description='Extract browser history from and Anroid NAND Dump')
parser.add_argument('path', type=str, help='the full path to the NAND dump')
args = parser.parse_args()

doIt(args.path)
