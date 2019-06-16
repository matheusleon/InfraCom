import sys
import itertools
import socket
import os
import subprocess
from socket import socket as Socket

dnsName = "localhost"
dnsPort = 2010

def main():
    
    serverSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    # Comunicacao com o DNS
    ############################
    
    serverSocket.connect((dnsName,dnsPort))
    
    print('------------Conectou com o DNS')

    print('Digite o dominio e endereco de IP:')
    #domainName = input()
    #ipAddress = input()

    msg = "oi.com" + '#' + "123.456"
    print('Enviando pro DNS: ' + msg)
    serverSocket.send(msg.encode('ascii'))
    answer = serverSocket.recv(1024).decode('ascii')

    print('Recebi do DNS: ' + answer)

    serverSocket.close()
    ############################


    """
    serverClientSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    serverClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    #print('------------Conectou com o CLIENT')
    serverClientSocket.bind(('', 2080))
    serverClientSocket.listen(1)
    connection_socket = serverClientSocket.accept()[0]
    print('------------Conectou com o CLIENT')

    while True:
        request = connection_socket.recv(1024).decode('ascii')
        print('Recebi o dominio ' + request)
        if (request == "oi.com"):
            ans = '123.456'
            connection_socket.send(ans.encode('ascii'))
        
        if not request:
            break

    return 0
    """


if __name__ == "__main__":
    sys.exit(main())