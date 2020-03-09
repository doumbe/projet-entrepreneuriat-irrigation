# coding: utf-8
import pymongo
import json
import time
from ExtractMeteoWeb_online import *
#from ExtractMeteoWeb_local import *

class MeteoReportWeb(object):
  """ Classe qui construit un bulletin météo """
  emw=ExtractMeteoWeb()
  tableauJson={}
  tableauMongo=[]

  def __init__(self):
    """ Recupère la liste des intitulés et le tableau des donnees météo """
    print("---MeteoReportWeb---")
    self.intitules,self.donnees=self.emw.returnMeteoData()
    return

  def setMeteoReport(self):
    """ Compile les données et construit un bulletin météo heure par heure """
    #print("---setMeteoReport---")
    taille=len(self.intitules)
    self.horaires=[self.donnees[0][i]+' - '+self.donnees[1][i] for i in range(taille)]
    for j in range(taille):
      self.tableauJson[self.horaires[j]]={self.intitules[i]:self.donnees[i][j] for i in range(2,taille)}
    self.tableauMongo=[{"time":k,"data":v} for k,v in self.tableauJson.items()]
    return

  def afficheMeteoReport(self):
    """ Affiche le bulletin météo """
    #print("---afficheMeteoReport---")
    for H in self.horaires:
      print(H)
      for i,k in enumerate(self.tableauJson[H],2):
        print('--> '+self.intitules[i]+' : '+mrw.tableauJson[H][self.intitules[i]])
      print()
    return

if __name__ == '__main__':
  print("---MeteoReportWeb_MAIN---")
  while 1:
    mrw=MeteoReportWeb()
    mrw.setMeteoReport()
    mrw.afficheMeteoReport()
    print()
    parsedJson=json.dumps(mrw.tableauJson)
    #print(parsedJson)
    baseName="Agriculture"
    colName="meteo"
    client=pymongo.MongoClient()
    dbTest=client[baseName][colName]
    dbTest.insert_many(mrw.tableauMongo)
    time.sleep(60)