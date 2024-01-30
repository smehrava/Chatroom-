import argparse
import socket
import threading

def receive_messages(clientSocket):
    while True:
        try:
            #receiving message from server
            data, addr = clientSocket.recvfrom(1024)
            #printing the message
            print(data.decode())
        except:
            # in case client has just joined and hasnt received any message yet print this;
            print("first message, nothing to share yet")

def run(clientSocket, clientname, serverAddr, serverPort):
    #sending the name of client to server
    clientSocket.sendto(f"Name_of_client: {clientname}".encode(), (serverAddr, serverPort))
    while True:
        #asking client to enter a message
        message = input(f"{clientname}, enter your message: \n")
        full_message = f"{clientname}: {message}"
        #specifying a condition where if client types in Q or q then they wanna get out of server
        if message.lower() == "q":
            exit()
        else:
            #otherwise, sending the message to server
            clientSocket.sendto(full_message.encode(), (serverAddr, serverPort))

#this part was already given in the template except for threading part. I added threading
#added threading for each function
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='argument parser')
    parser.add_argument('name')  # to use: python udp_client.py username
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)  # Creating a UDP socket.

    tRun = threading.Thread(target=run, args=(clientSocket, clientname, serverAddr, serverPort))
    tReceive = threading.Thread(target=receive_messages, args=(clientSocket, ))

    tRun.start()
    tReceive.start()

