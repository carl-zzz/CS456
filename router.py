#!/usr/bin/python
#Python program for router
from socket import *
from packet import *
import sys

#bad input detection
if len(sys.argv) == 5:
	routerId = int(sys.argv[1])
	nseHost = sys.argv[2]
	nsePort = int(sys.argv[3])
	routerPort = int(sys.argv[4])
else:
	print("Incorrect # of inputs.")
	sys.exit()

#create log
routerName = str('router' + str(routerId) + '.log')
routerLog = open(routerName,'w')

routerSocket = socket(AF_INET,SOCK_DGRAM)
routerSocket.bind(('',routerPort))

#send INIT pkt to nse
pkt_Init = pkt_INIT(routerId)
bufferArr = pkt_Init.getUDPdata()
routerSocket.sendto(bufferArr,(nseHost,nsePort))
routerLog.write('R'+str(routerId)+' sends an INIT: router_id '+str(routerId))
routerLog.write('\n')

#receive circuitDB from nse
bufferReceived = routerSocket.recvfrom(1024)[0]
#print("length of circuitDB buffer: ",len(bufferReceived))
circuitDB = circuit_DB(0)
circuitDB.parseUDPdata(bufferReceived)
routerLog.write('R'+str(routerId)+' received a CIRCUIT_DB: nbr_link '+str(circuitDB.getNbrLink()))
routerLog.write('\n')

#build link state database with circuit database received
LSDB = []
#dupLSDB = []
sentLspdu = []
discoveredNeighbors = []
discoveredR = []
discoveredR.append(routerId)
nbrLink = circuitDB.getNbrLink()
linkCosts = circuitDB.getLinkCost()
#lspdu_nbrlink = LSPDU_NBRLINK(routerId,routerId,nbrLink)
#LSDB.append(lspdu_nbrlink)
i = 0
while i < nbrLink:
	lspdu = LSPDU(routerId,routerId,linkCosts[i].getLinkId(),linkCosts[i].getCost())
	#save_Lspdu = sent_LSPDU(lspdu.getRouterId(),lspdu.getLinkId(),lspdu.getCost())
	#dupLSDB.append(save_Lspdu)
	LSDB.append(lspdu)
	pkt_Hello = pkt_HELLO(routerId,linkCosts[i].getLinkId())
	bufferArr = pkt_Hello.getUDPdata()
	routerSocket.sendto(bufferArr,(nseHost,nsePort))
	routerLog.write('R'+str(routerId)+' sends an HELLO: router_id '+str(pkt_Hello.getRouterId())+' link_id '+str(pkt_Hello.getLinkId()))
	routerLog.write('\n')
	i = i + 1

i = 0
routerLog.write("Topology database: " + '\n')
while i < len(LSDB):
	routerLog.write("R"+str(LSDB[i].getSender())+" -> "+"R"+str(LSDB[i].getRouterId())+" link "+str(LSDB[i].getLinkId())+" cost "+str(LSDB[i].getCost()))
	routerLog.write('\n')
	i = i + 1


