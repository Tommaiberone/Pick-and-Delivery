#!/usr/bin/env python

from operator import truediv
import time
import sys
import math 
import socket
import threading

from numpy import average
import rospy
from std_msgs.msg import String
from tf2_msgs.msg import TFMessage
from geometry_msgs.msg import TransformStamped
import tf2_ros
from Pick_and_Delivery.msg import NewGoal

HOST 				= 	"localhost"
PORT 				= 	12345
SUPERDEBUG 			= 	False
DEBUG 				= 	False
CHATTY 				= 	False
MEASURE 			= 	True
SIZE 				= 	1024
ARRIVATO_MSG 		= 	"Arrived"
BLOCCATO_MSG 		= 	"Stuck"
NUM_CLIENTS 		= 	28

POSIZIONE_MOTHERBASE_X = 0
POSIZIONE_MOTHERBASE_Y = 0

#Paradigmi
FIFO 						= 	True		#Implementato
PRIORITY_QUEUE 				= 	False		#Implementato
DISTANCE_AND_MAX_TIME 		= 	False		#Implementato
DISTANCE 					= 	False		#Implementato
MITT_EQUALS_DEST_CHECK		= 	False		#Implementato
FULL_PATH_PREDICT			=	False		#Implementato

#Modificatori dei paradigmi
###Per attivarne uno deve essere attivo almeno uno dei paradigmi di sopra
WAIT_POSITION_MOTHERBASE	= 	False		#Implementato
WAIT_POSITION_PRECALC		= 	False		#Manca la parte in cui viene effettivamente precalcolata la posizione

MAX_PRIORITY = 5
HIGH_PRIORITY = 4
MEDIUM_PRIORITY = 3
LOW_PRIORITY = 2
NO_PRIORITY = 1

#Inizializza la classe Utente, con l'username e i parametri di posizione
class Utente:

	Username				=	""
	posizione_x				=	0
	posizione_y				=	0
	priority 				=	0
	
	def __init__(self, Username, x, y, priority):
		self.Username= Username
		self.posizione_x = x
		self.posizione_y = y
		self.priority = priority

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
	going_precalc_position				= 	False
	coming_home							= 	False
	busy 								= 	False
	talking								= 	False 	#Flag per evitare che il robottino venga segnalato come bloccato
													#quando e' in attesa di una risposta del client

	Status_checker						=	""		#Lo status_checker viene direttamente istanziata alla creazione di un'istanza
													#per evitare un bug che avveniva all'iscrizione di nuovi thread al topic \arrived
	
	posizione_x							=	0
	posizione_y							=	0

	posizione_mittente_x				=	0
	posizione_mittente_y				=	0

	posizione_destinatario_x			=	0
	posizione_destinatario_y			=	0

	posizione_motherbase_x				= 	POSIZIONE_MOTHERBASE_X
	posizione_motherbase_y				= 	POSIZIONE_MOTHERBASE_Y
	
	posizione_di_attesa_x 				= 	POSIZIONE_MOTHERBASE_X
	posizione_di_attesa_y				= 	POSIZIONE_MOTHERBASE_Y

	nome_mittente	 					= 	""
	client_served 						= 	""
	address_served 						= 	""
	nome_destinatario					= 	""
	tempo_presa_in_carico				= 	0
	supercounter						= 	0
	tempo_inizializzazione				= 	0


#Inizializzo gli utenti e le relative posizioni
Utenti =  	{ 	
				"Tommaso" 		: 	Utente	("Tommaso", 		11.1,	11.4, 	MAX_PRIORITY),
				"Filippo" 		:	Utente	("Filippo", 		19.8,	13.1, 	HIGH_PRIORITY),
				"Federico" 		:	Utente	("Federico", 		21.9,	11.4, 	MEDIUM_PRIORITY),
				"Luigi"			:	Utente	("Luigi", 			37.1,	13.1, 	LOW_PRIORITY),
				"Carlo"			:	Utente	("Carlo", 			24.1,	13.5, 	NO_PRIORITY),
				"Francesco"		:	Utente	("Francesco", 		6.0,	17.0, 	HIGH_PRIORITY),
				"Pietro"		:	Utente	("Pietro", 			8.7,	21.5, 	MEDIUM_PRIORITY),
				"Peppe"			:	Utente	("Peppe", 			8.4,	25.5, 	LOW_PRIORITY),
				"Massimo"		:	Utente	("Massimo", 		42.6,	10.8, 	MAX_PRIORITY),
				"Bianca"		:	Utente	("Bianca", 			5.5,	13.0, 	NO_PRIORITY)

			}	


