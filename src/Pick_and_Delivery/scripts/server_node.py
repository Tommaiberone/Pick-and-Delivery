#!/usr/bin/env python

import time
import Queue
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

#Inizializza la classe Utente, con l'username e i parametri di posizione
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

#Inizializza la classe robot, che prende come parametri:
#	-	Dei parametri di controllo
# 	-	L'inizializzazione del listener al topic \Arrived
#	-	I parametri di navigazione, che consistono in 
#	-	-	Posizione del robot
#	-	-	Nome del destinatario
#	-	-	Posizione del destinatario
class robot:

	going_to_goal 						= 	False
	coming_to_client					= 	False
	busy 								= 	False
	talking								= 	False 	#Flag per evitare che il robottino venga segnalato come bloccato
													#quando e' in attesa di una risposta del client

	Status_checker						=	""		#Lo status_checker viene direttamente istanziata alla creazione di un'istanza
													#per evitare un bug che avveniva all'iscrizione di nuovi thread al topic \arrived
	
	posizione_x							=	0
	posizione_y							=	0
	posizione_theta						= 	0
	
	nome_destinatario 					= 	""

	posizione_destinatario_x			=	0
	posizione_destinatario_y			=	0
	posizione_destinatario_theta		= 	0


#Inizializzo gli utenti e le relative posizioni
Utenti =  	{ 	
				"Tommaso" 	: 	Utente	("Tommaso", 	11.1,	11.4,	0),
				"Filippo" 	:	Utente	("Filippo", 	19.8,	13.1,	0),
				"Federico" 	:	Utente	("Federico", 	21.9,	11.4,	0),
				"Luigi"		:	Utente	("Luigi", 		37.1,	13.1,	0),
				"Carlo"		:	Utente	("Carlo", 		24.1,	13.5,	0)
			}	

#Mette il thread principale in ascolto su una porta. 
#Ogni client che si connette viene messo in coda
def listen(sock, fifo):

	if CHATTY : print("Mi metto in ascolto sulla porta...")
	sock.listen(5)
	
	while True:
		
		#Accetta una nuova connessione
		client, address = sock.accept()

		#Mette in coda il client
		fifo.put([client, address])

		#Controlla se il robot e' occupato
		robot_occupato_check(client)

		if CHATTY : print("Inserito in coda il client {} con indirizzo {}\n".format(client, address))

		
# Funzione che controlla se il robot e' occupato. In caso positivo manda un messaggio 
# al client in cui lo avverte che e' stato messo in attesa 
def robot_occupato_check(client):
	if robottino.busy:
		client.send("Ciao! Il robottino al momento e' occupato, ti metto in comunicazione appena possibile\n")
	

# Funzione che, quando il robottino non e' occupato e ci sta qualche client in attesa di essere servito,
# starta un thread che prende in carico la richiesta	
def start_thread(fifo):

	while True:
		
		if not fifo.empty() and not robottino.busy:
			[client, address] = fifo.get()
			threading.Thread(target = client_handle_thread,args = (client,address)).start()

#Manda il messaggio di benvenuto al client e si mette in ascolto di una sua risposta
def benvenuto(client):

	client.send("Ciao! Dimmi come ti chiami cosi' vengo a prendere il pacco\n")
	time.sleep(.5)
	client.send(" -> ")

#Funzione che viene chiamata quando il robottino termina la missione di un client
def arrivederci(client):

	#Resetta i parametri di controllo
	robottino.coming_to_client = False
	robottino.going_to_goal = False
	robottino.busy = False

	#Saluta e chiude la connessione con il client
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

	#Se il messaggio ricevuto indica che il robottino e' giunto a destinazione
	#il robottino passa allo step successivo
	if (msg.data.lower() == ARRIVATO_MSG.lower()):
		next_step(client)
	
	#Se il messaggio ricevuto indica che il robottino e' bloccato
	#Informa il client e chiude la comunicazione
	elif (msg.data.lower() == BLOCCATO_MSG.lower()):
		if not robottino.talking:
			bloccato(client)


