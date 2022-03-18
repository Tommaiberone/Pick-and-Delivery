import errno
import socket

Database =  {   "Tommaso"   :   "Password_Tommaso",
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

    message = raw_input(" -> ")  # take input
    if message.lower().strip() == 'bye':
        print("Ricevuto il comando di arresto, chiudo la connessione...")

        try: client_socket.close()  # close the connection
        except socket.error as e:
            print ("Caught exception socket.error :", e)
        exit

    print("Mando il messaggio...")
    client_socket.send(message)  # send message
    print("Mandato")
    print("Aspetto una risposta...")

    while message.lower().strip() != 'bye':
        
        data = client_socket.recv(1024)  # receive response

        print('>>' + data)  # show in terminal

        if data == " -> ":
            message = raw_input("")  # again take input
            print("Mando il messaggio...")
            client_socket.send(message)  # send message
            print("Mandato")
            print("Aspetto una risposta...")



    print("Ricevuto il comando di arresto, chiudo la connessione...")

    try: client_socket.close()  # close the connection
    except socket.error as e:
        print ("Caught exception socket.error :", e)


if __name__ == '__main__':

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

    

    client_program()