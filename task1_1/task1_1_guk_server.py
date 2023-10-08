import socket
import datetime

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((socket.gethostname(), 12345))
server_socket.listen(5)

print('Server has started. Awaiting input...')

while True:
    client_socket, client_address = server_socket.accept()
    data = client_socket.recv(1024).decode('utf-8')
    print(f"Recieved: {data} from {client_socket.getsockname()}")

    client_socket.send(f'Message recieved'.encode('ascii'))
    print(f"Time of receiving: {datetime.datetime.now()}")

