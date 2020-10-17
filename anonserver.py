import socket
import struct
import sys

 #getting command line arguments
for args in sys.argv:
    if args == '-p':
        localPort = int(sys.argv[sys.argv.index(args)+1])
    if args == '-l':
        logfile = sys.argv[sys.argv.index(args)+1]
    if args == '-u':
        url = sys.argv[sys.argv.index(args)+1]

localIP     = socket.gethostbyname(socket.gethostname())

bufferSize  = 1024

 

msgFromServer       = "Hello UDP Client"

bytesToSend         = str.encode(msgFromServer)

 

# Create a datagram socket

UDPServerSocket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

 

# Bind to address and ip

UDPServerSocket.bind((localIP, localPort))

 

print("UDP server up and listening")

 

# Listen for incoming datagrams

while(True):

    bytesAddressPair = UDPServerSocket.recvfrom(bufferSize)

    message = bytesAddressPair[0]

    address = bytesAddressPair[1]

    clientMsg = "Message from Client:{}".format(message)
    clientIP  = "Client IP Address:{}".format(address)
    
    print(clientMsg)
    print(clientIP)

   

    # Sending a reply to client

    UDPServerSocket.sendto(bytesToSend, address)
