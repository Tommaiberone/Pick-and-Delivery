#!/usr/bin/env python

import time
import socket
import threading
import rospy
from std_msgs.msg import String, Float32
from Pick_and_Delivery.msg import NewGoal

HOST = "localhost"
PORT = 12345
DEBUG = False
CHATTY = True
SIZE = 1024
ARRIVATO_MSG = "Arrived"
BLOCCATO_MSG = "Stuck"

class Utente:

	Username				=	""
	posizione_x				=	0
	posizione_y				=	0
	posizione_theta 		= 	0
	
	def __init__(self, Username, x, y, theta):
		self.Username= Username
		self.posizione_x = x
		self.posizione_y = y
		self.posizione_theta = theta


class robot:

	going_to_goal 						= 	False
	coming_to_client					= 	False
	busy 								= 	False
	talking								= 	False 	#Flag per evitare che il robottino venga segnalato come bloccato
													#quando e' in attesa di una risposta del client

	Status_checker						=	""
	
	posizione_x							=	0
	posizione_y							=	0
	posizione_theta						= 	0
	
	nome_destinatario 					= 	""

	posizione_destinatario_x			=	0
	posizione_destinatario_y			=	0
	posizione_destinatario_theta		= 	0


Utenti =  	{ 	"Tommaso" 	: 	Utente	("Tommaso", 	11.1,	11.4,	0),
				"Filippo" 	:	Utente	("Filippo", 	19.8,	13.1,	0),
				"Federico" 	:	Utente	("Federico", 	21.9,	11.4,	0),
				"Luigi"		:	Utente	("Luigi", 		37.1,	13.1,	0),
				"Carlo"		:	Utente	("Carlo", 		24.1,	13.5,	0)
			}	


def listen(sock):

	if CHATTY : print("Mi metto in ascolto sulla porta...")
	sock.listen(5)
	
	while True:
		client, address = sock.accept()
		if DEBUG : print("Connesso al client {} con indirizzo {}\n".format(client, address))
		threading.Thread(target = client_handle_thread,args = (client,address)).start()


def benvenuto(client):

	client.send("Ciao! Dimmi come ti chiami cosi' vengo a prendere il pacco\n")
	time.sleep(.5)
	client.send(" -> ")


