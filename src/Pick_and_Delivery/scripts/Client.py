import socket
import time
import threading

DEBUG = False
CHATTY = True
SIZE = 1024
AUTO_CHECK = True
N = 5

Database =  {   "Tommaso"   :   "Password_Tommaso",
                "T"         :   "T",
                "Filippo"   :   "Password_Filippo",
                "Federico"  :   "Password_Federico",
                "Luigi"     :   "Password_Luigi",
                "Andrea"    :   "Password_Andrea"
                }


#Si occupa della connessione con il server:
#Riceve o invia messaggi a seconda del comportamento del server
def client_program():

    #imposto host e porta di connessione con il server
    host = "localhost" 
    port = 12345

    #Istanzio la socket e mi connetto al server
    client_socket = socket.socket()  
    client_socket.settimeout(3000)
    client_socket.connect((host, port))


    messaggio_da_inviare = ""
    while messaggio_da_inviare.lower().strip() != 'bye':
        
        #Ricevo un messaggio dalla socket connessa al server
        messaggio_ricevuto = client_socket.recv(SIZE)

        #Check che verifica che la connessione non si sia interrotta
        #e che quindi il messaggio sia stato ricevuto correttamente.
        #Altrimenti interrompe l'esecuzione del programma
        if (not messaggio_ricevuto):
            print("La recv si e' bloccata!\n")
            try: client_socket.close()
            except socket.error as e: print ("Caught exception socket.error :", e)
            exit(0)

        #Printa nel terminale il messaggio ricevuto dal server
        print('>>' + messaggio_ricevuto)

        #Accetta un input dall'utente se il server si predispone
        #in modalita' di "ascolto"
        if messaggio_ricevuto == " -> ":    

            messaggio_da_inviare = raw_input("")
            client_socket.send(messaggio_da_inviare)


        #Chiude la connessione con il server se riceve il messaggio di chiusura
        elif messaggio_ricevuto == "Arrivederci e grazie per aver usato il nostro servizio!":

            if DEBUG: print("Ricevuto il comando di arresto, chiudo la connessione...")
            try: client_socket.close()
            except socket.error as e:
                print ("Caught exception socket.error :", e)
            break

        time.sleep(.4)


#Controlla che l'utente sia registrato al servizio
def check_user():

    username = ""

    while True :

        username = raw_input("Inserisci il tuo nome utente: ")

        #Check Username
        if username not in Database.keys():
            print("Errore! Utente non registrato")
            continue
        
        password = raw_input("Inserisci la password: ")
        
        #Check Password
        if (Database[username] != password):
            print("Errore! La password non combacia")
            continue
            
        print("Utente loggato correttamente")
        break

    return username    

#una versione modificata di client program che
# non richiede all'utente di mandare il proprio nome

#   Fa recv a caso per far andare avanti il server finche' non riceve " -> "
#   Allora manda il nome del mittente
#   Di nuovo continua a fare recv finche' non riceve " -> "
#   Allora manda il nome del destinatario
def auto_client_program(nome_mittente, nome_destinatario): #Aggiungere forse peso pacchetto?

    #imposto host e porta di connessione con il server
    host = "localhost" 
    port = 12345

    #Istanzio la socket e mi connetto al server
    client_socket = socket.socket()  
    client_socket.settimeout(3000)
    client_socket.connect((host, port))

    messaggio_da_inviare = ""

    i=0

    while True:
        
        #Ricevo un messaggio dalla socket connessa al server
        messaggio_ricevuto = client_socket.recv(SIZE)

        #Check che verifica che la connessione non si sia interrotta
        #e che quindi il messaggio sia stato ricevuto correttamente.
        #Altrimenti interrompe l'esecuzione del programma
        if (not messaggio_ricevuto):
            print("La recv si e' bloccata!\n")
            exit(0)

        #Accetta un input dall'utente se il server si predispone
        #in modalita' di "ascolto"
        elif messaggio_ricevuto == " -> ":

            #La prima volta manda il nome del mittente
            if i == 0:    
                client_socket.send(nome_mittente)

            #La seconda manda il nome del destinatario    
            elif i==1:
                client_socket.send(nome_destinatario)
                print("Io {} sono in coda con un pacchetto per {}. Mi disconnetto.\n".format(nome_mittente, nome_destinatario))
                try: client_socket.close()
                except socket.error as e:
                    print ("Caught exception socket.error :", e)
                break
                
            i+=1

        #Chiude la connessione con il server se riceve il messaggio di chiusura
        elif messaggio_ricevuto == "Arrivederci e grazie per aver usato il nostro servizio!":

            if DEBUG: print("Ricevuto il comando di arresto, chiudo la connessione...")
            try: client_socket.close()
            except socket.error as e:
                print ("Caught exception socket.error :", e)
            break


