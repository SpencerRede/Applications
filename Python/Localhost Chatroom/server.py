import socket
import threading
import sys
import datetime

#sentence = connectionSocket.recv(1024).decode()
 		#capitalizedSentence = sentence.upper()
 		#connectionSocket.send(capitalizedSentence.encode())
 		#connectionSocket.close()  
		#connectionSocket.send("You are now connected!".encode())
 		#connectionSocket.close()  
 		#sys.exit()

#TODO: Implement all code for your server here

# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	pass

serverPort = int(sys.argv[3])
serverPassword = sys.argv[5]

#created a socket that works with TCP and is an internet socket 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen()

#store the clients name/usernames  
clients = []
usernamesList = []

#broadcast a message to all the connected clients 
def broadcast(client, message):
	for i in range(len(clients)):
		if (client != clients[i]):
			clients[i].send(message.encode())
		

def handle(client):
	while True:
		message = client.recv(1024).decode()
		index = clients.index(client)
		username = usernamesList[index]
		currTime = datetime.datetime.now()

		if message == ':Exit':
			clients.remove(client)
			usernamesList.remove(username)
			print("{} left the chatroom".format(username))
			sys.stdout.flush()

			broadcast(client, "{} left the chatroom".format(username))
			client.send("CLOSE".encode());
			client.close()
			break
		elif message == ":)":
			print("{}: [feeling happy]".format(username))
			sys.stdout.flush()
			broadcast(client, "{}: [feeling happy]".format(username))
		elif message == ":(":
			print("{}: [feeling sad]".format(username))
			sys.stdout.flush()
			broadcast(client, "{}: [feeling sad]".format(username))
		elif message == ":mytime":
			print("{}; {}".format(username, currTime.strftime("%H:%M:%S")))
			sys.stdout.flush()
			broadcast(client, "{}: {}".format(username, currTime.strftime("%H:%M:%S")))
		elif message == ":+1hr":
			oneHourLater = currTime + datetime.timedelta(hours=1) 
			print("{}: {}".format(username, oneHourLater.strftime("%a %b %d %H:%M:%S %Y")))
			sys.stdout.flush()
			broadcast(client, "{}: {}".format(username, oneHourLater.strftime("%a %b %d %H:%M:%S %Y")))
		else: 
			print('{}: {}'.format(username, message))
			sys.stdout.flush()
			broadcast(client, '{}: {}'.format(username, message))

def receive():
	while True:
		#when a client tries to connect, server will accept  
		client, address = serverSocket.accept()
		# print("Connected to {}".format(address))
		# sys.stdout.flush()
		password = client.recv(1024).decode()
		if password != serverPassword: 
			client.send('Incorrect passcode'.encode())
			client.close()
			break

		#request and store the username
		client.send('Nick'.encode())
		username = client.recv(1024).decode()
		usernamesList.append(username)

		#print the username and broadcast it
		# print("The username of the client is {}".format(username))
		# sys.stdout.flush()
		print("{} joined the chatroom".format(username))
		sys.stdout.flush()
		broadcast(client, "{} joined the chatroom".format(username))

		connectedToMesssage = "Connected to {} on port {}".format("127.0.0.1", serverPort)
		client.send(connectedToMesssage.encode())
		#client.send(sentence)

		clients.append(client)

		#starts handling the thread for the client
		thread = threading.Thread(target=handle, args=(client,))
		thread.start()


print("Server started on port {}. Accepting connections".format(serverPort))
sys.stdout.flush()
#executes the receive function which will start an endless while loop
#to accept new connections from clients constantly
receive()
#sys.exit()


