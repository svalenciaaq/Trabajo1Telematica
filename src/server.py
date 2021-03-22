import base64
import socket
import os
from Queue import queue
import threading
import hashlib
import json
from message import message
import time


# Create Socket (TCP) Connection
ServerSocket = socket.socket(family = socket.AF_INET, type = socket.SOCK_STREAM) 
host = '127.0.0.1'
print(host)
port = 1233
ThreadCount = 0


try:
    ServerSocket.bind((host, port))
except socket.error as e:
    print(str(e))

print('Waitiing for a Connection...')
ServerSocket.listen(10)
HashTable = {}
queu= []
qe = ""
queuesubscriber = ""

# Function : For each client 
def threaded_client(connection):
    connection.send(str.encode('Username: ')) # Request Username
    name = connection.recv(2048)
    connection.send(str.encode('Password: ')) # Request Password
    password = connection.recv(2048)
    password = password.decode()
    name = name.decode()
    password=hashlib.sha256(str.encode(password)).hexdigest() # Password hash using SHA256
 # REGISTERATION PHASE   
    
# If new user,  regiter in Hashtable Dictionary  
    if name not in HashTable:
        HashTable[name]=password
        connection.send(str.encode('Registeration Successful')) 
        print('Registered : ',name)
        print("{:<8} {:<20}".format('USER','PASSWORD'))
        for k, v in HashTable.items():
            label, num = k,v
            print("{:<8} {:<20}".format(label, num))
        print("-------------------------------------------")

        f = open ('holamundo.txt','a')
        mensaje = "\n"+ name +" "+password 
        f.write(mensaje)
        print(mensaje)
        f.close()
        
    else:
# If already existing user, check if the entered password is correct
        if(HashTable[name] == password):
            connection.send(str.encode('Connection Successful')) # Response Code for Connected Client 
            print('Connected : ',name)
        else:
            connection.send(str.encode('Login Failed')) # Response code for login failed
            print('Connection Denied : ',name)

    while True:

        # Commands Queue and Channels
        # Qeueu- Create a queue
        # MessageQ= Senda message to a queue
        z = connection.recv(2048)
        dec = base64.b64decode(z).decode()
        print(type(dec))
        cmd = json.loads(dec)
        print(cmd)
        if(cmd["cmd"] == 'queuesubscriber'):
            queuesubscriber = cmd["queue"]
            print("entre")
            break
            

        if(cmd["cmd"] == 'queue'):
            create_queue(cmd["namequeu"],name,connection)
            break

        if(cmd["cmd"] == 'showq'):
          show_queue(name,connection)
          break       

        if(cmd["cmd"] == 'delete'):
            delete_qeueu(cmd["namequeu"], name, connection)

        if(cmd["cmd"] =='sendq'):
           sendq(name,cmd["namequeue"],cmd["data"])
           break
           
        if(cmd["cmd"] == 'close'):
            break    

        if(cmd["cmd"]  == 'pullq'):
            pullq(cmd["queue"],connection)
            break    

    connection.close()
    print("The connection to client " + name +" has been closed.")        

def show_queue(x, con):
    queuesname = []
    for i in queu:
        queuesname.append(i.queu)
    j ={
        "data": json.dumps(queuesname)
    }    
    ju = json.dumps(j)
    enc = str.encode(ju)
    encoded = base64.b64encode(enc)
    con.send(encoded)             

def delete_qeueu(x,y,con):
    j = ""
    for i in queu:
        if(i.user == y):
            if(i.queu == x):
                queu.remove(i)
    je = {
        "data": j
    }   
    ju = json.dumps(je)
    enc = str.encode(ju)
    encoded = base64.b64encode(enc)
    con.send(encoded)         


def create_queue(x,y,con):
    q = queue(x, y)
    j = ""
    alreadyCreated = False
    for i in queu:
          if(i.queu == x):
            alreadyCreated = True
            break 
    if(alreadyCreated):
        j = "Queue named \"" + x +"\" is already created"
        print("Queue named \"" + x +"\" is already created") 
    else:
        j = "Queue named \"" + x +"\" created successfully!"
        queu.append(q)
    je = {
        "data": j
    }   
    ju = json.dumps(je)
    enc = str.encode(ju)
    encoded = base64.b64encode(enc)
    con.send(encoded)          


def sendq(x,y,z):
    msg = message(x,y,z)
    for i in queu:
        if i.queu == msg.queue:
            i.push(msg.data)
            print(i.messages)

def pullq(x,con):
    j=""
    for i in queu:
        if i.queu == x:
            j = i.pop()
            if(j == ""):
                print("no messages found!")
            else:
                print("Messages: " + j)
    je = {
        "data": j
    }   
    ju = json.dumps(je)
    enc = str.encode(ju)
    encoded = base64.b64encode(enc)
    con.send(encoded)                

    
    


while True:
    Client, address = ServerSocket.accept()
    client_handler = threading.Thread(
        target=threaded_client,
        args=(Client,)  
    )
    client_handler.start()
    ThreadCount += 1
    print('Connection Request: ' + str(ThreadCount))
ServerSocket.close()