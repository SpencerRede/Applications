import random
import socket
import argparse
import threading
import sys
import hashlib
import time
import logging
import hashlib
import random
import traceback

if __name__ == "__main__":
	pass

# Command Line arg
#  cdcd


folderName = sys.argv[2]
transferPort = int(sys.argv[4])
name = sys.argv[6]
clients = []
logging.basicConfig(filename="logs.log", level=logging.INFO)

sent_chunks = []

# initate connection with P2P Tracker
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect(('localhost', 5100))

listeningSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
listeningSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR,1)
listeningSocket.bind(('127.0.0.1', transferPort))
listeningSocket.listen()


def hash_file(filename):
   """"This function returns the SHA-1 hash
   of the file passed into it"""

   # make a hash object
   h = hashlib.sha1()

   # open file for reading in binary mode
   with open(filename,'rb') as file:

       # loop till the end of the file
       chunk = 0
       while chunk != b'':
           # read only 1024 bytes at a time
           chunk = file.read(1024)
           h.update(chunk)

   # return the hex representation of digest
   return h.hexdigest()


folderChunks = []
# Parsing the local_chunks file into a list of tuples
with open(f"{folderName}/local_chunks.txt") as fp:
	for i in fp.readlines():
		tmp = i.split(",")
		try:
			folderChunks.append((int(tmp[0]), tmp[1].strip("\n")))
			#result.append((eval(tmp[0]), eval(tmp[1])))
		except:pass

	print(folderChunks)

def parseChunks():
	# TODO Send the hashes of all files accessable from folderName to socket
	# LOCAL_CHUNKS, <chunk_ind>, <file_hash>, <IP_addr>, <Port_nbr> 
	i = 0
	while (folderChunks[i][1] != "LASTCHUNK"):
		chunkInd = folderChunks[i][0]
		fileHash = hash_file(f"{folderName}/{folderChunks[i][1]}")
		print(f"  ... Considering chunk_{chunkInd}")
		if not (sent_chunks.__contains__(chunkInd)) :
			print(f"	... PARSING chunk_{chunkInd}")
			# ipAddr = socket.gethostbyname(socket.gethostname())
			portNumber = transferPort

			print(f"		... Sending chunks to {client}")
			command = f"LOCAL_CHUNKS,{chunkInd},{fileHash},localhost,{portNumber}"
			client.send(command.encode())
			time.sleep(1)

			sent_chunks.append(chunkInd)
			#Log the command as well as appending the name of the client sending it
			logging.info(f"{name},{command}")
		i += 1


# #listening to the server and sending username
def handle(client):
	while True:
		try:
			# P2Pclient, address = listeningSocket.accept()
			response = client.recv(1024).decode()

			# P2PTracker response
			print(f"	{response}")
			sys.stdout.flush()
			currentFile = ""

			# Parsed Response into an array of strings
			psdResponse = response.split(",")
			if (psdResponse[0] == "GET_CHUNK_FROM") :
				logging.info(f"P2PTracker,{response}")
				
				# Logic for finding a random IP an cooresponding port
				numIPaddr = int((len(psdResponse) - 4) / 2)
				randomIPind = random.randrange(numIPaddr + 1)
				randomIP = psdResponse[3+(randomIPind * 2)]
				randomPort = psdResponse[4+(randomIPind * 2)]
				print(f"Connecting to IP:{randomIP} on PORT:{randomPort}")
				sys.stdout.flush()

				client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
				client.connect((randomIP, int(randomPort)))
				print("	...Connected")

				sys.stdout.flush()
				client.send(f"REQUEST_CHUNK,{psdResponse[1]},{randomIP},{randomPort}".encode())
				time.sleep(1)
				logging.info(f"{name},REQUEST_CHUNK,{psdResponse[1]},{randomIP},{randomPort}")
			elif (psdResponse[0] == "CHUNK_LOCATION_UNKNOWN") :
				logging.info(f"P2PTracker,{response}")
				pass
			elif(psdResponse[0] == "DATA"):
				print(f"Recieved File chunk_{psdResponse[1]}: len = {len(psdResponse[2])}")
				sys.stdout.flush()
				f = open(f"{folderName}/chunk_{psdResponse[1]}", "ab")

				if (psdResponse[2] != "STOP") :
					f.write(psdResponse[2].encode('ANSI'))
				else :
					print("STOPPING")
					sys.stdout.flush()
					f.close()
					folderChunks.insert(0, [psdResponse[1], f"chunk_{psdResponse[1]}"])
					f = open(f"{folderName}/local_chunks.txt", "w")
					for chunk in folderChunks :
						f.write(f"{chunk[0]},{chunk[1]}\n")
					f.close()
					
					print(f"SENDING LOCALCHUNK")
					parseChunks()
					break

		except Exception:
			client.close()
			traceback.print_exc()
			break

def listenTransfer(client):
	while True:	
		try :
			response = client.recv(1024).decode()
			print(response)
			sys.stdout.flush()

			# Parsed Response into an array of strings
			psdResponse = response.split(",")
			if (psdResponse[0] == "REQUEST_CHUNK"):

				filename = f"{folderName}/chunk_{psdResponse[1]}"
				f = open(filename,'rb')
				print (f"Sending... {filename}")
				sys.stdout.flush()
				l = f.read(1024).decode("ANSI")
				l.zfill(1024-len(l))
				while (l):
					print(f"Sending:{l}")
					sys.stdout.flush()
					client.send(f"DATA,{psdResponse[1]},{l}".encode())
					time.sleep(1)
					l = f.read(1024)
				
				STOPmsg = f"DATA,{psdResponse[1]},STOP"
				print(f"Sending: {STOPmsg}")
				sys.stdout.flush()
				client.send(f"{STOPmsg}".encode())
				time.sleep(1)
				client.close()
				break
			
		except Exception:
			client.close()
			traceback.print_exc()
			break
		
def receive():
	while True:
		#when a client tries to connect, server will accept  
		P2Pclient, address = listeningSocket.accept()
		print(f"Client: {address} connected")
		sys.stdout.flush()
		clients.append(client)

		#starts handling the thread for the client
		thread = threading.Thread(target=listenTransfer, args=(P2Pclient,))
		thread.start()

#function to send messages to the server 
def write():
	while (input != "EXIT"):
		inputMessage = input('')
		logging.info(f"{name},{inputMessage}")
		client.send(inputMessage.encode())

parseChunks()

handle_thread = threading.Thread(target=handle, args=(client,))
handle_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()

receive()

# Python program to find the SHA-1 message digest of a file

# importing the hashlib module


#message = clientSocket.recv(1024)
#clientSocket.close()
#print(message.decode())
#sentence = raw_input("Input lowercase sentence:")
#clientSocket.send(sentence.encode())
#modifiedSentence = clientSocket.recv(1024)
#print("From Server: ", modifiedSentence.decode())
#clientSocket.close()
#sys.stdout.flush()