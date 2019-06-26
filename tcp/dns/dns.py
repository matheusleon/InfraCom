import sys
import itertools
import socket
import os
import subprocess
from socket import socket as Socket

map = {}

def main():

  # Comunicacao com o server
  dnsSocket = Socket(socket.AF_INET, socket.SOCK_STREAM)
  dnsSocket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)

  dnsSocket.bind(('', 2010))
  dnsSocket.listen(1)

  print('------------Conectou com o SERVER')
  connection_socket = dnsSocket.accept()[0]

  msg = connection_socket.recv(1024).decode('ascii')
  domainName, ipAddress = msg.split("#")

  map[domainName] = ipAddress

  dnsSocket.close()


  # Comunicacao com o Client
  UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  UDPServerSocket.bind(('localhost', 2001))

  while(True):
    bytesAddressPair = UDPServerSocket.recvfrom(1024)
    domainName = bytesAddressPair[0].decode('ascii')
    address = bytesAddressPair[1]
    print('Recebi do Client: ' + domainName)
    if not domainName:
      break
    if (domainName in map):
      msg = "YES#" + map.get(domainName)
    else:
      msg = "NO#Nao existe esse dominio"
    UDPServerSocket.sendto(msg.encode('ascii'), address)

  
if __name__ == "__main__":
  sys.exit(main())