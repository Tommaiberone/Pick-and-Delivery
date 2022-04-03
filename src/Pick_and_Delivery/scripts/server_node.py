#!/usr/bin/env python

import time
import math 
import socket
import threading
import rospy
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
import tf2_ros
from Pick_and_Delivery.msg import NewGoal

HOST = "localhost"
PORT = 12345
DEBUG = True
CHATTY = True
SIZE = 1024
ARRIVATO_MSG = "Arrived"
BLOCCATO_MSG = "Stuck"

#Inizializza la classe Utente, con l'username e i parametri di posizione
class Utente:

	Username				=	""
	posizione_x				=	0
	posizione_y				=	0
	
	def __init__(self, Username, x, y):
		self.Username= Username
		self.posizione_x = x
		self.posizione_y = y

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

	posizione_destinatario_x			=	0
	posizione_destinatario_y			=	0

	nome_destinatario 					= 	""
	client_served 						= 	""
	address_served 						= 	""


#Inizializzo gli utenti e le relative posizioni
Utenti =  	{ 	
				"Tommaso" 	: 	Utente	("Tommaso", 	11.1,	11.4),
				"Filippo" 	:	Utente	("Filippo", 	19.8,	13.1),
				"Federico" 	:	Utente	("Federico", 	21.9,	11.4),
				"Luigi"		:	Utente	("Luigi", 		37.1,	13.1),
				"Carlo"		:	Utente	("Carlo", 		24.1,	13.5)
			}	


#Manda il messaggio di benvenuto al client e si mette in ascolto di una sua risposta
def benvenuto(client, address):

	client.send("Ciao! Dimmi come ti chiami cosi' vengo a prendere il pacco\n")
	time.sleep(.5)
	client.send(" -> ")

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
		nome_richiedente = nome_sconosciuto()

	#Mette in coda il client
	clientList.append([nome_richiedente, client, address])

	#Controlla se il robot e' occupato
	robot_occupato_check(client)

	if CHATTY : print("Inserito in lista il client {} con indirizzo {}\n".format(client, address))		

	if DEBUG:
		print("Lista dei client in attesa:\n")
		for elem in clientList:
			print("{}, {}, {}".format(elem[0], elem[1], elem[2]))
	

#Mette il thread principale in ascolto su una porta. 
#Ogni client che si connette viene messo in coda
def clientListen(sock):

	if CHATTY : print("Mi metto in ascolto sulla porta...")
	sock.listen(5)
	
	while True:
		
		#Accetta una nuova connessione
		client, address = sock.accept()

		#Si sincera del nome del richiedente e lo aggiunge alla lista d'attesa
		threading.Thread(target = benvenuto,args = (client, address, )).start()

		
# Funzione che controlla se il robot e' occupato. In caso positivo manda un messaggio 
# al client in cui lo avverte che e' stato messo in attesa 
def robot_occupato_check(client):
	if robottino.busy:
		client.send("Ciao! Il robottino al momento e' occupato, ti metto in comunicazione appena possibile\n")
	

def checkDistance(nome1, nome2):
	if  (
			math.sqrt(math.pow(robottino.posizione_x - Utenti[nome1].posizione_x, 2)+ 
			math.pow(robottino.posizione_y-Utenti[nome1].posizione_y, 2)) 
			< 
			math.sqrt(math.pow(robottino.posizione_x-Utenti[nome2].posizione_x, 2)+ 
			math.pow(robottino.posizione_y-Utenti[nome2].posizione_y, 2)) 
		
		):
		return True
	return False



def retrieve_from_list():

	print("\n\n\nMI HANNO CHIAMATO AIUTO\n\n\n")

	nome_richiedente, client, address = clientList[0]
	daRimuovere = 0
	counter = 0
	
	if (len(clientList) != 1):

		if DEBUG: print("Piu' di un client in attesa, scelgo quello piu' vicino al robot\n")

		for elem in clientList:

			if checkDistance(elem[0], nome_richiedente):
				nome_richiedente= elem[0]
				client= elem[1]
				address= elem[2]
				daRimuovere=counter

			counter+=1

	if DEBUG: print("Rimuovo {} dalla lista dei client in attesa\n".format(nome_richiedente))

	clientList.pop(daRimuovere)

	robottino.nome_destinatario = nome_richiedente
	robottino.client_served = client
	robottino.address_served = address


# Funzione che, quando il robottino non e' occupato e ci sta qualche client in attesa di essere servito,
# starta un thread che prende in carico la richiesta	
def start_thread():

	while True:
		
		if len(clientList) != 0 and not robottino.busy:

			print("\n\nOCIO\n\n")

			retrieve_from_list()

			#Imposta le variabili di destinazione del robottino sulla base della posizione del destinatario
			robottino.posizione_destinatario_x 		= 	Utenti[robottino.nome_destinatario].posizione_x
			robottino.posizione_destinatario_y 		= 	Utenti[robottino.nome_destinatario].posizione_y

			if DEBUG: print("Servo la richiesta di {}, client #{}, con indirizzo {}\n".
						format(robottino.nome_destinatario, robottino.client_served, robottino.address_served))
			threading.Thread(target = client_handle_thread).start()


