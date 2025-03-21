import socket
import threading

# Server configuration
HOST = '127.0.0.1'  # Localhost
PORT = 12345  # Port number

# Create a socket
server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.bind((HOST, PORT))
server.listen()

clients = []
nicknames = []

# Broadcast function to send messages to all clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handle communication with a client
def handle_client(client):
    while True:
        try:
            message = client.recv(1024)
            broadcast(message)
        except:
            index = clients.index(client)
            clients.remove(client)
            client.close()
            nickname = nicknames.pop(index)
            broadcast(f'{nickname} has left the chat!'.encode('utf-8'))
            break

# Accept new clients
def receive():
    while True:
        client, address = server.accept()
        print(f'Connected with {address}')
        
        client.send('NICK'.encode('utf-8'))
        nickname = client.recv(1024).decode('utf-8')
        nicknames.append(nickname)
        clients.append(client)

        print(f'Nickname: {nickname}')
        broadcast(f'{nickname} joined the chat!'.encode('utf-8'))
        client.send('Connected to the chat!'.encode('utf-8'))

        # Start a new thread for each client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()

print('Server is running...')
receive()