#Manda il messaggio di benvenuto al client e si mette in ascolto di una sua risposta
def benvenuto(client, address):

	client.send("Ciao! Dimmi come ti chiami cosi' vengo a prendere il pacco\n")
	time.sleep(.1)
	client.send(" -> ")

	try:
		richiesta_ricevuta = client.recv(SIZE)
	except socket.error as e:
		print ("Il client con indirizzo {} si e' disconnesso in modo inaspettato".format(address))
		if DEBUG: print ("Il codice di errore e' {}!".format(e))
		client.close()
		return False

	nome_richiedente = richiesta_ricevuta.strip()

	if SUPERDEBUG: print("Ho ricevuto il messaggio {}, \n".format(nome_richiedente))

	#Si accerta che il nome del richiedente sia tra quelli la cui posizione e' nota
	while nome_richiedente not in Utenti.keys():
		nome_richiedente = nome_sconosciuto()

	client.send("Ciao {}! A chi vuoi portare il pacchetto?\n".format(nome_richiedente))
	time.sleep(.1)
	client.send(" -> ")

	try:
		richiesta_ricevuta = client.recv(SIZE)
	except socket.error as e:
		print ("Il client con indirizzo {} si e' disconnesso in modo inaspettato".format(address))
		if DEBUG: print ("Il codice di errore e' {}!".format(e))
		client.close()
		return False

	robottino.talking = False

	nome_destinatario = richiesta_ricevuta.strip()

	if SUPERDEBUG: print("Ho ricevuto il messaggio {}, \n".format(nome_destinatario))

	#Si accerta che il nome del richiedente sia tra quelli la cui posizione e' nota
	while nome_destinatario not in Utenti.keys():
		nome_destinatario = nome_sconosciuto()

	#Mette in coda il client
	clientList.append([nome_richiedente, client, address, nome_destinatario, Utenti[nome_richiedente].priority, 0, time.time()])

	#Controlla se il robot e' occupato. In caso positivo manda un messaggio 
	# al client in cui lo avverte che e' stato messo in attesa	
	if robottino.busy:
		try: client.send("Ciao! Il robottino al momento e' occupato, ti metto in comunicazione appena possibile\n")
		except: do_nothing()
		time.sleep(.1)

	if CHATTY : print("Inserito in lista il client {} con un pacchetto per {}\n".format(nome_richiedente, nome_destinatario))		

	if DEBUG:
		print("Lista dei client in attesa:\n")
		for elem in clientList:
			print("{} con un pacco per {}".format(elem[0], elem[3]))

	               
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
	
def checkDistance(nome1, nome2):
	if  (
			math.sqrt	(	
							math.pow(robottino.posizione_x - Utenti[nome1].posizione_x, 2)+ 
							math.pow(robottino.posizione_y - Utenti[nome1].posizione_y, 2)
						) 
			< 
			math.sqrt	(	
							math.pow(robottino.posizione_x - Utenti[nome2].posizione_x, 2)+ 
							math.pow(robottino.posizione_y - Utenti[nome2].posizione_y, 2)
						) 
		
		):
		return True
	return False

