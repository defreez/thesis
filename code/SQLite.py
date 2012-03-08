#!/usr/bin/python

class Record:
	# Defines header type -> size relationship
	# From The SQLite rawDatabase File Format (section 2.1)
	SQLITE_TSZ  = { 0:0, 1:1, 2:2, 3:3, 4:4, 5:6, 7:8, 8:0, 9:0, 12:1, 13:1 }
	SQLITE_TYPE = { 'NULL'  : 0, 'INT8'  : 1, 'INT16' : 2, 'INT24' : 3,
			'INT32' : 4, 'INT48' : 5, 'INT64' : 6, 'FLOAT' : 7,
			'ZERO'  : 8, 'ONE'   : 9, 'TEXT'  : 12, 'BLOB' : 13 }

	def __init__(self, rawData, schema, sliceSz, searchField=0):
		self.schema = schema
		self.searchField = searchField
		self.sliceSz = sliceSz
		self.fieldSizes  = []
		self.fieldVals = []
		self.totalDataSize = 0
		self.valid = False
		self.szHdr = 0

		self.minHdrSz = 2
		for field in schema: self.minHdrSz += 1

		self.backStep(rawData)

		if self.valid:
			self.popVals()
		else:
			raise InvalidRecord()


	def backStep(self, rawData):
		bCurs = self.minHdrSz
		for f in range(0, len(self.schema)): self.fieldSizes.append(0)

		while bCurs < self.sliceSz and not self.valid:
			if self.validateHdr(rawData[self.sliceSz - bCurs : self.sliceSz], bCurs):
				self.tailingRec = rawData[self.sliceSz - bCurs:]
				self.valid = True
			bCurs += 1

	def validateHdr(self, rawSlice, bCurs):
		"""Attempts to validate whether or not this is a valid SQLite header + rawDataslice.
		rawData: slice from expected beginning of header (size) to search field (not include)
		bCurs: how many bytes we had to step back from search field to get here
		
		returns true if validates against schema, otherwise false
		"""

		blHdrSz    = False	# Header size validates
		blZeroByte = False	# Zero byte validates
		szHdr = self.minHdrSz

		if rawSlice[0] < self.minHdrSz:
			return False
			
		# Check mandatory zero byte after header size
		cursor = 1
		if rawSlice[cursor] == 0:
			blZeroByte = True
		cursor += 1

		for field in range(0, len(self.schema)):
			try: 
				if self.schema[field] >= 12:
					if rawSlice[cursor] > 127:
						self.fieldSizes[field] = Record.txtSize(Record.hufDecode(rawSlice[cursor:cursor+2]))
						cursor += 1
						szHdr += 1
					elif rawSlice[cursor] > 0:
						self.fieldSizes[field] = Record.txtSize(rawSlice[cursor])
					else:
						self.fieldSizes[field] = 0
				else:
					self.fieldSizes[field] = Record.SQLITE_TSZ[rawSlice[cursor]]
		
				cursor += 1
			except IndexError:
				raise InvalidRecord()
			except KeyError:
				pass
		
		skippedData = 0
		for field in range(0, self.searchField):
			skippedData += self.fieldSizes[field]
		if szHdr + skippedData == bCurs and self.szHdr == rawSlice[0]:
			blHdrSz = True

		self.szHdr = szHdr

		if blHdrSz and blZeroByte:
			for fs in self.fieldSizes:
				self.totalDataSize += fs

		return blHdrSz and blZeroByte

	def popVals(self):
		cursor = self.szHdr
		for f in self.fieldSizes:
			self.fieldVals.append(self.tailingRec[cursor : cursor + f])
			cursor += f 
	

	def hufDecode(twoBytes):
		"""Huffman decode two bytes.
		Someday this should do two or three bytes"""
		return (twoBytes[0] - 128) * 128 + twoBytes[1]

	def txtSize(rawSize):
		"""Convert a raw size for a SQLite text field into number of bytes"""
		return (rawSize - 13) // 2

class InvalidRecord(Exception):
	pass
