import socket
import subprocess
import os
import argparse

serverName = "localhost"
serverPort = 2080

clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    clientSocket.connect((serverName, serverPort))
except Exception:
    pass

try: 
    while (True):
        print('Informe o dominio com o qual deseja se conectar:')
        domain = input()
        print('Enviando o dominio ' + domain)
        clientSocket.send(domain.encode())
        ip_address = clientSocket.recv(1024).decode('ascii')
        print('Recebi o IP ' + ip_address)
        

except KeyboardInterrupt:
    escape = True
except Exception:
    clientSocket.close()


clientSocket.close()