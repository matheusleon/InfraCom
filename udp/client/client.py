import sys
import socket
import subprocess
import os
import argparse

def send(Socket, adress, act_ack, msg):
  adress = (adress[0], 2080)
  msg = str(act_ack) + ' ' + msg
  while (True):
    try:
      Socket.sendto(msg.encode('ascii'), adress)
      serverAnswer, lixo = Socket.recvfrom(1024)
      if (serverAnswer.decode('ascii') == '-'):
        act_ack += 1
        break
    except socket.timeout as e:
      continue
  return
  
def recv(Socket, expected_ack):
  confirma = '-'
  while (True):
    try:
      answer = Socket.recvfrom(1024)
      body = answer[0].decode('ascii')
      adress = answer[1]
      adress = (adress[0], 2080)
      this_ack, real_msg = body.split(' ', 1)
      this_ack = int(this_ack)
      if (this_ack != expected_ack):
        Socket.sendto(confirma.encode('ascii'), adress)
        continue
      else:
        Socket.sendto(confirma.encode('ascii'), adress)
        expected_ack += 1
        return real_msg
    except socket.timeout as e:
      continue
  return 'nunca deveria chegar aqui'

act_ack = 0
expected_ack = 0
serverName = "localhost"
serverPort = 2080
dnsName = "localhost"
dnsPort = 2001

def main():
    while (True):
      # Comunicacao com DNS
      ############################

      print('Informe o dominio com o qual deseja se conectar:')
      domainName = input()
      UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      UDPClientSocket.bind(('', 3000))
      UDPClientSocket.sendto(domainName.encode('ascii'), (dnsName, dnsPort))
      msgFromServer = UDPClientSocket.recvfrom(1024)
      ipAddress = msgFromServer[0].decode('ascii')
      
      #ipAddress = '127.0.0.1'
      
      print('IP que veio do DNS: ' + ipAddress)    
      
      serverAdress = (ipAddress, 2080)

      while (True):
          print('Informe a opcao:')
          option = input()
          send(UDPClientSocket, serverAdress, act_ack, option)
          if (option == "GET"):
              print('Digite o nome do arquivo:')
              filename = input()
              send(UDPClientSocket, serverAdress, act_ack, filename)
              msg = recv(UDPClientSocket, expected_ack)
              exist = msg
              if (exist == "YES"):
                  print('Arquivo recebido com sucesso!')
                  print('RECEBI DO SERVER:::: ' + msg)
                  text = recv(UDPClientSocket, expected_ack)
                  print('Recebi do server o texto: ' + text)
                  with open(filename, 'w') as newFile:
                      newFile.write(text)
              else:
                  print('Arquivo nao existe')
          elif (option == "LIST"):
              #msg = clientSocket.recv(1024).decode('ascii')
              msg = recv(UDPClientSocket, expected_ack)
              files = msg.split("#")
              print(files)
          elif (option == "CLOSE"):
              UDPClientSocket.close()
              break
          else:
              # INVALIDO  
              print('Opcao invalida')
    
    
    ############################

if __name__ == "__main__":
    sys.exit(main())
