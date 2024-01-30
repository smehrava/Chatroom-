import socket
import threading

# Lists For Clients and Their names
# clients = []
names = []

# Sending Messages To All Connected Clients
def broadcast(message):
    for client in clients:
        client.send(message)

# Handling Messages From Clients
def handle_client(client):
    while True:
        try:
            # Broadcasting Messages to all clients
            message = client.recv(1024)
            broadcast(message)
            print(message)
        except:
            # Removing And Closing Clients in exception
            index = clients.index(client)
            clients.remove(client)
            client.close()
            name = names[index]
            broadcast('{} is not in the chat anymore!'.format(name).encode('ascii'))
            names.remove(name)
            break


def run(serverSocket, serverPort):
    global server
    server = serverSocket
    while True:
        # Accept Connection
        client, address = server.accept()
        print("Connected with {}".format(str(address)))

        # Request And Store name of the client
        name = client.recv(1024).decode('ascii')
        names.append(name)
        clients.append(client)

        # Print name of the client who has joined and then broadcast it to all clients so everyone knows this client has joined server
        print("name is {}".format(name))
        broadcast("{} joined the server on port {}!".format(name,serverPort).encode('ascii'))
        client.send('Connected to server on server port!'.encode('ascii'))

        # Handling thread for client
        thread = threading.Thread(target=handle_client, args=(client,))
        thread.start()


# **Main Code**:
#this part was already given to us through template.
if __name__ == "__main__":
    server_port = 9301
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Creating a TCP socket.
    server_socket.bind(('127.0.0.1', server_port))
    server_socket.listen(3)


    clients = []  # List to add the connected client sockets
    run(server_socket, server_port)  # Calling the function to start the server.
