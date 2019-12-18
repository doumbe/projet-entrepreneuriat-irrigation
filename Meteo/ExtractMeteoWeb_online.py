from bs4 import BeautifulSoup
import json
import requests

class ExtractMeteoWeb(object):
  intitules=[]
  donnees=[]
  tableauFinal={}
  
  def __init__(self):
    print("---INIT---")
    self.url = 'https://www.lameteoagricole.net/meteo-heure-par-heure/Nice-06000.html'
    return
  
  def getData(self):
    print("---GETDATA---")
    html = requests.get(self.url).text
    return html

  def transformData(self,html):
    print("---TRANSFORMDATA---")
    print("--> part 1")
    f1=html.find("<table id=\"meteoIntit\">")
    f2=html.find("</table>",f1)
    #print(f1,f2)
    html2=html[f1:f2+8]
    #print(html)
    html2=html2.replace("<br />","")
    #print(html2)
    self.soup1 = BeautifulSoup(html2, 'lxml')
    
    print("--> part 2")
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
    print("---PARSELIST1---")
    tab = self.soup1.find('table', {'id': 'meteoIntit'})
    td = tab.find_all('td')
    self.intitules = [t.string for t in td]
    return
  
  def parseList2(self):
    print("---PARSELIST2---")
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
    print("---SETDATA---")
    for i,intit in enumerate(self.intitules):
      self.tableauFinal[intit]=self.donnees[i]
    return
  
  def returnMeteoData(self):
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
