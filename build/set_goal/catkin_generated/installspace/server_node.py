#!/usr/bin/env python2

import time
import socket
import threading

host = "localhost"
port = 12345
debug = True
busy = False
size = 1024

Database =  {   "Tommaso"   :   "Posizione_Tommaso",
				"Filippo"   :   "Posizione_Filippo",
				"Federico"  :   "Posizione_Federico",
				"Luigi"     :   "Posizione_Luigi",
				"Andrea"    :   "Posizione_Andrea"
                }


def listen(sock):
	if debug : print("Mi metto in ascolto sulla porta...")
	sock.listen(5)
	while True:
		client, address = sock.accept()
		if debug : print("Connesso al client con indirizzo", address)
		threading.Thread(target = server_thread,args = (client,address)).start()

def server_thread(client, address):

	while True:
		try:
			data = client.recv(size)
			if data:
				if data == "call":
					# Set the response to echo back the recieved data
					if busy == False :
						busy = True 
						elabora(client, address)
						continue
				else:
					client.send("Ricevuta richiesta sconosciuta\n")
					time.sleep(.5)
					client.send("Per favore elabora...\n")
					time.sleep(.5)
					client.send(" -> ")
			else:
				raise error('Client disconnected')
		except:
			if debug: print ("Il client con indirizzo", address, "si e' disconnesso "+
							  "correttamente")
			client.close()
			return False

def elabora(client, address):
	client.send("Ricevuta richiesta di elaborazione pacchetto\n")
	time.sleep(.5)
	client.send("Simulo di starlo venendo a prendere\n")
	time.sleep(5)
	client.send("Eccomi! Dove devo portarlo?\n")
	time.sleep(.5)
	client.send(" -> ")
	try:
		data = client.recv(size)
	except:
		if debug: print ("Il client con indirizzo", address, "si e' disconnesso "+
							"correttamente")
		client.close()
		return False
	while True:
		if data in Database.keys():
			client.send("Ok! porto il pacchetto a "+ data + " in posizione "+ Database[data]+ "\n")
			time.sleep(5)
			busy = False
			break
		else:
			client.send("Ricevuta richiesta sconosciuta\n")
			time.sleep(.5)
			client.send("Per favore elabora...\n")
			time.sleep(.5)
			client.send(" -> ")
			time.sleep(.5)
			try:
				data = client.recv(size)
			except:
				if debug: print ("Il client con indirizzo", address, "si e' disconnesso "+
									"correttamente")
				client.close()
				return False


	
	
	

if __name__ == "__main__":
    
	if (debug): print("Creo la socket del server...")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	if (debug): print("Faccio il bind della socket alla porta 12345")
	sock.bind((host, port))
	listen(sock)