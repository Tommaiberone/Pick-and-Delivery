#!/usr/bin/env python2

import time
import socket
import threading
import rospy
from std_msgs.msg import String, Float32
from Pick_and_Delivery.msg import NewGoal

HOST = "localhost"
PORT = 12345
DEBUG = True
SIZE = 1024
ARRIVATO_MSG = "Arrived"
BLOCCATO_MSG = "Stuck"

class Utente:

	Username		=	""
	posizione_x			=	0
	posizione_y			=	0
	posizione_theta 		= 	0
	
	def __init__(self, Username, x, y, theta):
		self.Username= Username
		self.posizione_x = x
		self.posizione_y = y
		self.posizione_theta = theta

Utenti =  	{ 	"Tommaso" 	: 	Utente	("Tommaso", 	19.6,	11.4,	0),
				"Filippo" 	:	Utente	("Filippo", 	5.8,	17.1,	0),
				"Federico" 	:	Utente	("Federico", 	8.3,	21.3,	0),
				"Luigi"		:	Utente	("Luigi", 		43,		13,		0),
				"Carlo"		:	Utente	("Carlo", 		51.5,	6.3,	0)
			}	

class robot:

	going_to_goal 						= 	False
	coming_to_client					= 	False
	busy 								= 	False

	posizione_x							=	0
	posizione_y							=	0
	posizione_theta						= 	0
	
	nome_destinatario 					= 	""

	posizione_destinatario_x			=	0
	posizione_destinatario_y			=	0
	posizione_destinatario_theta		= 	0

def listen(sock):

	if DEBUG : print("Mi metto in ascolto sulla porta...")
	sock.listen(5)
	
	while True:
		client, address = sock.accept()
		if DEBUG : print("Connesso al client con indirizzo", address)
		threading.Thread(target = client_handle_thread,args = (client,address)).start()


def benvenuto(client):
	
	client.send("Ciao! Dimmi come ti chiami e a chi vuoi spedire il pacco: [tuo_nome, nome_destinatario]\n")
	time.sleep(.5)
	client.send(" -> ")

def arrivederci(client):

	client.send("Ciao{}! Ho portato con successo il tuo pacco a destinazione:\n".
				format(client))
	time.sleep(.5)
	client.send("Arrivederci e grazie per aver usato il nostro servizio!")


def status_callback(msg, client):

	if DEBUG: print("Ho ricevuto il messaggio {} dal topic \Arrived".format(msg))

	if (msg.data.lower() == ARRIVATO_MSG.lower()):
		next_step(client)
	
	elif (msg.data.lower() == BLOCCATO_MSG.lower()):
		bloccato(client)

def bloccato(client):

	if DEBUG: print("Il robot e' bloccato\n")
	client.send("Ci dispiace {}, purtroppo la consegna e' bloccata!!\n".format(client))		


def next_step(client):

	if robottino.coming_to_client == True:
		robottino.going_to_goal = True
		robottino.coming_to_client = False
		vai_a(client, robottino.nome_destinatario, (robottino.posizione_destinatario_x, 
													robottino.posizione_destinatario_y, 
													robottino.posizione_destinatario_theta))
	
	elif robottino.going_to_goal == True:
		robottino.coming_to_client = True
		robottino.going_to_goal = False
		robottino.busy = False
		arrivederci(client)



#Un thread si occupa di un client dopo essersi connesso
def client_handle_thread(client, address):

	#Ogni thread si iscrive alla topic /Arrived
	Status_checker = 	rospy.Subscriber("/Arrived", String,
			 	  		status_callback, client)

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

			nome_richiedente = messaggio_ricevuto[0].strip()
			nome_destinatario = messaggio_ricevuto[1].strip()

			if DEBUG: print("Ho ricevuto il messaggio {}, \n".format(messaggio_ricevuto))

			if nome_richiedente not in Utenti.keys() or nome_destinatario not in Utenti.keys():
				richiesta_sconosciuta(client)

			else:

				if DEBUG: print("Il nome del richiedente e': {}".format(nome_richiedente))
				if DEBUG: print("Il nome del destinatario e': {}".format(nome_destinatario))
				
				client.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(nome_richiedente))
				posizione_richiedente = (	Utenti[nome_richiedente].posizione_x,
											Utenti[nome_richiedente].posizione_y,
											Utenti[nome_richiedente].posizione_theta
										)
				
				posizione_destinatario = ( Utenti[nome_destinatario].posizione_x,
											Utenti[nome_destinatario].posizione_y,
											Utenti[nome_destinatario].posizione_theta
										)

				robottino.posizione_destinatario_x = posizione_destinatario[0]
				robottino.posizione_destinatario_y = posizione_destinatario[1]
				robottino.posizione_destinatario_theta = posizione_destinatario[2]

				if DEBUG: print("La posizione del richiedente e': x={}, y={}, theta={}\n".
							format(posizione_richiedente[0], posizione_richiedente[1], posizione_richiedente[2]))

				if DEBUG: print("La posizione del destinatario e': x={}, y={}, theta={}\n".
							format(posizione_destinatario[0], posizione_destinatario[1], posizione_destinatario[2]))

				while robottino.busy == True:
					client.send("Robot temporaneamente occupato, riprovo in qualche istante...\n")
					time.sleep(5)

				robottino.busy = True 
				robottino.coming_to_client = True

				vai_a (client, nome_richiedente, posizione_richiedente)					

def vai_a(client, nome_destinazione, posizione_destinazione):

	if DEBUG and robottino.coming_to_client == True: 
		print("Ricevuta richiesta di elaborazione pacchetto da parte di {}\n".
				format(nome_destinazione))

	Nuova_destinazione = NewGoal	(	posizione_destinazione[0],
										posizione_destinazione[1],
										posizione_destinazione[2]
									)
					
	NewGoal_Publisher.publish(Nuova_destinazione)

	if robottino.coming_to_client == True:
		client.send("Ho impostato correttamente la destinazione, " +
					"sto arrivando a prendere il pacchetto\n")
	else:
		client.send("Ho impostato correttamente la destinazione, " +
					"porto subito il tuo pacchetto\n")


	
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

	robottino = robot()
    
	if (DEBUG): print("Creo la socket del server...")

	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	if (DEBUG): print("Faccio il bind della socket alla porta 12345")

	sock.bind((HOST, PORT))
	listen(sock)
