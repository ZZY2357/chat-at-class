import socket
import threading
import time
import sys

class Server:
	def __init__(self, port=6324):
		self.host = '0.0.0.0'
		self.port = port

		self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
		self.socket.bind((self.host, self.port))
		self.socket.listen()

	def handleClientThread(self, clientSocket, addr):
		client = Client(clientSocket, addr)
		while True:
			msg = client.recvMessage()
			if msg:
				self.sendMessageFromClient(client, msg)
			if msg.startswith('/nick'):
				client.nickName = msg.split(' ')[1].replace(':', '.')
			if msg.startswith('/quit') or msg.startswith('/exit'):
				client.close()
				break

	def sendMessageFromClient(self, client, msg):
		for c in clients:
			c.sendMessage(f'{ client.nickName }: { msg }')

	def sendMessageToClient(self, client, msg):
		client.sendMessage(f'SERVER: { msg }')

clients = []
class Client:
	def __init__(self, socket, addr):
		self.id = time.time()
		self.nickName = self.id

		self.socket = socket
		self.addr = addr

		clients.append(self)

	def recvMessage(self):
		msg = self.socket.recv(2048)
		return msg.decode()

	def sendMessage(self, msg):
		self.socket.send(msg.encode('utf-8'))

	def close(self):
		for i in range(len(clients)):
			if clients[i].id == self.id:
				del clients[i]
				break

try:
	port = int(input('Type port[6324]: '))
except:
	port = 6324

server = Server(port)
print(f'Server is runing at { socket.gethostbyname(socket.gethostname()) }:{ port }')

while True:
	clientSocket, addr = server.socket.accept()
	print(f'{ addr } has connected.')

	clientThread = threading.Thread(target=server.handleClientThread, args=(clientSocket, addr))
	clientThread.start()
