# coding: utf-8
import json
import socket
import sys
from MeteoReportWeb import *

# =============================================================================
""" Classe Principale à executer """
# =============================================================================

if __name__ == '__main__':
  print("---MAIN---")
  mrw=MeteoReportWeb()
  mrw.setMeteoReport()
  #mrw.afficheMeteoReport()
  #print()
  parsedJson = json.dumps(mrw.tableauFinal)
  print(parsedJson)
  sock=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  server_address = ('localhost', 10000)
  print('Starting up on {} port {}'.format(*server_address))
  sock.bind(server_address)
  sock.listen(1)
  while True:
    print("Attente d'une connexion")
    connection, client_address = sock.accept()
    try:
      print('connection from', client_address)
      while True:
        data = connection.recv(16)
        print('received {!r}'.format(data))
        if data:
          print('sending data back to the client')
          connection.sendall(parsedJson)
        else:
          print('no data from', client_address)
          break
    finally:
      connection.close()
