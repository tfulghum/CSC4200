import socket
import sys
import struct
import random
import logging

#functions
 
def packThePacket(sNum, aNum, A, S, F):
	#This struct needs some work but will otherwise function
	packer = struct.Struct('>iii')
	print(A*2*2 + S*2 + F, hex(sNum), hex(aNum))
	lastLine = A*2*2 + S*2 + F
	packet = packer.pack(sNum, aNum, lastLine)
	print(packet)
	return packet

def stopAndWait(mySocket, buffSiz):
	servMsg = 0
	mySocket.setdefaulttimeout(currentTime)
	
	#Can get rid of exponential backoff
	while not servMsg:
		servMsg = mySocket.recvfrom(buffSiz)
		#I don't think we need this anymore
		#servMsg = "Message from Server {}".format(msgFromServer[0])
	return servMsg

def msgParser(msg):
	packer = struct.Struct('>iii')
	unpackedMsg = packer.unpack(msg)
	seqNumber = unpackedMsg[0]
	ackNumber = unpackedMsg[1]
	flags = unpackedMsg[2]
	
	#Determines which flags are set based on the value of the flags variable
	if flags >= 4:
		A = 1
		flags = flags - 4
	else:
		A = 0
	if flags >= 2:
		S = 1
		flags = flags - 2
	else:
		S = 0
	if flags >= 1:
		F = 1
	else:
		F = 0
	
	return seqNumber, ackNumber, A, S, F
	
def msgParserPayload(msg):
	packer = struct.Struct('>iii512i')
	unpackedMsg = packer.unpack(msg)
	seqNumber = unpackedMsg[0]
	ackNumber = unpackedMsg[1]
	flags = unpackedMsg[2]
	payload = unpackedMsg[3]
	
	#Determines which flags are set based on the value of the flags variable
	if flags >= 4:
		A = 1
		flags = flags - 4
	else:
		A = 0
	if flags >= 2:
		S = 1
		flags = flags - 2
	else:
		S = 0
	if flags >= 1:
		F = 1
	else:
		F = 0
	
	return seqNumber, ackNumber, A, S, F, payload

#getting command line arguments
for args in sys.argv:
    if args == '-s':
        server = sys.argv[sys.argv.index(args)+1]
    elif args == '-p':
        port = int(sys.argv[sys.argv.index(args)+1])
    elif args == '-l':
        logfile = sys.argv[sys.argv.index(args)+1]
		

msgFromClient       = "Hello UDP Server"

bytesToSend         = str.encode(msgFromClient)

serverAddressPort   = (server, port)

bufferSize          = 1024

#Maximum amount of time to wait for stop and wait protocol
maxWait = 500

#Number of failed attempts to send/recieve data from server
numFails = 0

#Sets sequence number to 32 bits
seqNumber = 12345

#Sets ACK number to 32 bits
ackNumber = 0

#Creates the unused portion
#Set default for flags
A = 0
S = 1
F = 0

firstPacket = packThePacket(seqNumber, ackNumber, A, S, F)

# Create a UDP socket at client side

UDPClientSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

#Handshake start

# Send to server using created UDP socket
UDPClientSocket.sendto(firstPacket, serverAddressPort)

#Response from the server
msg = stopAndWait(UDPClientSocket, bufferSize)

#Parse the response
seqNumber, ackNumber, A, S, F = msgParser(msg)

#Kept for debugging
print(seqNumber, ackNumber, A, S, F)

#Create response packet
myPacket = packThePacket(seqNumber, ackNumber, A, S, F)

#Second half of handshake
UDPClientSocket.sendto(myPacket, serverAddressPort)
	
#Payload loop
while(not F):
	#Get response from the server
	msg = stopAndWait(UDPClientSocket, bufferSize)
	seqNumber, ackNumber, A, S, F = msgParser(msg)
	print(seqNumber, ackNumber, A, S, F)
	
	#Send seq and ack depending on recieved values
	if A:
		newAckNumber = seqNumber+1
	if S:
		newSeqValue = ack+1
	myPacket = packer.pack(newSeqNumber, newAckNumber, A, S, F)