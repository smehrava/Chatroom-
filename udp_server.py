import queue
import threading
import socket

#making a queue to contain all messages
messageQueue = queue.Queue()
clients = []

def receive():
    while True:
        try:
            #recieving message from client
            message, addr = serverSocket.recvfrom(1024)
            #putting the message inside our queue
            messageQueue.put((message, addr))
        #handling exceptions if occurred
        except Exception as e:
            print("Error:", e)

def run(serverSocket, serverPort):
    print(f'UDP server is listening on port {serverPort}')
    while True:
        #making sure the message queue contains a message
        while not messageQueue.empty():
            #getting the message from the queue
            message, addr = messageQueue.get()
            #printing the message on server
            print(message.decode())

            #if the client is not already there, we add it to our clients list
            if addr not in clients:
                clients.append(addr)
            for client in clients:
                try:
                    #seperating clients name from rest of the message
                    if message.decode().startswith("Name_of_client:"):
                        clientName = message.decode().split(":", 1)  # Use "1" to split once at the first occurrence
                        clientName = clientName[1]
                        #sending a message to that client saying it has succesfully joined the server.
                        serverSocket.sendto(f"{clientName} joined!\n".encode(), client)
                    else:
                        #broadcasting the message to other clients
                        for other_client in clients:
                            if other_client != client:
                                serverSocket.sendto(message, other_client)

                except:
                    clients.remove(client)

#this part was already given in the template except for threading part. I added threading
if __name__ == "__main__":
    serverPort = 9301
    serverSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.
    serverSocket.bind(('127.0.0.1', serverPort))
    t1 = threading.Thread(target=receive)
    t2 = threading.Thread(target=run, args=(serverSocket, serverPort))
    t1.start()
    t2.start()