#Annuncia al client che la consegna e' bloccata
def bloccato(client):
 
	print("Il robot e' bloccato, prova a riavviare il server\n")
	client.send("Ci dispiace, purtroppo la consegna e' bloccata, chiudo la connessione!\n")

	try: client.close()
	except socket.error as e: print ("Caught exception socket.error :", e)
	exit(0)
		

#Chiede al client di ripetere qualora questo fornisca 
# un messaggio che non viene riconosciuto
def richiesta_sconosciuta(client):	
	client.send("Ricevuta richiesta sconosciuta\n")
	time.sleep(.5)
	client.send("Per favore elabora...\n")
	time.sleep(.5)
	client.send(" -> ")
	time.sleep(.5)
	robottino.talking = True;	


#Fa ripetere al client il nome del mittente o del destinatario,
#nel caso quello indicato non fosse presente nel database
def nome_sconosciuto(client):

	client.send("Il nome non risulta essere nel database...\n")
	time.sleep(.5)
	client.send("Per favore riprova!\n")
	time.sleep(.5)
	client.send(" -> ")
	time.sleep(.5)

	try:
		messaggio_ricevuto = client.recv(SIZE)
	except socket.error as e:
		print ("Il client si e' disconnesso in modo inaspettato!")
		if DEBUG: print ("Il codice di errore e' {}!".format(e))
		client.close()
		return False
	
	robottino.talking = False

	return messaggio_ricevuto.strip()


#Questa e' la funzione invocata inizialmente da ogni thread che ha preso in carico un client
def client_handle_thread(client, address):

	robottino.busy = True 
	
	#Manda il messaggio di benvenuto al client e chiede la posizione 
	#alla quale deve andare a prendere il pacchetto
	benvenuto(client)

	try:
		richiesta_ricevuta = client.recv(SIZE)
	except socket.error as e:
		print ("Il client con indirizzo {} si e' disconnesso in modo inaspettato".format(address))
		if DEBUG: print ("Il codice di errore e' {}!".format(e))
		client.close()
		return False

	robottino.talking = False

	nome_richiedente = richiesta_ricevuta.strip()

	if DEBUG: print("Ho ricevuto il messaggio {}, \n".format(nome_richiedente))

	#Si accerta che il nome del richiedente sia tra quelli la cui posizione e' nota
	while nome_richiedente not in Utenti.keys():
		nome_richiedente = nome_sconosciuto(client)

	#Ogni thread si iscrive alla topic /Arrived
	robottino.Status_checker = 	rospy.Subscriber("/Arrived", String, status_callback, client)

	if DEBUG: print("Il nome del richiedente e': {}".format(nome_richiedente))
	client.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(nome_richiedente))

	#Imposta la destinazione sulla base della posizione dell'utente nel database
	posizione_richiedente = (	Utenti[nome_richiedente].posizione_x,
								Utenti[nome_richiedente].posizione_y,
								Utenti[nome_richiedente].posizione_theta
							)

	if DEBUG: print("La posizione del richiedente e': x={}, y={}, theta={}\n".
				format(posizione_richiedente[0], posizione_richiedente[1], posizione_richiedente[2]))

	robottino.coming_to_client = True

	#Invoca la funzione che determina l'effettivo movimento del robot
	vai_a (client, nome_richiedente, posizione_richiedente)


