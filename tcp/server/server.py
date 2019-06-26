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
  
  # Comunicacao com o DNS
  serverSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
  serverSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  serverSocket.connect((dnsName,dnsPort))
  
  print('------------Conectou com o DNS')

  print('Digite o dominio:')
  domainName = input()
  print('Digite o endereco de IP:')
  ipAddress = input()

  msg = domainName + '#' + ipAddress
  serverSocket.send(msg.encode('ascii'))

  serverSocket.close()
  

  # Comunicacao com o Client
  serverClientSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
  serverClientSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
  
  serverClientSocket.bind(('', 2080))
  serverClientSocket.listen(1)
  connection_socket = serverClientSocket.accept()[0]
  print('Conectou com o CLIENT')

  while True:
    option = connection_socket.recv(1024).decode('ascii')
    if not option:
      break
    if (option == "GET"):
      filename = connection_socket.recv(1024).decode('ascii')
      exist = os.path.exists(filename)
      if (exist):
        connection_socket.send(b"1")
        f = open(filename, 'rb')
        msg = f.read()
        f.close()
        connection_socket.send(msg)
      else:
        connection_socket.send(b"0")
      
    elif (option == "LIST"):
      files = [f for f in glob.glob("*.*")]
      ans = ""
      for f in files:
        if (f != "server.py"):
          ans = ans + f + "#"
      if (len (files)):
        ans = ans[:-1]
      connection_socket.send(ans.encode('ascii'))
    elif (option == "CLOSE"):
      print('Fechando conexao com Client')
    else:
      print('Opcao invalida')

  return 0

if __name__ == "__main__":
  sys.exit(main())