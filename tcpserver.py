from socket import *

# create server
with socket(AF_INET, SOCK_STREAM) as server:
    # Bind server
    server.bind((gethostname(), 9999))
    # Listen
    server.listen(5)
    while True:
        # Accept connection
        clientSock, addr = server.accept()
        # Receive msg
        msg = clientSock.recv(15).decode()
        newMsg = 'Hello to our server, hope our service helps you'
        clientSock.send(newMsg.encode())
        clientSock.close()
