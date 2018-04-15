import os
import requests
import csv
import re
from bs4 import BeautifulSoup
from urllib.request import urlopen

#Funcion para obtener los niveles de los embalses
def queryNivel(queryURL,headersValues,elementList,cuenca):
  response= urlopen(queryURL)
  html = response.read()
  soup = BeautifulSoup(html,"lxml")
  #table=soup.find('table');
  table = soup.find(attrs={'class':'Tabla'})
  #rows = table.find_all('tr')
  #td = tr.find(attrs={'class':'ResultadoCampo'})
  currentIndex=0
  for row in table.findAll("tr"):
    cells = row.findAll("td")
    if (currentIndex > 0):
      capacidad=cells[1].find(text=True)
      embalsada=cells[2].find(text=True)
      variacion=cells[3].find(text=True)
      aux=cells[0].find("a")
      nombre = aux.text
      element=[nombre,capacidad,embalsada,variacion,cuenca]
      elementList.append(element)
    currentIndex=currentIndex+1
  return
#Current directory where is located the script
currentDir = os.path.dirname(__file__)
filename = "embalses_dataset.csv"
filePath = os.path.join(currentDir, filename)
Urls=["https://www.embalses.net/cuenca-2-duero.html","https://www.embalses.net/cuenca-5-ebro.html","https://www.embalses.net/cuenca-3-tajo.html"]
Cuencas=["Duero","Ebro","Tajo"]
headerValues={}
embalsesList=[]
headerList=["Pantano","Capacidad","Embalsada","Variacion","Cuenca"]
embalsesList.append(headerList)
for i in range(0,3):
    queryNivel(Urls[i],headerValues,embalsesList,Cuencas[i])
with open(filePath, 'w', newline='') as csvFile:
  writer = csv.writer(csvFile)
  for embalse in embalsesList:
    writer.writerow(embalse)