def arrivederci(client):

	robottino.coming_to_client = False
	robottino.going_to_goal = False
	robottino.busy = False

	client.send("Fatto! Ho portato con successo il tuo pacco a destinazione!\n")
	time.sleep(.5)
	client.send("Arrivederci e grazie per aver usato il nostro servizio!")
	client.close()

	robottino.Status_checker.unregister()	#Disconnette il listener dal topic, 
											#altrimenti si bugga con il prossimo client

	if DEBUG: 
		print("STATS ROBOTTINO:\n\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

#Funzione di callback per il listener sul topic /Arrived
#Viene eseguita ad ogni nuovo messaggio su tale topic, e
#si comporta in modo diverso a seconda del messaggio che ha ricevuto
def status_callback(msg, client):

	if DEBUG: print("Ho ricevuto il messaggio {} dal topic \Arrived".format(msg))

	if (msg.data.lower() == ARRIVATO_MSG.lower()):
		next_step(client)
	
	elif (msg.data.lower() == BLOCCATO_MSG.lower()):
		if not robottino.talking:
			bloccato(client)


def bloccato(client):
 
	if CHATTY: print("Il robot e' bloccato\n")
	client.send("Ci dispiace, purtroppo la consegna e' bloccata!!\n")


def nome_sconosciuto(client):

	client.send("Il nome non risulta essere nel database...\n")
	time.sleep(.5)
	client.send("Per favore riprova!\n")
	time.sleep(.5)
	client.send(" -> ")
	time.sleep(.5)

	try:
		messaggio_ricevuto = client.recv(SIZE)
	except:
		print ("Il client si e' disconnesso in modo inaspettato!")
		client.close()
		return False
	
	robottino.talking = False

	return messaggio_ricevuto.strip()


def next_step(client):

	if robottino.coming_to_client == True:

		robottino.going_to_goal = True
		robottino.coming_to_client = False

		client.send("Eccomi! A chi vuoi portare il pacco?\n")
		time.sleep(.5)
		client.send(" -> ")

		try:
			messaggio_ricevuto = client.recv(SIZE)
		except:
			print ("Il client si e' disconnesso in modo inaspettato!")
			client.close()
			return False

		robottino.talking = False

		nome_destinatario = messaggio_ricevuto.strip()

		while nome_destinatario not in Utenti.keys():
			nome_destinatario = nome_sconosciuto(client)

		if DEBUG: print("Il nome del destinatario e': {}".format(nome_destinatario))

		posizione_destinatario = 	( 	Utenti[nome_destinatario].posizione_x,
										Utenti[nome_destinatario].posizione_y,
										Utenti[nome_destinatario].posizione_theta
									)

		robottino.posizione_destinatario_x = posizione_destinatario[0]
		robottino.posizione_destinatario_y = posizione_destinatario[1]
		robottino.posizione_destinatario_theta = posizione_destinatario[2]

		if DEBUG: print("La posizione del destinatario e': x={}, y={}, theta={}\n".
			format(posizione_destinatario[0], posizione_destinatario[1], posizione_destinatario[2]))

		client.send("Ok! Porto subito il tuo pacco a {}\n".format(nome_destinatario))

		vai_a(client, robottino.nome_destinatario, (robottino.posizione_destinatario_x, 
													robottino.posizione_destinatario_y, 
													robottino.posizione_destinatario_theta))
	
	elif robottino.going_to_goal == True:
		arrivederci(client)


#Un thread si occupa di un client dopo essersi connesso
def client_handle_thread(client, address):

	while robottino.busy == True:
		client.send("Robot temporaneamente occupato, riprovo in qualche istante...\n")
		time.sleep(5)

	robottino.busy = True 
	
	benvenuto(client)

	try:
		richiesta_ricevuta = client.recv(SIZE)
	except:
		print ("Il client con indirizzo {} si e' disconnesso in modo inaspettato".format(address))
		client.close()
		return False

	robottino.talking = False

	nome_richiedente = richiesta_ricevuta.strip()

	if DEBUG: print("Ho ricevuto il messaggio {}, \n".format(nome_richiedente))

	while nome_richiedente not in Utenti.keys():
		nome_richiedente = nome_sconosciuto(client)

	#Ogni thread si iscrive alla topic /Arrived
	robottino.Status_checker = 	rospy.Subscriber("/Arrived", String,
						status_callback, client)

	if DEBUG: print("Il nome del richiedente e': {}".format(nome_richiedente))
	
	client.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(nome_richiedente))
	posizione_richiedente = (	Utenti[nome_richiedente].posizione_x,
								Utenti[nome_richiedente].posizione_y,
								Utenti[nome_richiedente].posizione_theta
							)

	if DEBUG: print("La posizione del richiedente e': x={}, y={}, theta={}\n".
				format(posizione_richiedente[0], posizione_richiedente[1], posizione_richiedente[2]))


	robottino.coming_to_client = True

	vai_a (client, nome_richiedente, posizione_richiedente)				


def vai_a(client, nome_destinazione, posizione_destinazione):

	if CHATTY and robottino.coming_to_client == True: 
		print("Ricevuta richiesta di elaborazione pacchetto da parte di {}\n".
				format(nome_destinazione))

	if DEBUG: 
		print("STATS ROBOTTINO:\n\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

	Nuova_destinazione = NewGoal	(	posizione_destinazione[0],
										posizione_destinazione[1],
										posizione_destinazione[2]
									)
					
	NewGoal_Publisher.publish(Nuova_destinazione)

	if robottino.coming_to_client == True:
		client.send("Ho impostato correttamente la destinazione, " +
					"sto arrivando a prendere il pacchetto\n")
	elif robottino.going_to_goal == True:
		client.send("Ho impostato correttamente la destinazione, " +
					"porto subito il tuo pacchetto\n")

	
def richiesta_sconosciuta(client):	
	client.send("Ricevuta richiesta sconosciuta\n")
	time.sleep(.5)
	client.send("Per favore elabora...\n")
	time.sleep(.5)
	client.send(" -> ")
	time.sleep(.5)
	robottino.talking = True;	
	

if __name__ == "__main__":

	rospy.init_node('server', anonymous=True)
	NewGoal_Publisher = rospy.Publisher('New_Goal', NewGoal, queue_size=10)
	rate = rospy.Rate(10)

	robottino = robot()
    
	if (DEBUG): print("Creo la socket del server...")

	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.settimeout(3000)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	if (DEBUG): print("Faccio il bind della socket alla porta 12345")

	server_socket.bind((HOST, PORT))
	listen(server_socket)
