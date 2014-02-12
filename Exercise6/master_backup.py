import os
from time import sleep
from socket import *
import json
from threading import Thread
from datetime import datetime

class Counter(Thread):
	def __init__(self, count, handler, ismaster=False):
		""" Initializes the thread """
		Thread.__init__(self)
		self.count = count
		self.handler = handler
		self.ismaster = ismaster


		self.addr = ('127.0.0.1', 8005)
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.setblocking(0)
		self.interrupt = False
		self.last_ping = datetime.now()

		if not self.ismaster:
			self.sock.bind(self.addr)

	def init_socket(self):
		""" Initializing the socket, master is receiving and backup is sending """
		self.sock = socket(AF_INET, SOCK_DGRAM)
		self.sock.setsockopt(SOL_SOCKET, SO_REUSEADDR, 1)
		self.sock.setblocking(0)
		if not self.ismaster:
			self.sock.bind(self.addr)

	def send_ping(self):
		""" Printing the ping and sending a status to the backup """
		print self.count
		self.count += 1
		data = json.dumps({'STATUS': 'IM ALIVE', 'COUNT': self.count})
		self.sock.sendto(data, self.addr)

	def run(self):
		""" Thread is running """
		while not self.interrupt:
			if self.ismaster:
				self.send_ping()
			else:
				self.check_message()
			sleep(0.5)

	def check_message(self):
		""" Checks if there is a message to get in the buffer. Checks the time of the last status is got from the master.
		If it's too long, it assumes that the master has crashed and sets itself as master, and telling the mainclass to spawn a new backup """
		interval = (datetime.now()-self.last_ping).seconds
		if interval > 1:
			print 'YOU HAVE TO BECOME A MASTER MY FRIEND'
			self.ismaster = True
			self.sock.close()
			self.init_socket()
			self.handler.should_create_backup = True
			return
		try:
			data, addr = self.sock.recvfrom(1024)
			self.last_ping = datetime.now()
		except:
			return
		if data:
			data = json.loads(data)
			self.count = data['COUNT']
		else:
			pass

class ThreadHandler:
	def __init__(self):
		self.threads = {'master': Counter(0, self, True), 'backup': Counter(0, self)}
		self.should_create_backup = False

	def spawn_thread(self, ismaster):
		""" Spawns a new backup """
		self.threads['master'] = self.threads['backup']
		self.threads['backup'] = Counter(0, self)
	
	def run(self):
		""" Runs the main """
		for _, thread in self.threads.items():
			thread.start()
		while True:
			if self.should_create_backup:
				self.threads['master'] = self.threads['backup'] 
				self.threads['backup'] = Counter(0, self)
				self.threads['backup'].start()
				self.should_create_backup = False
			if not self.threads['master']:
				continue
			try:
				self.threads['master'].join(1)
			except KeyboardInterrupt:
				print "Ctrl+C received, shutting down master"
				count = self.threads['master'].count
				self.threads['master'].interrupt = True
				self.threads['master'].join()

handler = ThreadHandler()
print os.getpid()
handler.run()