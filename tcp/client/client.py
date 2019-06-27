import sys
import socket
import subprocess
import os
import argparse

serverName = "localhost"
serverPort = 2080

dnsName = "localhost"
dnsPort = 2010

def print_menu():
  print('Os comandos disponiveis sao:')
  print('GET nome_do_arquivo para solicitar um arquivo do servidor')
  print('LIST para listar todos os arquivos no diretorio do servidor')
  print('CLOSE para encerrar a conexão com este servidor')

def main():
  
  while (True):
    # Comunicacao com DNS
    while (True):
      print('Informe o dominio com o qual deseja se conectar:')
      domainName = input()

      UDPClientSocket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
      UDPClientSocket.sendto(domainName.encode('ascii'), (dnsName, dnsPort))

      msgFromServer = UDPClientSocket.recvfrom(1024)
      msg = msgFromServer[0].decode('ascii')
      exist, ipAddress = msg.split('#')
      if (exist == "YES"):
        # print('IP que veio do DNS: ' + ipAddress)
        break
      else:
        print('Nao existe registro desse dominio')


    # Comunicacao com SERVER
    clientSocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    clientSocket.connect((ipAddress, serverPort))

    print('Conectou com o SERVER')
    print_menu()
    while (True):
      print('Digite a opcao desejada')
      option = input()
      clientSocket.send(option.encode('ascii'))
      if (option == "GET"):
        print('Digite o nome do arquivo:')
        filename = input()
        clientSocket.send(filename.encode('ascii'))
        exist = clientSocket.recv(1).decode('ascii')
        print('Enviando requisicao ao servidor:')
        if (exist == "1"):
          myfile = open(filename, 'wb')
          
          data = clientSocket.recv(int(1e8))
          myfile.write(data)
          myfile.close()
          print('Arquivo recebido com sucesso!')

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
        print('Opcao invalida')
      

if __name__ == "__main__":
  sys.exit(main())
