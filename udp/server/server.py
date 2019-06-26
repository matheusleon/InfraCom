import sys
import itertools
import socket
import os
import glob
import subprocess
from socket import socket as Socket

dnsName = "localhost"
dnsPort = 2010

def send(Socket, adress, act_ack, msg):
  adress = (adress[0], 3000)
  msg = str(act_ack) + ' ' + msg
  print(str(adress))
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
      adress = (adress[0], 3000)
      this_ack, real_msg = body.split(' ', 1)
      this_ack = int(this_ack)
      if (this_ack != expected_ack):
        Socket.sendto(confirma.encode('ascii'), adress)
        continue
      else:
        Socket.sendto(confirma.encode('ascii'), adress)
        expected_ack += 1
        return real_msg, adress
    except socket.timeout as e:
      continue
  return 'nunca deveria chegar aqui'

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
    #serverSocket.send(domainName.encode('ascii'))
    #serverSocket.send(ipAddress.encode('ascii'))
    answer = serverSocket.recv(1024).decode('ascii')

    print('Recebi do DNS: ' + answer)

    serverSocket.close()
    ############################
    
    act_ack = 0
    expected_ack = 0

    
    while (True):
      UDPServerSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      UDPServerSocket.bind(('localhost', 2080))
      while True:
          print('Server esta esperando a mensagem')
          option, clientAdress = recv(UDPServerSocket, expected_ack)
          print('OPCAO E:' + option)
          if not option:
              break
          if (option == "GET"):
              filename, clientAdress = recv(UDPServerSocket, expected_ack)
              print('NOME DO ARQUIVO ' + filename)
              exist = os.path.exists(filename)
              if (exist):
                  send(UDPServerSocket, clientAdress, act_ack, 'YES')
                  f = open(filename, 'r')
                  msg = f.read()
                  f.close()
                  send(UDPServerSocket, clientAdress, act_ack, msg)
              else:
                  send(UDPServerSocket, clientAdress, act_ack, 'NO')
          elif (option == "LIST"):
              files = [f for f in glob.glob("*.txt")]
              ans = ""
              for f in files:
                  ans = ans + f + "#"
              print(ans)
              if (len (files)):
                  ans = ans[:-1]
              print(ans)
              #connection_socket.send(ans.encode('ascii'))
              send(UDPServerSocket, clientAdress, act_ack, ans)
          elif (option == "CLOSE"):
              print('Fechando conexao com Client')
              break
          else:
              print('INVALIDO')
              # INVALIDO        

    return 0

if __name__ == "__main__":
    sys.exit(main())

