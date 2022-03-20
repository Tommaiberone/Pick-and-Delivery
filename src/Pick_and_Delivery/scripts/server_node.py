#!/usr/bin/env python

import time
import socket
import threading
import rospy
from std_msgs.msg import String, Float32
from Pick_and_Delivery.msg import NewGoal

HOST = "localhost"
PORT = 12345
DEBUG = True
BUSY = False
SIZE = 1024

class Utente:   
	Username		=	""
	
	class posizione:
		x			=	0
		y			=	0
		theta 		= 	0
	
	def __init__(self, Username, x, y, theta):
		self.Username= Username
		self.posizione.x = x
		self.posizione.y = y
		self.posizione.theta = theta

Utenti =  { 	"Tommaso" 	: 	Utente("Tommaso",0,0,0),
				"Filippo" 	:	Utente("Filippo",0,0,0),
				"Federico" 	:	Utente("Federico",0,0,0),
				"Luigi"		:	Utente("Luigi",0,0,0),
				"Carlo"		:	Utente("Carlo",0,0,0)
			}	


def listen(sock):
	if DEBUG : print("Mi metto in ascolto sulla porta...")
	sock.listen()
	while True:
		client, address = sock.accept()
		if DEBUG : print("Connesso al client con indirizzo", address)
		threading.Thread(target = client_handle_thread,args = (client,address)).start()


def benvenuto(client):
	client.send("Ciao! Dimmi come ti chiami, cosi' vengo a prendere il pacco:\n")
	time.sleep(.5)
	client.send(" -> ")


def arrivato_callback(client):
	print("temp")

#Un thread si occupa di un client dopo essersi connesso
def client_handle_thread(client, address):

	#Ogni thread si iscrive alla topic /Arrived
	Arrivato_checker = 	rospy.Subscriber("/Arrived", String,
			 	  		arrivato_callback,callback_args= client)

	benvenuto(client)

	while True:

		try:
			richiesta_ricevuta = client.recv(SIZE)
		except:
			if DEBUG: print ("Il client con indirizzo", address, "si e' disconnesso correttamente")
			client.close()
			return False

		else:
			messaggio_ricevuto = richiesta_ricevuta.strip().split(",")

			nome_richiedente = messaggio_ricevuto[0]

			if DEBUG: print("Ho ricevuto il messaggio {}, \n".format(messaggio_ricevuto))
			if DEBUG: print("Il nome richiedente e': {}".format(nome_richiedente))

			if nome_richiedente not in Utenti.keys():
				richiesta_sconosciuta(client)

			else:
				if DEBUG: print("Nome utente riconosciuto, invio una risposta")

				client.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(nome_richiedente))
				posizione_richiedente = Utenti[nome_richiedente].posizione

				if DEBUG: print("La posizione del richiedente e': x={}, y={}, theta={}\n".
							format(posizione_richiedente.x, posizione_richiedente.y, posizione_richiedente.theta))

				#while BUSY == True:
				#	client.send("Robot temporaneamente occupato, riprovo in qualche istante...\n")
				#	time.sleep(5)

				BUSY = True 

				elabora_richiesta(client, address, nome_richiedente, posizione_richiedente)						

def elabora_richiesta(client, address, nome_client, posizione_client):

	if DEBUG: print("Ricevuta richiesta di elaborazione pacchetto da parte di {}\n".format(nome_client))
	time.sleep(.5)

	Nuova_destinazione = NewGoal	(	posizione_client.x,
						posizione_client.y,
						posizione_client.theta
					)
					
	NewGoal_Publisher.publish(Nuova_destinazione)

	client.send("Ho impostato correttamente la posizione\n")
	time.sleep(.5)
	client.send("Eccomi! Dove devo portarlo?\n")
	time.sleep(.5)
	client.send(" -> ")
	try:
		messaggio_ricevuto = client.recv(SIZE)
	except:
		if DEBUG: print ("Il client con indirizzo {} si e' disconnesso correttamente".format(address))
		client.close()
		return False

	while True:

		contenuto_messaggio_ricevuto = messaggio_ricevuto.strip().split(",")

		nome_destinatario = contenuto_messaggio_ricevuto[0]

		if nome_destinatario in Utenti.keys():
		
			posizione_destinatario = Utenti[nome_destinatario].posizione

			client.send("Ok! porto il pacchetto a {}".format(nome_destinatario))

			nuova_destinazione = NewGoal	(	posizione_destinatario.x,
												posizione_destinatario.y,
												posizione_destinatario.theta
											)
					
			NewGoal_Publisher.publish(nuova_destinazione)


			time.sleep(5)
			BUSY = False
			break
		else:
			richiesta_sconosciuta(client)
			try:
				messaggio_ricevuto = client.recv(SIZE)
			except:
				if DEBUG: 
					print ("Il client con indirizzo", address, "si e' disconnesso correttamente")
				client.close()
				return False


	
def richiesta_sconosciuta(client):	
	client.send("Ricevuta richiesta sconosciuta\n")
	time.sleep(.5)
	client.send("Per favore elabora...\n")
	time.sleep(.5)
	client.send(" -> ")
	time.sleep(.5)	
	

if __name__ == "__main__":

	rospy.init_node('server', anonymous=True)
	NewGoal_Publisher = rospy.Publisher('New_Goal', NewGoal, queue_size=10)
	rate = rospy.Rate(10)
    
	if (DEBUG): print("Creo la socket del server...")
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
	if (DEBUG): print("Faccio il bind della socket alla porta 12345")
	sock.bind((HOST, PORT))
	listen(sock)
