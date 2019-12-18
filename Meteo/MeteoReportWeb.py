import json
from ExtractMeteoWeb_online import *
#from ExtractMeteoWeb_local import *

class MeteoReportWeb(object):
  emw=ExtractMeteoWeb()
  tableauFinal={}
  
  def __init__(self):
    print("---INIT---")
    self.intitules,self.donnees=self.emw.returnMeteoData()
    taille=len(self.intitules)
    self.horaires=[self.donnees[0][i]+' - '+self.donnees[1][i] for i in range(taille)]
    return

  def setMeteoReport(self):
    print("---setMeteoReport---")
    taille=len(self.intitules)
    for j in range(taille):
      self.tableauFinal[self.horaires[j]]={self.intitules[i]:self.donnees[i][j] for i in range(2,taille)}
    return

  def afficheMeteoReport(self):
    print("---afficheMeteoReport---")
    for H in self.horaires:
      print(H)
      for i,k in enumerate(self.tableauFinal[H],2):
        print('--> '+self.intitules[i]+' : '+mrw.tableauFinal[H][self.intitules[i]])
      print()
    return

if __name__ == '__main__':
  print("---MAIN---")
  mrw=MeteoReportWeb()
  mrw.setMeteoReport()
  mrw.afficheMeteoReport()
  print()
  parsedJson = json.dumps(mrw.tableauFinal)
  print(parsedJson)