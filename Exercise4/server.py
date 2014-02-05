import socket
import json

address = ('127.0.0.1', 5005)

sock = socket.socket(socket.AF_INET, # Internet
                     socket.SOCK_DGRAM) # UDP
sock.bind(address)

while True:
    data, addr = sock.recvfrom(1024) # buffer size is 1024 bytes
    if not data:
    	break
    print "received message:", json.loads(data)
    print type(json.loads(data))
    sock.sendto(data, addr)

sock.close()