#receive pkts from neighbors
#while (len(discoveredR) < NBR_ROUTER):
#while True:
while (len(LSDB) <= 14):
	bufferReceived = routerSocket.recvfrom(1024)[0]
	if len(bufferReceived) <= 8:
		#received HELLP pkt here
		pkt_Hello = pkt_HELLO(0,0)
		pkt_Hello.parseUDPdata(bufferReceived)
		routerLog.write('R'+str(routerId)+' receives an HELLO: router_id '+str(pkt_Hello.getRouterId())+' link_id '+str(pkt_Hello.getLinkId()))
		routerLog.write('\n')
		if pkt_Hello.getRouterId() not in discoveredR:
			discoveredR.append(pkt_Hello.getRouterId())
			discoveredNeighbors.append(pkt_Hello)
		#pack and send the LSPDU pkts after received HELLO pkt
		i = 0
		while i < nbrLink:
			pkt_lspdu = pkt_LSPDU(LSDB[i].getSender(),LSDB[i].getRouterId(),LSDB[i].getLinkId(),LSDB[i].getCost(),pkt_Hello.getLinkId())
			bufferArr = pkt_lspdu.getUDPdata()
			routerSocket.sendto(bufferArr,(nseHost,nsePort))
			sent_Lspdu = sent_LSPDU(pkt_lspdu.getRouterId(),pkt_lspdu.getLinkId(),pkt_lspdu.getCost())
			sentLspdu.append(sent_Lspdu)
			routerLog.write('R'+str(routerId)+' sends an LSPDU: sender_id '+str(pkt_lspdu.getSender())+' router_id '+str(pkt_lspdu.getRouterId())+' link_id '+str(pkt_lspdu.getLinkId())+' cost '+str(pkt_lspdu.getCost())+' via '+str(pkt_lspdu.getVia()))
			routerLog.write('\n')
			i = i + 1
	else:
		#received LSPDU pkt here
		#print("LSPDU pkt size: ",len(bufferReceived))
		pkt_lspdu = pkt_LSPDU(0,0,0,0,0)
		pkt_lspdu.parseUDPdata(bufferReceived)
		if pkt_lspdu.getRouterId() not in discoveredR:
			discoveredR.append(pkt_lspdu.getRouterId())
		routerLog.write('R'+str(routerId)+' receives an LSPDU: sender_id '+str(pkt_lspdu.getSender())+' router_id '+str(pkt_lspdu.getRouterId())+' link_id '+str(pkt_lspdu.getLinkId())+' cost '+str(pkt_lspdu.getCost())+' via '+str(pkt_lspdu.getVia())+'\n')
		lspdu = LSPDU(pkt_lspdu.getSender(),pkt_lspdu.getRouterId(),pkt_lspdu.getLinkId(),pkt_lspdu.getCost())
		#save_Lspdu = sent_LSPDU(lspdu.getRouterId(),lspdu.getLinkId(),lspdu.getCost())
		#dupLSDB.append(save_Lspdu)

		#if (lspdu.getSender() in discoveredNeighbors):# and (save_Lspdu not in dupLSDB):
		if lspdu not in LSDB:
			LSDB.append(lspdu)
			#dupLSDB.append(save_Lspdu)
			#print the new topology database
			k = 0
			routerLog.write("Topology database: " + '\n')
			while k < len(LSDB):
				routerLog.write("R"+str(LSDB[k].getSender())+" -> "+"R"+str(LSDB[k].getRouterId())+" link "+str(LSDB[k].getLinkId())+" cost "+str(LSDB[k].getCost()))
				routerLog.write('\n')
				k = k + 1
			i = 0
			while i < len(discoveredNeighbors):
				if discoveredNeighbors[i].getRouterId() != pkt_lspdu.getSender():
					pkt_lspdu_new = pkt_LSPDU(routerId,pkt_lspdu.getRouterId(),pkt_lspdu.getLinkId(),pkt_lspdu.getCost(),discoveredNeighbors[i].getLinkId())
					#save_Lspdu = sent_LSPDU(pkt_lspdu_new.getRouterId(),pkt_lspdu_new.getLinkId(),pkt_lspdu_new.getCost())
					if pkt_lspdu_new not in sentLspdu:# and (save_Lspdu not in dupLSBD):
						bufferArr = pkt_lspdu_new.getUDPdata()
						routerSocket.sendto(bufferArr,(nseHost,nsePort))
						sent_Lspdu = sent_LSPDU(pkt_lspdu_new.getRouterId(),pkt_lspdu_new.getLinkId(),pkt_lspdu_new.getCost())
						sentLspdu.append(sent_Lspdu)
						routerLog.write('R'+str(routerId)+' sends an LSPDU: sender_id '+str(pkt_lspdu_new.getSender())+' router_id '+str(pkt_lspdu_new.getRouterId())+' link_id '+str(pkt_lspdu_new.getLinkId())+' cost '+str(pkt_lspdu_new.getCost())+' via '+str(pkt_lspdu_new.getVia())+'\n')
				i = i + 1

			

routerLog.close()




