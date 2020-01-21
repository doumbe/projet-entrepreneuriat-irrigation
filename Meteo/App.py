import json
import serial
import time
from MeteoReportWeb import *

# =============================================================================
# class App(object):
#   """ Classe Principale à executer qui construit un bulletin météo """
#   emw=ExtractMeteoWeb()
#   tableauFinal={}
#
#   def __init__(self):
#     """ Recupère la liste des intitulés et le tableau des donnees météo """
#     print("---INIT---")
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
  ser = serial.Serial(port='COM6',baudrate = 9600,parity=serial.PARITY_NONE,stopbits=serial.STOPBITS_ONE,bytesize=serial.EIGHTBITS,timeout=1)
  mrw=MeteoReportWeb()
  while 1:
    mrw.setMeteoReport()
    #mrw.afficheMeteoReport()
    #print()
    parsedJson = json.dumps(mrw.tableauFinal)
    #print(parsedJson)
    ser.write(parsedJson.encode("utf-8"))
    print("JSON envoyé")
    # On lit la ligne
    x = ser.readline()
    if x:
      x = x.rstrip()
      x = x.decode("utf-8")
      print(x)
    time.sleep(2)