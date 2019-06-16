import sys
import itertools
import socket
import os
import glob
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
    domainName = input()
    ipAddress = input()

    #msg = "oi.com" + '#' + "123.456"
    msg = domainName + '#' + ipAddress
    print('Enviando pro DNS: ' + msg)
    serverSocket.send(msg.encode('ascii'))
    answer = serverSocket.recv(1024).decode('ascii')

    print('Recebi do DNS: ' + answer)

    serverSocket.close()
    ############################

    
    
    serverClientSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
    serverClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    serverClientSocket.bind(('', 2080))
    serverClientSocket.listen(1)
    connection_socket = serverClientSocket.accept()[0]
    print('------------Conectou com o CLIENT')

    while True:
        option = connection_socket.recv(1024).decode('ascii')
        print('OPCAO E:' + option)
        if not option:
            break
        if (option == "GET"):
            filename = connection_socket.recv(1024).decode('ascii')
            print('NOME DO ARQUIVO ' + filename)
            exist = os.path.exists(filename)
            if (exist):
                connection_socket.send('YES#'.encode('ascii'))
                f = open(filename, 'r')
                msg = f.read().encode('ascii')
                f.close()
                connection_socket.send(msg)
            else:
                connection_socket.send('NO#'.encode('ascii'))
            
        elif (option == "LIST"):
            files = [f for f in glob.glob("*.txt")]
            ans = ""
            for f in files:
                ans = ans + f + "#"
            print(ans)
            if (len (files)):
                ans = ans[:-1]
            print(ans)
            connection_socket.send(ans.encode('ascii'))
        elif (option == "CLOSE"):
            print('Fechando conexao com Client')
        else:
            print('INVALIDO')
            # INVALIDO        

    return 0

if __name__ == "__main__":
    sys.exit(main())