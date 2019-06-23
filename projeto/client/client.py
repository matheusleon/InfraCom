import socket
import subprocess
import os
import argparse

serverName = "localhost"
serverPort = 2080

dnsName = "localhost"
dnsPort = 2001

try:
    while (True):
      # Comunicacao com DNS
      ############################

      print('Informe o dominio com o qual deseja se conectar:')
      domainName = input()
      UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      UDPClientSocket.sendto(domainName.encode('ascii'), (dnsName, dnsPort))
      msgFromServer = UDPClientSocket.recvfrom(1024)
      ipAddress = msgFromServer[0].decode('ascii')
      print('IP que veio do DNS: ' + ipAddress)    
      ############################
    
      # Comunicacao com SERVER
      ############################
      clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
      clientSocket.connect((ipAddress, serverPort))

      while (True):
          print('Informe a opcao:')
          option = input()
          clientSocket.send(option.encode('ascii'))
          if (option == "GET"):
              print('Digite o nome do arquivo:')
              filename = input()
              clientSocket.send(filename.encode('ascii'))
              msg = clientSocket.recv(1024).decode('ascii')
              exist, text = msg.split("#", 1)
              if (exist == "YES"):
                  print('Arquivo recebido com sucesso!')
                  print('RECEBI DO SERVER:::::; ' + msg)
                  text = clientSocket.recv(1024).decode('ascii')
                  print('Recebi do server o texto: ' + text)
                  with open(filename, 'w') as newFile:
                      newFile.write(text)
              else:
                  print('Arquivo nao existe')
          elif (option == "LIST"):
              msg = clientSocket.recv(1024).decode('ascii')
              files = msg.split("#")
              print(files)
          elif (option == "CLOSE"):
              clientSocket.close()
              break
          else:
              # INVALIDO  
              print('Opcao invalida')
    
    
    ############################


except KeyboardInterrupt:
    escape = True
#except Exception:
#    clientSocket.close()


#clientSocket.close()