#Funzione che viene chiamata quando il robottino termina la missione di un client
def arrivederci():

	#Saluta e chiude la connessione con il client
	robottino.client_served.send("Fatto! Ho portato con successo il tuo pacco a destinazione!\n")
	time.sleep(.5)
	robottino.client_served.send("Arrivederci e grazie per aver usato il nostro servizio!")
	robottino.client_served.close()

	robottino.Status_checker = ""	#Disconnette il listener dal topic, 
									#altrimenti si bugga con il prossimo client

	if DEBUG: 
		print("STATS ROBOTTINO:\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))
	
	#Resetta i parametri di controllo
	robottino.coming_to_client = False
	robottino.going_to_goal = False
	robottino.busy = False

#Funzione di callback per il listener sul topic /Arrived
#Viene eseguita ad ogni nuovo messaggio su tale topic, e
#si comporta in modo diverso a seconda del messaggio che ha ricevuto
def status_callback(msg):

	if DEBUG: print("Ho ricevuto il messaggio {} dal topic \Arrived".format(msg))

	#Se il messaggio ricevuto indica che il robottino e' giunto a destinazione
	#il robottino passa allo step successivo
	if (msg.data.lower() == ARRIVATO_MSG.lower()):
		next_step()
	
	#Se il messaggio ricevuto indica che il robottino e' bloccato
	#Informa il client e chiude la comunicazione
	elif (msg.data.lower() == BLOCCATO_MSG.lower()):
		if not robottino.talking:
			bloccato()


#Annuncia al client che la consegna e' bloccata
def bloccato():
 
	print("Il robot e' bloccato, prova a riavviare il server\n")
	robottino.client_served.send("Ci dispiace, purtroppo la consegna e' bloccata, chiudo la connessione!\n")

	try: robottino.client_served.close()
	except socket.error as e: print ("Caught exception socket.error :", e)
	exit(0)
		

#Chiede al client di ripetere qualora questo fornisca 
# un messaggio che non viene riconosciuto
def richiesta_sconosciuta():	
	robottino.client_served.send("Ricevuta richiesta sconosciuta\n")
	time.sleep(.5)
	robottino.client_served.send("Per favore elabora...\n")
	time.sleep(.5)
	robottino.client_served.send(" -> ")
	time.sleep(.5)
	robottino.talking = True;	


#Fa ripetere al client il nome del mittente o del destinatario,
#nel caso quello indicato non fosse presente nel database
def nome_sconosciuto():

	robottino.client_served.send("Il nome non risulta essere nel database...\n")
	time.sleep(.5)
	robottino.client_served.send("Per favore riprova!\n")
	time.sleep(.5)
	robottino.client_served.send(" -> ")
	time.sleep(.5)

	try:
		messaggio_ricevuto = robottino.client_served.recv(SIZE)
	except socket.error as e:
		print ("Il client si e' disconnesso in modo inaspettato!")
		if DEBUG: print ("Il codice di errore e' {}!".format(e))
		robottino.client_served.close()
		return False
	
	robottino.talking = False

	return messaggio_ricevuto.strip()


#Questa e' la funzione invocata inizialmente da ogni thread che ha preso in carico un client
def client_handle_thread():

	robottino.busy = True 

	#Ogni thread si iscrive alla topic /Arrived
	if (robottino.Status_checker != ""):
		print("\n\nERRORE NELLO STATUS CHECKER!\n\n")

	robottino.Status_checker = 	rospy.Subscriber("/Arrived", String, status_callback)

	if DEBUG: print("Il nome del richiedente e': {}".format(robottino.nome_destinatario))
	robottino.client_served.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(robottino.nome_destinatario))

	if DEBUG: print("La posizione del richiedente e': x={}, y={}\n".
				format(robottino.posizione_destinatario_x, robottino.posizione_destinatario_y))

	robottino.coming_to_client = True

	#Invoca la funzione che determina l'effettivo movimento del robot
	vai_a ()