# Chiama N volte la funzione auto_client_program() dandogli in input il nome del
# richiedente e il nome del destinatario del pacchetto presenti in un dizionario appositamente creato
#    Il dizionario sarebbe una lista di Mittente - Destinatario che possa sfruttare tutte le funzionalita' dei paradigmi

def clients_spawner():

    clients =   [   
                    ["Tommaso"  ,   "Filippo"   , 20],
                    ["Federico" ,   "Carlo"     , 5],
                    ["Luigi"    ,   "Carlo"     , 22],
                    ["Filippo"  ,   "Tommaso"   , 5],
                    ["Carlo"    ,   "Federico"  , 15],
                    ["Tommaso"  ,   "Luigi"     , 27],
                    ["Filippo"  ,   "Federico"  , 52],
                    ["Peppe"    ,   "Bianca"    , 1],
                    ["Francesco",   "Massimo"   , 3],
                    ["Federico" ,   "Luigi"     , 34],
                    ["Bianca"   ,   "Federico"  , 15],
                    ["Pietro"   ,   "Carlo"     , 23],
                    ["Tommaso"  ,   "Bianca"    , 2],
                    ["Filippo"  ,   "Carlo"     , 51],
                    ["Federico" ,   "Peppe"     , 23],
                    ["Massimo"  ,   "Francesco" , 14],
                    ["Francesco",   "Bianca"    , 2],
                    ["Tommaso"  ,   "Federico"  , 42],
                    ["Filippo"  ,   "Tommaso"   , 13],
                    ["Peppe"    ,   "Bianca"    , 22],
                    ["Federico" ,   "Bianca"    , 28],
                    ["Carlo"    ,   "Luigi"     , 2],
                    ["Filippo"  ,   "Peppe"     , 52],
                    ["Peppe"    ,   "Carlo"     , 9],
                    ["Luigi"    ,   "Tommaso"   , 18],
                    ["Bianca"   ,   "Carlo"     , 12],
                    ["Luigi"    ,   "Massimo"   , 5],
                    ["Peppe"    ,   "Federico"  , 8]
                ]

    for tupla in clients:
        nome_mittente = tupla[0]
        nome_destinatario = tupla[1]
        tempo_di_attesa = tupla[2]

        threading.Thread(target = auto_client_program,args = (nome_mittente, nome_destinatario, )).start()
        time.sleep(tempo_di_attesa)

    return

#Fa effettuare il login all'utente e lo mette in comunicazione con il server
if __name__ == '__main__':

    if AUTO_CHECK == True:
        clients_spawner()
        exit()

    #Effettua il check dell'utente
    username = check_user()   

    #Si accerta che l'utente voglia inviare un pacchetto
    while True:
        
        print("Ciao {}, vuoi inviare un pacchetto? [s/n]".format(username))
        message = raw_input(" -> ")

        if message.lower().strip() == 'n':
            print("Ok, allora passo e chiudo!\n")
            break

        elif message.lower().strip() == 's':
            print("Ok, ti metto in comunicazione con il server...\n")
            client_program()
            break    

        else:
            print("Non ho capito, ripeti per favore:\n")
