#!/usr/bin/env python

import socket


TCP_IP = '78.91.30.144'
TCP_PORT = 8123
BUFFER_SIZE = 1024
MESSAGE = "Hello, World!"

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.connect((TCP_IP, TCP_PORT))
while 1:
	data = s.recv(BUFFER_SIZE)
	print data
	msg = raw_input('')
	if msg == "exit":
		break
	s.send(msg)
s.close()
