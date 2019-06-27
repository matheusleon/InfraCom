import sys
import socket
import subprocess
import os
import argparse

limit = int(1500)
serverName = "localhost"

# Socket que esta mandando o pacote
# Address é o endereço de ip do dest
# act_ack é o numero de pacotes que eu ja mandei
# msg é a mensagem que eu vou mandar em representaçao binaria
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

# Socket que esta recebendo o pacote
# 
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
  return ans, expected_ack

def main():
    dnsName = "localhost"
    dnsPort = 2010

    while (True):
      # Comunicacao com DNS
      ############################
      while (True):
        act_ack = 0
        expected_ack = 0
        print('Informe o dominio com o qual deseja se conectar:')
        domainName = input()
        UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        UDPClientSocket.bind(('', 3000))
        act_ack = send(UDPClientSocket, (dnsName, dnsPort), act_ack, domainName.encode('ascii'))
        msgFromServer, expected_ack = recv(UDPClientSocket, expected_ack)
        ipAddress = msgFromServer.decode('ascii')
        if (ipAddress == 'Nao existe esse dominio'):
          print('Nao existe esse dominio, tente novamente.')
          continue
        serverAdress = (ipAddress, 2080)
        break
      ############################
      
      act_ack = 0
      expected_ack = 0
      while (True):
          print('Informe a opcao:')
          option = input()
          act_ack = send(UDPClientSocket, serverAdress, act_ack, option.encode('ascii'))
          if (option == "GET"):
              print('Digite o nome do arquivo:')
              filename = input()
              act_ack = send(UDPClientSocket, serverAdress, act_ack, filename.encode('ascii'))
              msg, expected_ack = recv(UDPClientSocket, expected_ack)
              msg = msg.decode('ascii')
              exist = msg
              if (exist == "YES"):
                  print('Arquivo recebido com sucesso!')
                  text, expected_ack = recv(UDPClientSocket, expected_ack)
                  with open(filename, 'wb') as newFile:
                      newFile.write(text)
              else:
                  print('Arquivo nao existe')
          elif (option == "LIST"):
              msg, expected_ack = recv(UDPClientSocket, expected_ack)
              files = msg.decode('ascii').split("#")
              print(files)
          elif (option == "CLOSE"):
              UDPClientSocket.close()
              break
          else:
              print('Opcao invalida')
    
    
    ############################

if __name__ == "__main__":
    sys.exit(main())
