import socket
import threading
import sys 


#TODO: Implement a client that connects to your server to chat with other clients here

# Use sys.stdout.flush() after print statemtents

if __name__ == "__main__":
	pass

serverName = sys.argv[3]
serverPort = int(sys.argv[5])
username = sys.argv[7]
password = sys.argv[9]
# print("Connecting to {} on port {} with name: {} and password: {}".format(serverName, serverPort, username, password));
# sys.exit()

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((serverName, serverPort))
client.send(password.encode())

#listening to the server and sending username
def receive():
	while True:
		try:
			message = client.recv(1024).decode()
			#message from server, if it matches then send username 
			if message == 'Nick':
				client.send(username.encode())
			elif message == "CLOSE":
				# print("You have been disconncted");
				# sys.stdout.flush()
				client.close()
				break
			else:
				print(message)
				sys.stdout.flush()
		except:
			#close connection when there's an error
			print("I'm sorry. An error occured")
			sys.stdout.flush()
			client.close()
			break

#function to send messages to the server 
def write():
	inputMessage = ''
	while inputMessage != ":Exit":
		inputMessage = input('')
		client.send(inputMessage.encode())

receive_thread = threading.Thread(target=receive)
receive_thread.start()

write_thread = threading.Thread(target=write)
write_thread.start()



#message = clientSocket.recv(1024)
#clientSocket.close()
#print(message.decode())
#sentence = raw_input("Input lowercase sentence:")
#clientSocket.send(sentence.encode())
#modifiedSentence = clientSocket.recv(1024)
#print("From Server: ", modifiedSentence.decode())
#clientSocket.close()
#sys.stdout.flush()