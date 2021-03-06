import json
import socket
import base64


# create an ipv4 (AF_INET) socket object using the tcp protocol (SOCK_STREAM)
client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
queues=[]
option = 0
# connect the client
# client.connect((target, port))
client.connect(('127.0.0.1', 1233))
response = client.recv(2048)
# Input UserName
name = input(response.decode())	
client.send(str.encode(name))
response = client.recv(2048)
# Input Password
password = input(response.decode())	
client.send(str.encode(password))
''' Response : Status of Connection :
	1 : Registeration successful 
	2 : Connection Successful
	3 : Login Failed
'''
# Receive response 
response = client.recv(2048)
response = response.decode()
print(response)



def cifrar(x):
	ju = json.dumps(x)
	enc = str.encode(ju)
	encoded = base64.b64encode(enc)
	client.send(encoded)

def close_connection():
	
	j = {
		"cmd": "close"
	}
	cifrar(j)
	
	print("close connection")
	client.close()

def create_queue():	
	
	namequeue = input("Queue Name: ")
	j = {
		"cmd": "queue",
		"namequeu": namequeue
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	if(cmd["data"] == ""):
		print("No messages found in queue \"" + namequeue + "\"!")
	else:
		print(cmd["data"])
	
def delete_queue():

	namequeue = input("Queue Name to Delete: ")
	j = {
		"cmd": "delete",
		"namequeu": namequeue
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])

def showmy_queues():
	j = {
		"cmd": "showmq"
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print("My Queues")
	if not cmd["data"]:
		print("There are no queues to show!")
	else:
		for i in cmd["data"]:

			print(i)
		
def showall_queues():
	
	j = {
		"cmd": "showaq"
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print("All Queues")
	
	if not cmd["data"]:
		print("There are no queues to show!")
	else:
		for i in cmd["data"]:

			print(i)
			
def showall_channels():
	
	j = {
		"cmd": "showac"
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print("All Channels")
	
	if not cmd["data"]:
		print("There are no channels to show!")
	else:
		for i in cmd["data"]:

			print(i)

def sendq():
	namequeue= input("Queue Name: ")
	data = input("Your Message: ")
	j = {
		"cmd": "sendq",
		"user": name,
		"namequeue": namequeue,
		"data": data
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])
	
def pullq():
	que=  input("Queue name you want your message from: ")
	j = {
		"cmd": "pullq",
		"queue": que

	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])

def pullc():
	chan=  input("Channel's name you want your message from: ")
	j = {
		"cmd": "pullc",
		"chan": chan

	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])

def queue_subscribe():
	qu = input("Enter the queue you want to subscribe to: ")
	j ={
		"cmd":"queuesubscriber",
		"queue": qu
	}
	ju = json.dumps(j)
	enc = ju.encode()
	encoded= base64.b64encode(enc)
	client.send(encoded)

def create_channel():
	namechannel= input("Input Channel's name: ")
	j = {
		"cmd": "channel",
		"user": name,
		"channel": namechannel,
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	ju = json.loads(dec)
	print(ju["data"])

def delete_channel():
	namechannel = input("Channel's Name to Delete: ")
	j = {
		"cmd": "deletec",
		"channel": namechannel
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])

def showmy_channel():
	j = {
		"cmd": "showmc"
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print("My Channels")
	if not cmd["data"]:
		print("There are no channels to show!")
	else:
		for i in cmd["data"]:

			print(i)

def showmy_channelsus():
	j = {
		"cmd": "showmcs"
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print("Channels I am Suscribed")
	if not cmd["data"]:
		print("There are no channels to show!")
	else:
		for i in cmd["data"]:

			print(i)

def sendc():
	namechannel= input("Channel Name: ")
	data = input("Your Message: ")
	j = {
		"cmd": "sendc",
		"user": name,
		"namequeue": namechannel,
		"data": data
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])

def subscribe_channel():
	cu = input("Enter the Channel you want to subscribe to: ")
	j ={
		"cmd":"subscribec",
		"namequeue": cu
	}
	cifrar(j)
	q = client.recv(2048)
	dec = base64.b64decode(q).decode()
	cmd = json.loads(dec)
	print(cmd["data"])


while (response != "Login Failed"):
	print("\n")
	print("Choose An Option ")
	print("QUEUE OPTION")
	print("1. Create a queue ")
	print("2. Delete a qeueu ")
	print("3. Show my queues ")
	print("4. Show all queues")
	print("5. Send message to a queue")
	print("6. Pull message from a queue")
	print("7. Subscribe a queue")
	print("8. Create a chanel ")
	print("9. Delete a chanel")
	print("10. Show my chanels")
	print("11. Show all chanels")
	print("12. Show channels i am suscribed")
	print("13. Send message to a chanel")
	print("14. Subscribe a chanel")
	print("15. Pull a message from a channel")
	print("16. Close Connection")
	
	option = float(input("Input your option \n"))

	if option == 1:
		create_queue()
		client.close()
		break	
	
	if option == 2:
		delete_queue()
		client.close()
		break
		

	if option == 3:
		showmy_queues()	
		client.close()
		break

	if option == 4:
		showall_queues()
		client.close()
		break	

	if option == 5:
		sendq()
		client.close()
		break	

	if(option == 6):
		pullq()
		client.close()
		break	

	if(option == 7):
		queue_subscribe()
		client.close()
		break	
	
	
	if(option == 8):
		create_channel()
		client.close()
		break
	
	if(option == 9):
		delete_channel()
		client.close()
		break

	if(option == 10 ):
		showmy_channel()
		client.close()
		break
	if(option == 11 ):
		showall_channels()
		client.close()
		break
	
	if(option == 12):
		showmy_channelsus()
		client.close()
		break
	if(option == 13):
		sendc()
		client.close()
		break

	if(option == 14):
		subscribe_channel()
		client.close()
		break
	if option == 15:
		pullc()
		client.close()
		break	
	if option == 16:
		close_connection()
		break	