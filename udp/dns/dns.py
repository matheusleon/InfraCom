import sys
import itertools
import socket
import os
import subprocess
from socket import socket as Socket

map = {}

limit = int(1500)

def transform_int(value):
  pot = int(2**31)
  cur = b''
  while (pot > 0):
    if (value >= pot):
      value -= pot
      cur = cur + b'1'
    else:
      cur = cur + b'0'
    pot = pot // 2
  return cur

def send(Socket, address, act_ack, msg):
  packs = []
  while (len(msg) > 0):
    preff_size = min(limit - 33, len(msg))
    cur_ack = act_ack + len(packs)
    cur_ack = transform_int(cur_ack)
    packs.append(cur_ack + msg[0 : preff_size])
    msg = msg[preff_size:]
    if (len(msg) == 0):
      packs[-1] = b'1' + packs[-1]
    else:
      packs[-1] = b'0' + packs[-1]
    
  for packet in packs:
    while (True):
      try:
        Socket.sendto(packet, address)
        serverAnswer, lixo = Socket.recvfrom(1)
        if (serverAnswer == b'1'):
          act_ack += 1
          break
      except socket.timeout as e:
        continue
        
  return act_ack

def recv(Socket, expected_ack):
  confirma = b'1'
  ans = b''
  address = ('', -1)
  while (True):
    try:
      answer = Socket.recvfrom(limit)
      address = answer[1]
      body = answer[0]
      flag_fim = body[0:1]
      this_ack = body[1:33]
      real_msg = body[33:]
      this_ack = int(this_ack, 2)

      if (this_ack != expected_ack):
        Socket.sendto(confirma, address)
        continue
      else:
        Socket.sendto(confirma, address)
        expected_ack += 1
        ans += real_msg
        if (flag_fim == b'1'):
          break
        else:
          continue
    except socket.timeout as e:
      continue
  return ans, address, expected_ack

def main():
    
    UDPDNSSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPDNSSocket.bind(('localhost', 2010))
    act_ack = 0
    expected_ack = 0

    # Comunicacao com o server
    ############################
    msg, serverAddress, expected_ack = recv(UDPDNSSocket, expected_ack)
    domainName, ipAddress = msg.decode('ascii').split(" ")
    print('Recebi do SERVER o dominio: ' + domainName)
    print('Recebi do SERVER o IP: ' + ipAddress)
    map[domainName] = ipAddress
    ############################

    # Comunicacao com o Client
    ##########################
    while(True):
        act_ack = 0
        expected_ack = 0
        domainName, address, expected_ack = recv(UDPDNSSocket, expected_ack)
        domainName = domainName.decode('ascii')
        print('Recebi do Client: ' + domainName + ' ' + str(address))
        if not domainName:
            break
        if (domainName in map):
            msg = map.get(domainName)
        else:
            msg = 'Nao existe esse dominio'
        act_ack = send(UDPDNSSocket, address, act_ack, msg.encode('ascii'))
    ############################
    
if __name__ == "__main__":
    sys.exit(main())
