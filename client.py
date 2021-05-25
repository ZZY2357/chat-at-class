import tkinter as tk
import socket
import threading

host = input('Type server: ')
port = int(input('Type port: '))

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
clientSocket.connect((host, port))

# GUI
root = tk.Tk()
root.title('Chat At Class By zzy')

messageText = tk.Text(root)
inputComponet = tk.Entry(root, width=100)

def sendButtonClicked():
	clientSocket.send(inputComponet.get().encode('utf-8'))
	if inputComponet.get().startswith('/exit') or inputComponet.get().startswith('/quit'):
		root.destroy()
	else:
		inputComponet.delete(0, tk.END)
sendButton = tk.Button(root, text='Send', command=sendButtonClicked)

messageText.grid(column=0)
inputComponet.grid(column=0, row=1)
sendButton.grid(column=1, row=1)

# Network
def handleSocketThread():
	while True:
		msg = clientSocket.recv(2048)
		if msg:
			messageText.insert(tk.END, msg.decode() + '\n\r')
socketThread = threading.Thread(target=handleSocketThread)
socketThread.start()

# GUI main loop
root.mainloop()
clientSocket.send(b'/exit')
clientSocket.close()