def checkFullDistance(mittente_nuovo, mittente_vecchio, destinatario_nuovo, destinatario_vecchio):
	if	(math.sqrt	(	
				math.pow(robottino.posizione_x - Utenti[mittente_nuovo].posizione_x, 2)+ 
				math.pow(robottino.posizione_y - Utenti[mittente_nuovo].posizione_y, 2)
		) + math.sqrt	(	
				math.pow(Utenti[mittente_nuovo].posizione_x- Utenti[destinatario_nuovo].posizione_x, 2)+ 
				math.pow(Utenti[mittente_nuovo].posizione_y- Utenti[destinatario_nuovo].posizione_y, 2)
		) 
		<
		math.sqrt	(	
				math.pow(robottino.posizione_x - Utenti[mittente_vecchio].posizione_x, 2)+ 
				math.pow(robottino.posizione_y - Utenti[mittente_vecchio].posizione_y, 2)
		) + math.sqrt	(	
				math.pow(Utenti[mittente_vecchio].posizione_x- Utenti[destinatario_vecchio].posizione_x, 2)+ 
				math.pow(Utenti[mittente_vecchio].posizione_y- Utenti[destinatario_vecchio].posizione_y, 2)
		)):
		return True
	return False

def retrieve_from_list():

	if (len(clientList) == 0):
		return

	if DEBUG:
		for elem in clientList:
			print("\n\n{} con un pacco per {}\n\n".format(elem[0], elem[3]))

	nome_richiedente, client, address, nome_destinatario, priority, inutile1, inutile2 = clientList[0]
	daRimuovere = 0
	counter = 0
	
	if (len(clientList) != 1):
		
		if (FIFO):
			do_nothing()

		elif (PRIORITY_QUEUE):
			
			if CHATTY: print("Piu' di un client in attesa, scelgo quello con priorita' maggiore\n")

			for elem in clientList:

				if (elem[4] > priority):
					nome_richiedente= elem[0]
					client= elem[1]
					address= elem[2]
					priority= elem[3]
					daRimuovere=counter

				counter+=1

		elif (DISTANCE_AND_MAX_TIME):

			if CHATTY: print("Piu' di un client in attesa, scelgo quello piu' vicino al robot o quello non servito da troppo tempo\n")

			done = False

			for elem in clientList:
				
				#Se c'e' un client in attesa da almeno tre "turni" allora il robot sceglie di servire
				#lui a prescindere dalla distanza
				if done == False and elem[5] > 2:
					nome_richiedente= elem[0]
					client = elem[1]
					address = elem[2]
					daRimuovere = counter
					done = True
				
				if done == False and checkDistance(elem[0], nome_richiedente):
					nome_richiedente= elem[0]
					client= elem[1]
					address= elem[2]
					daRimuovere=counter
				
				elem[5]+=1
				counter+=1

				done = False

		elif (DISTANCE):
			
			for elem in clientList:

				if checkDistance(elem[0], nome_richiedente):
					nome_richiedente= elem[0]
					client= elem[1]
					address= elem[2]
					nome_destinatario= elem[3]
					daRimuovere=counter

				counter+=1
	
		elif (MITT_EQUALS_DEST_CHECK):

			for elem in clientList:
				
				if checkDistance(elem[0], nome_richiedente):
					nome_richiedente= elem[0]
					client= elem[1]
					address= elem[2]
					daRimuovere=counter
				counter+=1

			counter = 0

			for elem in clientList:

				#Se c'e' un client in attesa il cui destinatario corrisponde con il mittente
				#di un altro client in attesa serve direttamente lui
				for elem2 in clientList:

					if elem[3] == elem2[0]:
						nome_richiedente= elem[0]
						client = elem[1]
						address = elem[2]
						daRimuovere = counter
						break
				
				counter+=1
			
		elif FULL_PATH_PREDICT:
			
			for elem in clientList:

				if checkFullDistance(elem[0], nome_richiedente, elem[3], nome_destinatario):
					nome_richiedente= elem[0]
					client= elem[1]
					address= elem[2]
					nome_destinatario= elem[3]
					daRimuovere=counter

				counter+=1

	if DEBUG: print("Rimuovo {} dalla lista dei client in attesa\n".format(nome_richiedente))

	tempo_presa_in_carico = time.time()
	presa_in_carico_list.append(tempo_presa_in_carico - clientList[daRimuovere][6])

	if MEASURE and CHATTY: 
		print("Il client {} e' stato preso in carico dopo {} secondi da quando ha fatto richiesta\n"
			.format(nome_richiedente, tempo_presa_in_carico - clientList[daRimuovere][6]))


	clientList.pop(daRimuovere)
	orderList.append(nome_richiedente)

	if DEBUG:
		print("Lista dei client in attesa:")
		for elem in clientList:
			print("{} con un pacco per {}".format(elem[0], elem[3]))

	robottino.nome_mittente = nome_richiedente
	robottino.nome_destinatario = nome_destinatario
	robottino.client_served = client
	robottino.address_served = address
	robottino.tempo_presa_in_carico = tempo_presa_in_carico

