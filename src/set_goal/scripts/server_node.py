# import socket programming library
import socket

# import thread module
from _thread import *
import threading

print_lock = threading.Lock()

# thread function
def threaded(client_socket):

	while True:

		# data received from client
		data = client_socket.recv(1024)
		if not data:
			print('Bye')
			
			# lock released on exit
			print_lock.release()
			break

		# reverse the given string from client
		data = data[::-1]

		# send back reversed string to client
		client_socket.send(data)

	# connection closed
	client_socket.close()


def Main():

	host = "prova"
	port = 12345
	server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_socket.bind((host, port))
	print("socket binded to port", port)

	# put the socket into listening mode
	server_socket.listen(5)
	print("socket is listening")

	# a forever loop until client wants to exit
	while True:

		# establish connection with client
		client_socket, client_addr = server_socket.accept()

		# lock acquired by client
		print_lock.acquire()
		print('Connected to :', client_addr[0], ':', client_addr[1])

		# Start a new thread and return its identifier
		start_new_thread(threaded, (client_socket,))
	s.close()


if __name__ == '__main__':
	Main()
