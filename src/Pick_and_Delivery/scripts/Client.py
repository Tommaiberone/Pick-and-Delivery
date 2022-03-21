import errno
import socket
import time

DEBUG = True
SIZE = 1024

Database =  {   "Tommaso"   :   "Password_Tommaso",
                "T"         :   "T",
                "Filippo"   :   "Password_Filippo",
                "Federico"  :   "Password_Federico",
                "Luigi"     :   "Password_Luigi",
                "Andrea"    :   "Password_Andrea"
                }

def client_program():
    host = "localhost"  # as both code is running on same pc
    port = 12345  # socket server port number

    client_socket = socket.socket()  # instantiate
    client_socket.connect((host, port))  # connect to the server


    messaggio_da_inviare = ""
    while messaggio_da_inviare.lower().strip() != 'bye':
        
        messaggio_ricevuto = client_socket.recv(SIZE)  # receive response

        print('>>' + messaggio_ricevuto)  # show in terminal

        if messaggio_ricevuto == " -> ":
            
            messaggio_da_inviare = raw_input("")  # again take input
            client_socket.send(messaggio_da_inviare)  # send message

        time.sleep(.4)



    print("Ricevuto il comando di arresto, chiudo la connessione...")

    try: client_socket.close()  # close the connection
    except socket.error as e:
        print ("Caught exception socket.error :", e)


def check_user():

    username = ""

    while True :

        username = raw_input("Inserisci il tuo nome utente: ")

        if username not in Database.keys():
            print("Errore! Utente non registrato")
            continue
        
        password = raw_input("Inserisci la password: ")
        
        if (Database[username] != password):
            print("Errore! La password non combacia")
            continue
            
        print("Utente loggato correttamente")
        break

    return username

if __name__ == '__main__':

    username = check_user()   


    while True:

        print("Ciao", username, "vuoi inviare un pacchetto? [s/n]\n")
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
