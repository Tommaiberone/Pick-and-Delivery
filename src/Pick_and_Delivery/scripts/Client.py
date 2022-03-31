import socket
import time

DEBUG = False
CHATTY = True
SIZE = 1024

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

#Fa effettuare il login all'utente e lo mette in comunicazione con il server
if __name__ == '__main__':

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
