from socket import *

with socket(AF_INET, SOCK_STREAM) as client:
    client.connect((gethostname(), 9999))
    msg = 'I am a client'
    client.send(msg.encode())
    full_msg = ''
    while True:
        msg = client.recv(10)
        if len(msg) <= 0:
            break
        else:
            full_msg += msg.decode()
    print(full_msg)
