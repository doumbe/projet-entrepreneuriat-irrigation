# coding: utf-8
import json
import socket
import sys
from MeteoReportWeb import *

# =============================================================================
# class ServerTCP(object):
#   """ Classe Principale à executer qui construit un bulletin météo """
#   emw=ExtractMeteoWeb()
#   tableauFinal={}
#   
#   def __init__(self, host, port):
#     """ Recupère la liste des intitulés et le tableau des donnees météo """
#     #print("---INIT---")
#     self.intitules,self.donnees=self.emw.returnMeteoData()
#     return
# 
#   def setMeteoReport(self):
#     """ Compile les données et construit un bulletin météo heure par heure """
#     print("---setMeteoReport---")
#     taille=len(self.intitules)
#     self.horaires=[self.donnees[0][i]+' - '+self.donnees[1][i] for i in range(taille)]
#     for j in range(taille):
#       self.tableauFinal[self.horaires[j]]={self.intitules[i]:self.donnees[i][j] for i in range(2,taille)}
#     return
# 
#   def afficheMeteoReport(self):
#     """ Affiche le bulletin météo """
#     print("---afficheMeteoReport---")
#     for H in self.horaires:
#       print(H)
#       for i,k in enumerate(self.tableauFinal[H],2):
#         print('--> '+self.intitules[i]+' : '+mrw.tableauFinal[H][self.intitules[i]])
#       print()
#     return
# =============================================================================

if __name__ == '__main__':
  print("---MAIN---")
  #mrw=MeteoReportWeb()
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
          connection.sendall(data)
        else:
          print('no data from', client_address)
          break
    finally:
      connection.close()
  #mrw.setMeteoReport()
  #mrw.afficheMeteoReport()
  #print()
  #parsedJson = json.dumps(mrw.tableauFinal)
  #print(parsedJson)
