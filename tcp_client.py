from socket import *
import argparse
import threading

#
def run(clientSocket, clientname):
    while True:
        #asking from client to enter their message
        originalMessage = input(f'{clientname}, enter your message: \n')
        #modifying the message so that it contains clients name inside it
        message_to_send = f"{clientname}: {originalMessage}"
        #specifying a condition where if client types in Q or q then they wanna get out of server
        if originalMessage.lower() == "q":
            exit()
        # if the message isnt q or Q, then clients message is sent to server
        else:
            clientSocket.send(message_to_send.encode())

#
def receive():
    while True:
        try:
            #decoding the message that has been received
            message = clientSocket.recv(1024).decode('ascii')
            print(message)
        except:
            print("an error has been occurred.")
            clientSocket.close()
            break


#most of this code was given in the template, I added threading to it
if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Argument Parser')
    parser.add_argument('name')  # to use: python tcp_client.py username
    args = parser.parse_args()
    clientname = args.name
    serverAddr = '127.0.0.1'
    serverPort = 9301

    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((serverAddr, serverPort))

    #having thread for both functions I have
    threadRun = threading.Thread(target=run, args= (clientSocket, clientname))
    threadRun.start()

    threadRec = threading.Thread(target=receive)
    threadRec.start()


    run(clientSocket, clientname)