#Aggiorna le indicazioni del robottino in seguito ad uno 
# step completato (pacco recapitato, pacco preso in carico)
def next_step(client):

	#Se il robottino stava consegnando il pacco vuol dire che ora l'ha consegnato
	#ed e' pronto per una nuova missione
	#Quindi saluta il client
	if robottino.going_to_goal == True:
		arrivederci(client)

	#Se il robottino invece stava venendo a prendere il pacco vuol dire che ora
	#e' pronto a portarlo a destinazione
	elif robottino.coming_to_client == True:

		robottino.going_to_goal = True
		robottino.coming_to_client = False

		#Il robottino si sincera del destinatario del pacchetto
		client.send("Eccomi! A chi vuoi portare il pacco?\n")
		time.sleep(.5)
		client.send(" -> ")

		try:
			messaggio_ricevuto = client.recv(SIZE)
		except socket.error as e:
			print ("Il client si e' disconnesso in modo inaspettato!")
			if DEBUG: print ("Il codice di errore e' {}!".format(e))
			return False

		robottino.talking = False

		nome_destinatario = messaggio_ricevuto.strip()

		while nome_destinatario not in Utenti.keys():
			nome_destinatario = nome_sconosciuto(client)

		if DEBUG: print("Il nome del destinatario e': {}".format(nome_destinatario))

		#Imposta le variabili di destinazione del robottino sulla base della posizione del destinatario
		robottino.posizione_destinatario_x 		= 	Utenti[nome_destinatario].posizione_x
		robottino.posizione_destinatario_y 		= 	Utenti[nome_destinatario].posizione_y
		robottino.posizione_destinatario_theta 	= 	Utenti[nome_destinatario].posizione_theta

		if DEBUG: print("La posizione del destinatario e': x={}, y={}, theta={}\n".
			format(robottino.posizione_destinatario_x, robottino.posizione_destinatario_y , robottino.posizione_destinatario_theta))

		client.send("Ok! Porto subito il tuo pacco a {}\n".format(nome_destinatario))

		#Invoca la funzione che determina l'effettivo movimento del robot
		vai_a(client, robottino.nome_destinatario, (robottino.posizione_destinatario_x, 
													robottino.posizione_destinatario_y, 
													robottino.posizione_destinatario_theta))
					

#Pubblica sul topic \NewGoal i parametri di destinazione che gli vengono forniti in input
def vai_a(client, nome_destinazione, posizione_destinazione):

	if CHATTY and robottino.coming_to_client == True: 
		print("Ricevuta richiesta di elaborazione pacchetto da parte di {}\n".
				format(nome_destinazione))

	if DEBUG: 
		print("STATS ROBOTTINO:\n\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

	#Crea il messaggio Nuova_destinazione da passare al publisher
	Nuova_destinazione = NewGoal	(	posizione_destinazione[0],
										posizione_destinazione[1],
										posizione_destinazione[2]
									)

	#Il messaggio viene pubblicato					
	NewGoal_Publisher.publish(Nuova_destinazione)

	#Manda un feedback al client
	if robottino.coming_to_client == True:
		client.send("Ho impostato correttamente la destinazione, " +
					"sto arrivando a prendere il pacchetto\n")
	elif robottino.going_to_goal == True:
		client.send("Ho impostato correttamente la destinazione, " +
					"porto subito il tuo pacchetto\n")

if __name__ == "__main__":

	#Inizializza il nodo ROS del server
	rospy.init_node('server', anonymous=True)

	#Imposta il publisher sul topic \New_Goal
	NewGoal_Publisher = rospy.Publisher('New_Goal', NewGoal, queue_size=10)
	rate = rospy.Rate(10)

	#Inizializza il robottino
	robottino = robot()

	#Inizializza la coda con paradigma FIFO
	fifo = Queue.Queue()

	if (CHATTY): print("Creo la socket del server...")

	#Crea la socket del server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.settimeout(3000)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	if (CHATTY): print("Faccio il bind della socket alla porta 12345")

	server_socket.bind((HOST, PORT))

	#Crea il thread il cui scopo e' mettere in coda i client in arrivo
	threading.Thread(target = listen,args = (server_socket, fifo)).start()

	#Lancia la funzione che preleva i client dalla coda e li mette in comunicazione
	# con il robottino tramite la creazione di nuovi thread
	start_thread(fifo)
