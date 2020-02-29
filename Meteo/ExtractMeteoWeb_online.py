# coding: utf-8
from bs4 import BeautifulSoup
import json
import requests

class ExtractMeteoWeb(object):
  """ Classe de récupération (scraping) et d'extraction (parsing) de données d'un site Web """
  intitules=[]
  donnees=[]
  tableauFinal={}

  def __init__(self):
    """ Initialise l'URL de la page Web des previsions météo """
    #print("---INIT---")
    self.url = 'https://www.lameteoagricole.net/meteo-heure-par-heure/Nice-06000.html'
    return

  def getData(self):
    """ Recupère le code source de la page Web """
    #print("---GETDATA---")
    html = requests.get(self.url).text
    return html

  def transformData(self,html):
    """ Extrait le tableau des prévisions météo du code source """
    #print("---TRANSFORMDATA---")
    #print("--> part 1")
    f1=html.find("<table id=\"meteoIntit\">") # Cherche la position de la string balise <table> sur la page html
    f2=html.find("</table>",f1) # Cherche la fin du tableau a partir de f1
    #print(f1,f2)
    html2=html[f1:f2+8] # Extraire le tableau
    #print(html)
    html2=html2.replace("<br />","") # Supprime les sauts de ligne
    #print(html2)
    self.soup1 = BeautifulSoup(html2, 'lxml') # Transforme la string en objet arborescence XML

    #print("--> part 2")
    f1=html.find("<table id=\"meteoHour\">")
    f2=html.find("</table>",f1)
    #print(f1,f2)
    html2=html[f1:f2+8]
    #print(html)
    html2=html2.replace("<br />","").replace("<i>","").replace("</i>","")
    #print(html2)
    self.soup2 = BeautifulSoup(html2, 'html5lib')
    return

  def parseList1(self):
    """ Construit la liste des intitulés """
    #print("---PARSELIST1---")
    tab = self.soup1.find('table', {'id': 'meteoIntit'})
    td = tab.find_all('td')
    self.intitules = [t.string for t in td]
    return

  def parseList2(self):
    """ Construit le tableau des données météo """
    #print("---PARSELIST2---")
    tab = self.soup2.find('table', {'id': 'meteoHour'})
    tr = tab.find_all('tr')
    for line in tr:
        td = line.find_all('td')
        col=[]
        for t in td:
            if t.img:
                col.append(t.img['title'].replace("direction du vent - ",''))
            else:
                col.append(str(t.string).replace('<','< '))
        self.donnees.append(col)
    return

  def setData(self):
    """ Construit un dictionnaire en associant les données avec leurs intitulés """
    #print("---SETDATA---")
    for i,intit in enumerate(self.intitules):
      self.tableauFinal[intit]=self.donnees[i]
    return

  def returnMeteoData(self):
    """ Renvoie la liste des intitulés et le tableau des données météo """
    self.transformData(self.getData())
    self.parseList1()
    self.parseList2()
    return self.intitules,self.donnees

if __name__ == '__main__':
  print("---MAIN---")
  emw = ExtractMeteoWeb()
  html=emw.getData()
  emw.transformData(html)
  emw.parseList1()
  emw.parseList2()
  #print(emw.donnees)
  emw.setData()
  print(emw.tableauFinal)
  print()
  parsedJson = json.dumps(emw.tableauFinal)
  print(parsedJson)
