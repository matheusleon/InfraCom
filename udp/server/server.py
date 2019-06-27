import sys
import itertools
import socket
import os
import glob
import subprocess
from socket import socket as Socket

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

def send(Socket, adress, act_ack, msg):
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
        Socket.sendto(packet, adress)
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
  adress = ('', -1)
  while (True):
    try:
      answer = Socket.recvfrom(limit)
      adress = answer[1]
      body = answer[0]
      flag_fim = body[0:1]
      this_ack = body[1:33]
      real_msg = body[33:]
      this_ack = int(this_ack, 2)

      if (this_ack != expected_ack):
        Socket.sendto(confirma, adress)
        continue
      else:
        Socket.sendto(confirma, adress)
        expected_ack += 1
        ans += real_msg
        if (flag_fim == b'1'):
          break
        else:
          continue
    except socket.timeout as e:
      continue
  return ans, adress, expected_ack

def main():

    dnsName = "localhost"
    dnsPort = 2010
    act_ack = 0
    expected_ack = 0
    
    # Comunicacao com o DNS
    ############################
    UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    UDPServerSocket.bind(('localhost', 2080))
    dnsAddress = (dnsName, dnsPort)
    domainName = input('Digite o dominio: ')
    ipAddress = input('Digite o endereco de IP: ')
    msg = domainName + ' ' + ipAddress
    print('Enviando pro DNS: ' + msg)
    act_ack = send(UDPServerSocket, dnsAddress, act_ack, msg.encode('ascii'))
    UDPServerSocket.close()
    ############################
    
    while (True):
      UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      UDPServerSocket.bind(('localhost', 2080))
      
      act_ack = 0
      expected_ack = 0
      while True:
          print('Server esta esperando a mensagem')
          option, clientAdress, expected_ack = recv(UDPServerSocket, expected_ack)
          option = option.decode('ascii')
          if not option:
              break
          if (option == "GET"):
              filename, clientAdress, expected_ack = recv(UDPServerSocket, expected_ack)
              filename = filename.decode('ascii')
              exist = os.path.exists(filename)
              if (exist):
                  act_ack = send(UDPServerSocket, clientAdress, act_ack, 'YES'.encode('ascii'))
                  f = open(filename, 'rb')
                  msg = f.read()
                  f.close()
                  act_ack = send(UDPServerSocket, clientAdress, act_ack, msg)
              else:
                  act_ack = send(UDPServerSocket, clientAdress, act_ack, 'NO'.encode('ascii'))
          elif (option == "LIST"):
              files = [f for f in glob.glob("*.*")]
              ans = ""
              for f in files:
                  if (f != "server.py"):
                    ans = ans + f + "#"
              if (len (files)):
                  ans = ans[:-1]
              act_ack = send(UDPServerSocket, clientAdress, act_ack, ans.encode('ascii'))
          elif (option == "CLOSE"):
              print('Fechando conexao com Client')
              break
          else:
              print('INVALIDO')      

    return 0

if __name__ == "__main__":
    sys.exit(main())

