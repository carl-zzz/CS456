#packet.py
#All kinds of needed pkt structure

NBR_ROUTER = 5

class pkt_HELLO:
	def __init__( self, RouterId, LinkId ):
		self.routerId = RouterId
		self.linkId = LinkId

	def getRouterId( self ):
		return self.routerId

	def getLinkId( self ):
		return self.linkId

	def getUDPdata( self ):
		bufferArr = bytearray()
		temp = (self.routerId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.linkId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		return bufferArr
	
	def parseUDPdata( self, bufferArr ):
		self.routerId = int.from_bytes(bufferArr[0:4], byteorder='little')
		self.linkId = int.from_bytes(bufferArr[4:8], byteorder='little')

#this class stores link state database
class LSPDU:
	def __init__( self, Sender, RouterId, LinkId, Cost):
		self.sender = Sender
		self.routerId = RouterId
		self.linkId = LinkId
		self.cost = Cost

	def getSender( self ):
		return self.sender
	def getRouterId( self ):
		return self.routerId
	def getLinkId( self ):
		return self.linkId
	def getCost( self ):
		return self.cost

#this class stores sent LSPDU pkt 
class sent_LSPDU:
	def __init__( self, RouterId, LinkId, Cost):
		self.routerId = RouterId
		self.linkId = LinkId
		self.cost = Cost
	
	def getCost( self ):
		return self.cost
	def getRouterId( self ):
		return self.routerId
	def getLinkId( self ):
		return self.linkId

class pkt_LSPDU:
	def __init__( self, Sender, RouterId, LinkId, Cost, Via):
		self.sender = Sender
		self.routerId = RouterId
		self.linkId = LinkId
		self.cost = Cost
		self.via = Via

	def getSender( self ):
		return self.sender
	def getRouterId( self ):
		return self.routerId
	def getLinkId( self ):
		return self.linkId
	def getCost( self ):
		return self.cost
	def getVia( self ):
		return self.via

	def getUDPdata( self ):
		bufferArr = bytearray()
		temp = (self.sender).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.routerId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.linkId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.cost).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.via).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		return bufferArr

	def parseUDPdata( self, bufferArr):
		self.sender = int.from_bytes(bufferArr[0:4], byteorder='little')
		self.routerId = int.from_bytes(bufferArr[4:8], byteorder='little')
		self.linkId = int.from_bytes(bufferArr[8:12], byteorder='little')
		self.cost = int.from_bytes(bufferArr[12:16], byteorder='little')
		self.via = int.from_bytes(bufferArr[16:20], byteorder='little')



class pkt_INIT:
	def __init__( self, RouterId ):
		self.routerId = RouterId

	def getRouterId( self ):
		return self.routerId

	def getUDPdata( self ):
		bufferArr = bytearray()
		temp = (self.routerId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		return bufferArr


class link_cost:
	def __init__( self, LinkId, Cost):
		self.linkId = LinkId
		self.cost = Cost
	
	def getLinkId( self ):
		return self.linkId
	def getCost( self ):
		return self.cost

	def getUDPdata( self ):
		bufferArr = bytearray()
		temp = (self.linkId).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		temp = (self.cost).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		return bufferArr

	def parseUDPdata( self, bufferArr ):
		self.linkId = int.from_bytes(bufferArr[0:4], byteorder='little')
		self.cost = int.from_bytes(bufferArr[0:4], byteorder='little')
		

class circuit_DB:
	def __init__( self, NbrLink ):
		self.nbrLink = NbrLink
		self.linkCost = []

	def getNbrLink( self ):
		return self.nbrLink
	def addToLinkCost( self, linkcost ):
		self.linkCost.append(linkcost)
	def getLinkCost( self ):
		return self.linkCost

	def getUDPdata( self ):
		bufferArr = bytearray()
		temp = (self.nbrLink).to_bytes(length=4,byteorder='little')
		bufferArr.extend(temp)
		i = 0
		while i < ((self.nbrLink)-1):
			temp = (self.linkCost)[i].getUDPdata()
			bufferArr.extend(temp)
			i = i + 1
		return bufferArr

	def parseUDPdata( self, bufferArr ):
		self.nbrLink = int.from_bytes(bufferArr[0:4], byteorder='little')
		self.linkCost = []
		i = 0
		base = 4
		while i < self.nbrLink:
			linkcost = link_cost(0,0)
			linkcost.parseUDPdata(bufferArr[base:base+8])
			self.linkCost.append(linkcost)
			i = i + 1
			base = base + 8
		

		
