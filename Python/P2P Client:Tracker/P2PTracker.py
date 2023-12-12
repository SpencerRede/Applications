import socket
import threading
import sys
import datetime
import time

## TODO
# Work out client-client connection 
# Find out how to send files






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

serverPort = 5100

#created a socket that works with TCP and is an internet socket 
serverSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
serverSocket.bind(('127.0.0.1', serverPort))
serverSocket.listen()

#store the clients, check_list, and chunk_list
clients = [] 
check_list = []
chunk_list = []

#broadcast a message to all the connected clients 
def broadcast(client, message):
	for i in range(len(clients)):
		if (client != clients[i]):
			clients[i].send(message.encode())
		

def handle(client):
	while True:
		command = client.recv(1024).decode()
		print(command)
		sys.stdout.flush()
		# Parsed Response into an array of strings
		psdResponse = command.split(",")
		print(f"Command: {psdResponse[0]}")
		sys.stdout.flush()
		if (psdResponse[0] == "LOCAL_CHUNKS") : 
			msgChunknd = int(psdResponse[1])
			msgHash = psdResponse[2]
			clientIP = psdResponse[3]
			clientPort = int(psdResponse[4])
			foundInCheckList = False
			foundInChunkList = False

			# If chunk is already in the chunk_list, then skip
			for chunk in chunk_list :
				if (chunk[0] == msgChunknd and chunk[1] == msgHash and chunk[3] == clientPort):
					foundInChunkList = True
			print("		Not found in chunklist")

			if (not foundInChunkList) :
				# if chunk_index and file_hash already exist in check_list, remove that chunk from the check_list and add it to the chunk_list
				for chunk in check_list :
					if (chunk[0] == msgChunknd and chunk[1] == msgHash):
						check_list.remove(chunk)
						chunk_list.append(chunk)
						chunk_list.append([msgChunknd, msgHash, clientIP, clientPort])
						foundInCheckList = True

			if not foundInCheckList and not foundInChunkList:  check_list.append([msgChunknd, msgHash, clientIP, clientPort])
			print(f"CHECK_LIST: {check_list}")
			print(f"CHUNK_LIST: {chunk_list}\n")
			sys.stdout.flush()

		elif (psdResponse[0] == "WHERE_CHUNK") :
			chunkHash = ""
			msgChunkInd = int(psdResponse[1]) 
			locatedIPAddr = []
			locatedIPPorts = []
			fileFound = False

			for chunk in chunk_list :
				if chunk[0] == msgChunkInd :
					chunkHash = chunk[1]
					locatedIPAddr.append(chunk[2])
					locatedIPPorts.append(chunk[3])
					fileFound = True
			print(f"Found IP Addresses: {locatedIPAddr}")
			if fileFound : 
				print("File Found")
				ipMessage = ""
				for i in range(0, len(locatedIPAddr)) :
					ipMessage = f"{ipMessage},{locatedIPAddr[i]},{locatedIPPorts[i]}"
				clientMessage = f"GET_CHUNK_FROM,{msgChunkInd},{chunkHash}{ipMessage}"
				client.send(clientMessage.encode())
				# client.close()
				# print(f"Closed From client")
				time.sleep(1)
			else : client.send(f"CHUNK_LOCATION_UNKNOWN,{msgChunkInd}".encode())
		else : pass

def receive():
	while True:
		#when a client tries to connect, server will accept  
		client, address = serverSocket.accept()
		print(f"Client: {address} connected")
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


