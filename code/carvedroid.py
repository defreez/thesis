#!/usr/bin/python

#yaffs_packedtags2.h yaffs_packedtags2tagspart

import sys
import os.path
from hachoir_core.field import Parser, FieldSet, RawBytes, UInt8, UInt32, UInt16
from hachoir_core.stream import StringInputStream, LITTLE_ENDIAN

IMAGEPATH = '/home/lacie/Dropbox/thesis/data/nandsim2.img'
PAGESIZE = 2048
OOBSIZE  = 64
#OOBFREEOFFSET = 30	# This assumes a contiguous oobfree area, 
#OOBFREESIZE = 16	# which is not necessarily the case
OOBFREEOFFSET = 2
OOBFREESIZE = 38

# Hachoir Chunk parser, all of the classes that start with 'H' are splitting bits w/ Hachoir
class HChunk(Parser):
	endian = LITTLE_ENDIAN
	def createFields(self):
		yield RawBytes(self, "data", PAGESIZE)
		yield HOob(self, "oob", OOBSIZE)

class HOob(Parser):
	endian = LITTLE_ENDIAN
	def createFields(self):	
		yield RawBytes(self, "mtdfront", OOBFREEOFFSET)
		yield RawBytes(self, "tags", OOBFREESIZE)
		yield RawBytes(self, "mtdback", OOBSIZE - (OOBFREESIZE + OOBFREEOFFSET)) 

# These tags are reinterpreted if this chunk (block?) contains an object header
class HTags(FieldSet):
	def createFields(self):
		yield UInt32(self, "blockSeq", "sequence number for this block")
		yield UInt32(self, "objectId", "Object ID")
		yield UInt32(self, "chunkId", "Chunk ID")
		yield UInt32(self, "nBytes", "Number of data bytes in this chunk")

class Chunk:
	blockSeq = 0xffffffff
	objectId = 0
	chunkId = 0
	nBytes = 0

###### BEGIN ######

image = []	# Central chunk list

imgSize = os.path.getsize(IMAGEPATH)
imgStream = open(IMAGEPATH, 'r')

# While there is enough room in the file for a full chunk, parse w/ hachoir
while ( (imgSize - imgStream.tell()) >= (PAGESIZE + OOBSIZE) ):
	chunk = Chunk()
	strmChunk = StringInputStream( imgStream.read(OOBSIZE) )
	hChunk = HOob(strmChunk)
	print hChunk["tags"]
	#chunk.blockSeq = hChunk["tags"]["blockSeq"]
	#chunk.objectId = hChunk["tags"]["objectId"]
	#chunk.chunkId  = hChunk["tags"]["chunkId"]
	#chunk.nBytes   = hChunk["tags"]["nBytes"]
	image.append(chunk)
	imgStream.seek(imgStream.tell() + PAGESIZE)

if (imgStream.tell() != imgSize):
	print >> sys.stderr, "WARNING: Image not correct size for chosen PAGESIZE + OOBSIZE, ended on %d of %d" % (imgStream.tell(), imgSize)

imgStream.close()