#Aggiorna le indicazioni del robottino in seguito ad uno 
# step completato (pacco recapitato, pacco preso in carico)
def next_step():

	if DEBUG: 	print("nome client: {}, client #{}, address{}\n".
				format(robottino.nome_destinatario, robottino.client_served, robottino.address_served))

	#Se il robottino stava consegnando il pacco vuol dire che ora l'ha consegnato
	#ed e' pronto per una nuova missione
	#Quindi saluta il client
	if robottino.going_to_goal == True:
		arrivederci()

	#Se il robottino invece stava venendo a prendere il pacco vuol dire che ora
	#e' pronto a portarlo a destinazione
	elif robottino.coming_to_client == True:

		robottino.going_to_goal = True
		robottino.coming_to_client = False

		#Il robottino si sincera del destinatario del pacchetto
		robottino.client_served.send("Eccomi! A chi vuoi portare il pacco?\n")
		time.sleep(.5)
		robottino.client_served.send(" -> ")

		try:
			messaggio_ricevuto = robottino.client_served.recv(SIZE)
		except socket.error as e:
			print ("Il client si e' disconnesso in modo inaspettato!")
			if DEBUG: print ("Il codice di errore e' {}!".format(e))
			return False

		robottino.talking = False

		nome_destinatario = messaggio_ricevuto.strip()

		while nome_destinatario not in Utenti.keys():
			nome_destinatario = nome_sconosciuto()

		if DEBUG: print("Il nome del destinatario e': {}".format(nome_destinatario))

		#Imposta le variabili di destinazione del robottino sulla base della posizione del destinatario
		robottino.posizione_destinatario_x 		= 	Utenti[nome_destinatario].posizione_x
		robottino.posizione_destinatario_y 		= 	Utenti[nome_destinatario].posizione_y

		if DEBUG: print("La posizione del destinatario e': x={}, y={}\n".
			format(robottino.posizione_destinatario_x, robottino.posizione_destinatario_y))

		robottino.client_served.send("Ok! Porto subito il tuo pacco a {}\n".format(nome_destinatario))

		#Invoca la funzione che determina l'effettivo movimento del robot
		vai_a()
					

#Pubblica sul topic \NewGoal i parametri di destinazione che gli vengono forniti in input
def vai_a():

	if CHATTY and robottino.coming_to_client == True: 
		print("Ricevuta richiesta di elaborazione pacchetto da parte di {}\n".
				format(robottino.nome_destinatario))

	if DEBUG: 
		print("STATS ROBOTTINO:\n\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

	#Crea il messaggio Nuova_destinazione da passare al publisher
	Nuova_destinazione = NewGoal	(	robottino.posizione_destinatario_x,
										robottino.posizione_destinatario_y,
										0.0
									)

	#Il messaggio viene pubblicato					
	NewGoal_Publisher.publish(Nuova_destinazione)

	#Manda un feedback al client
	if robottino.coming_to_client == True:
		robottino.client_served.send("Ho impostato correttamente la destinazione, " +
					"sto arrivando a prendere il pacchetto\n")
	elif robottino.going_to_goal == True:
		robottino.client_served.send("Ho impostato correttamente la destinazione, " +
					"porto subito il tuo pacchetto\n")


#Funzione di callback del listener sul topic /tf
#Si occupa di aggiornare i parametri di navigazione del robottino
#sulla base di quanto viene stampato da ROS sul topic
def position_callback(tf):

    #Si accerta di poter effettuare la trasformazione
    transform_ok = transformCalculator.can_transform('map','base_link', rospy.Time(0))

    if transform_ok != 0:

        #Trova i nuovi parametri di navigazione del robottino sulla base della 
        #trasformazione ottenuta con:
        #   -   source_frame = base_link
        #   -   target_frame = map
        #   -   rospy.Time(0) fa si' che i parametri di cui sopra siano gli ultimi disponibili
        transformation = TransformStamped()
        transformation = transformCalculator.lookup_transform('map', 'base_link', rospy.Time(0))
        
        #Aggiorna la posizione del robottino
        robottino.posizione_x = transformation.transform.translation.x
        robottino.posizione_y = transformation.transform.translation.y



if __name__ == "__main__":

	#Inizializza il nodo ROS del server
	rospy.init_node('server', anonymous=True)

	#Imposta il publisher sul topic \New_Goal
	NewGoal_Publisher = rospy.Publisher('New_Goal', NewGoal, queue_size=10)
	rate = rospy.Rate(10)

	#Inizializza il robottino
	robottino = robot()

	#Inizializza la lista
	clientList = list()

	if (CHATTY): print("Creo la socket del server...")

	#Crea la socket del server
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.settimeout(3000)
	server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

	if (CHATTY): print("Faccio il bind della socket alla porta 12345")

	server_socket.bind((HOST, PORT))


	#Inizializza i calcolatori di trasformate interni di ROS
	transformCalculator = tf2_ros.Buffer()
	listener = tf2_ros.TransformListener(transformCalculator)

	subscriber_tf     = rospy.Subscriber( '/tf',   TFMessage,   position_callback)

	#Crea il thread il cui scopo e' mettere in coda i client in arrivo
	threading.Thread(target = clientListen,args = (server_socket,)).start()

	#Lancia la funzione che preleva i client dalla coda e li mette in comunicazione
	# con il robottino tramite la creazione di nuovi thread
	start_thread()