def do_nothing():
	return	

# Funzione che, quando il robottino non e' occupato e ci sta qualche client in attesa di essere servito,
# starta un thread che prende in carico la richiesta	
def start_thread():

	while True:
		
		if robottino.busy:
			continue

		if len(clientList) != 0:

			retrieve_from_list()

			#Imposta le variabili di destinazione del robottino sulla base della posizione del destinatario
			robottino.posizione_mittente_x 		= 	Utenti[robottino.nome_mittente].posizione_x
			robottino.posizione_mittente_y 		= 	Utenti[robottino.nome_mittente].posizione_y

			if DEBUG: print("Servo la richiesta di {}, client #{}, con indirizzo {}\n".
						format(robottino.nome_mittente, robottino.client_served, robottino.address_served))
			threading.Thread(target = client_handle_thread).start()
		
		elif WAIT_POSITION_MOTHERBASE:
			robottino.coming_home = True
			vai_a()

		elif WAIT_POSITION_PRECALC:
			robottino.going_precalc_position = True
			vai_a()

#Funzione che viene chiamata quando il robottino termina la missione di un client
def arrivederci():

	#Saluta e chiude la connessione con il client
	try:robottino.client_served.send("Fatto! Ho portato con successo il tuo pacco a destinazione!\n")
	except: do_nothing()
	time.sleep(.1)

	try:robottino.client_served.send("Arrivederci e grazie per aver usato il nostro servizio!")
	except: do_nothing()
	time.sleep(.1)

	robottino.client_served.close()

	#Disconnette il listener dal topic, altrimenti si bugga con il prossimo client
	robottino.Status_checker.unregister()	 
	robottino.Status_checker = ""	

	if CHATTY:
		print("Portato correttamente il pacco di {} a {}\n".format(robottino.nome_mittente, robottino.nome_destinatario)) 

	if SUPERDEBUG: 
		print("STATS ROBOTTINO:\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

	if MEASURE and CHATTY: print("Il client {} e' stato servito dopo {} secondi da quando e' stato preso in carico\n".
				format(robottino.nome_mittente, time.time() - robottino.tempo_presa_in_carico))
				
	tempo_serviti_list.append(time.time() - robottino.tempo_presa_in_carico)
	
	robottino.supercounter += 1

	if robottino.supercounter == NUM_CLIENTS:
		if MEASURE and CHATTY: 
			print("Il tempo di inizializzaione e' di {} secondi".format(robottino.tempo_inizializzazione))
			print("Il corrente e' di {} secondi\n".format(time.time()))
		
		if MEASURE:
			print("Il tempo totale per servire tutti i clients e' stato di {} secondi\n".
					format(time.time() - robottino.tempo_inizializzazione))
			print("Ho servito i clients in quest'ordine:")
			for elem in orderList:
				print(elem)

			tempo_medio_presa_in_carico = average(presa_in_carico_list)
			tempo_massimo_presa_in_carico = max(presa_in_carico_list)
			tempo_medio_servizio = average(tempo_serviti_list)
			tempo_massimo_servizio = max(tempo_serviti_list)

			print("\nIl tempo medio in cui sono stati presi in carico i pacchetti dei client " +
				  "dal momento in cui e' stata effettuata la richiesta e' stato di {} secondi".format(tempo_medio_presa_in_carico))

			print("\nIl tempo massimo che ha aspettato un client prima che fosse preso in carico il suo pacchetto " +
				  "dal momento in cui e' stata effettuata la richiesta e' stato di {} secondi".format(tempo_massimo_presa_in_carico))

			print("\nIl tempo medio in cui sono stati portati a destinazione i pacchetti dei client " +
				  "dal momento in cui sono stati presi in carico e' stato di {} secondi".format(tempo_medio_servizio))

			print("\nIl tempo massimo impiegagto a portare a destinazione un pacchetto " +
				  "dal momento in cui e' stato preso in carico e' stato di {} secondi".format(tempo_massimo_servizio))

		sys.stdout.close()

	#Resetta i parametri di controllo
	robottino.coming_to_client = False
	robottino.going_to_goal = False
	robottino.busy = False

#Funzione di callback per il listener sul topic /Arrived
#Viene eseguita ad ogni nuovo messaggio su tale topic, e
#si comporta in modo diverso a seconda del messaggio che ha ricevuto
def status_callback(msg):

	if SUPERDEBUG: print("Ho ricevuto il messaggio {} dal topic \Arrived".format(msg))

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
	try:robottino.client_served.send("Ci dispiace, purtroppo la consegna e' bloccata, chiudo la connessione!\n")
	except: do_nothing()
	time.sleep(.1)

	try: robottino.client_served.close()
	except socket.error as e: print ("Caught exception socket.error :", e)
	exit(0)
		
#Chiede al client di ripetere qualora questo fornisca 
# un messaggio che non viene riconosciuto
def richiesta_sconosciuta():	
	robottino.client_served.send("Ricevuta richiesta sconosciuta\n")
	time.sleep(.1)
	robottino.client_served.send("Per favore elabora...\n")
	time.sleep(.1)
	robottino.client_served.send(" -> ")
	time.sleep(.1)
	robottino.talking = True;	

#Fa ripetere al client il nome del mittente o del destinatario,
#nel caso quello indicato non fosse presente nel database
def nome_sconosciuto():

	robottino.client_served.send("Il nome non risulta essere nel database...\n")
	time.sleep(.1)
	robottino.client_served.send("Per favore riprova!\n")
	time.sleep(.1)
	robottino.client_served.send(" -> ")
	time.sleep(.1)

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
	robottino.coming_home = False
	robottino.going_precalc_position = False
	robottino.coming_to_client = True

	#Verifica che il robottino non stia gia' servendo un client
	if (robottino.Status_checker != ""):
		robottino.supercounter+=1
		if DEBUG or CHATTY: print("\n\nERRORE NELLO STATUS CHECKER!\n\n")
		#Bypassa il problema contando il client come servito 
 
	#Ogni thread si iscrive alla topic /Arrived
	robottino.Status_checker = 	rospy.Subscriber("/Arrived", String, status_callback)

	if SUPERDEBUG: print("Il nome del richiedente e': {}".format(robottino.nome_mittente))
	try:
		robottino.client_served.send("Ciao {}! Vengo subito a prendere il pacco:\n".format(robottino.nome_mittente))
	except: do_nothing()
	time.sleep(.1)

	if SUPERDEBUG: print("La posizione del richiedente e': x={}, y={}\n".
				format(robottino.posizione_mittente_x, robottino.posizione_mittente_y))

	#Invoca la funzione che determina l'effettivo movimento del robot
	vai_a ()

#Aggiorna le indicazioni del robottino in seguito ad uno 
# step completato (pacco recapitato, pacco preso in carico)
def next_step():

	#if DEBUG: 	print("nome client: {}, client #{}, address{}\n".
	#			format(robottino.nome_destinatario, robottino.client_served, robottino.address_served))


	if robottino.coming_home: robottino.coming_home = False
	if robottino.going_precalc_position: robottino.going_precalc_position = False

	#Se il robottino stava consegnando il pacco vuol dire che ora l'ha consegnato
	#ed e' pronto per una nuova missione
	#Quindi saluta il client
	elif robottino.going_to_goal == True:
		arrivederci()

	#Se il robottino invece stava venendo a prendere il pacco vuol dire che ora
	#e' pronto a portarlo a destinazione
	elif robottino.coming_to_client == True:

		robottino.going_to_goal = True
		robottino.coming_to_client = False

		
		#Imposta le variabili di destinazione del robottino sulla base della posizione del destinatario
		robottino.posizione_destinatario_x 		= 	Utenti[robottino.nome_destinatario].posizione_x
		robottino.posizione_destinatario_y 		= 	Utenti[robottino.nome_destinatario].posizione_y

		if SUPERDEBUG: print("La posizione del destinatario e': x={}, y={}\n".
			format(robottino.posizione_destinatario_x, robottino.posizione_destinatario_y))

		try: robottino.client_served.send("Ok! Porto subito il tuo pacco a {}\n".format(robottino.nome_destinatario))
		except: do_nothing()
		time.sleep(.1)

		#Invoca la funzione che determina l'effettivo movimento del robot
		vai_a()
					
#Pubblica sul topic \NewGoal i parametri di destinazione che gli vengono forniti in input
def vai_a():

	if CHATTY and robottino.coming_to_client == True: 
		print("Vado a prendere il pacchetto da parte di {} per {}\n".
				format(robottino.nome_mittente, robottino.nome_destinatario))

	elif CHATTY and robottino.going_to_goal == True: 
		print("Porto il pacchetto di {} a {}\n".
				format(robottino.nome_mittente, robottino.nome_destinatario))

	if SUPERDEBUG: 
		print("STATS ROBOTTINO:\n\ncoming_to_client: {},\ngoing_to_goal: {},\nbusy: {}\n\n".
				format(robottino.coming_to_client, robottino.going_to_goal, robottino.busy))

	#Crea il messaggio Nuova_destinazione da passare al publisher
	if robottino.coming_to_client:
		Nuova_destinazione = NewGoal	(	robottino.posizione_mittente_x,
											robottino.posizione_mittente_y,
											0.0
										)
		
		#Manda un feedback al client
		try: robottino.client_served.send("Ho impostato correttamente la destinazione, " +
					"sto arrivando a prendere il pacchetto\n")
		except: do_nothing()
		time.sleep(.1)

	elif robottino.going_to_goal:
		Nuova_destinazione = NewGoal	(	robottino.posizione_destinatario_x,
											robottino.posizione_destinatario_y,
											0.0
										)
		#Manda un feedback al client
		try: robottino.client_served.send("Ho impostato correttamente la destinazione, " +
					"porto subito il tuo pacchetto\n")
		except: do_nothing()
		time.sleep(.1)
	
	elif robottino.coming_home:
		Nuova_destinazione = NewGoal	(	robottino.posizione_motherbase_x,
											robottino.posizione_motherbase_y,
											0.0
										)
	
	elif robottino.going_precalc_position:
		Nuova_destinazione = NewGoal	(	robottino.posizione_di_attesa_x,
											robottino.posizione_di_attesa_y,
											0.0
										)

	#Il messaggio viene pubblicato					
	NewGoal_Publisher.publish(Nuova_destinazione)
		

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

	#Inizializza varie liste per la misurazione
	orderList = list()
	presa_in_carico_list = list()
	tempo_serviti_list = list()

	#Rendirizza i print verso un file
	if DISTANCE:
		file_path = 'DISTANCE.txt'
	elif FIFO:
		file_path = 'FIFO.txt'
	elif DISTANCE_AND_MAX_TIME:
		file_path = 'DISTANCE_AND_MAX_TIME.txt'
	elif FULL_PATH_PREDICT:
		file_path = 'FULL_PATH_PREDICT.txt'
	elif PRIORITY_QUEUE:
		file_path = 'PRIORITY_QUEUE.txt'
	elif MITT_EQUALS_DEST_CHECK:
		file_path = 'MITT_EQUALS_DEST_CHECK.txt'
	sys.stdout = open(file_path, "w")

	#Parametri per il calcolo del tempo
	robottino.tempo_inizializzazione = time.time()
	robottino.supercounter = 0

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
