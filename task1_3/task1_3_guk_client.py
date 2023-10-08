import socket

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((socket.gethostname(), 12345))

while True :
    message = input("Enter the message: ")

    if message == 'quit':
        break
    client_socket.send(message.encode('utf-8'))

client_socket.send(message.encode('utf-8'))

response = client_socket.recv(1024).decode('utf-8')
print(response)

client_socket.close()