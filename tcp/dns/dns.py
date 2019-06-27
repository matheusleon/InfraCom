import sys
import itertools
import socket
import os
import subprocess
from socket import socket as Socket

map = {}

def main():

  UDPDNSSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
  UDPDNSSocket.bind(('localhost', 2010))

  # Comunicacao com o server
  #########################
  msg = UDPDNSSocket.recvfrom(1024)[0]
  domainName, ipAddress = msg.decode('ascii').split(" ")
  print('Recebi do SERVER o dominio: ' + domainName)
  print('Recebi do SERVER o IP: ' + ipAddress)
  map[domainName] = ipAddress
  #########################


  # Comunicacao com o Client

  while(True):
    bytesAddressPair = UDPDNSSocket.recvfrom(1024)
    domainName = bytesAddressPair[0].decode('ascii')
    address = bytesAddressPair[1]
    print('Recebi do Client: ' + domainName)
    if not domainName:
      break
    if (domainName in map):
      msg = "YES#" + map.get(domainName)
    else:
      msg = "NO#Nao existe esse dominio"
    UDPDNSSocket.sendto(msg.encode('ascii'), address)

  
if __name__ == "__main__":
  sys.exit(main())
