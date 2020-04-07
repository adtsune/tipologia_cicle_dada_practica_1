import requests
#from bs4 import BeautifulSoup
import json
import jsonstat
import pandas as pd
import os.path
import time


# llegir_pagina: Llegir una pàgina html que retornem en un objecte tipus String
def llegir_pagina(url, filename):

  # Si la pàgina s'ha descarregat previament, fem servir la copia local
  if os.path.isfile(filename):

    f = open(filename,"r")
    contingut = f.read()
    f.close()

  else:

    s=requests.session()

    headers = {
      "User-Agent":"Mozilla/5.0 (Macintosh; Intel Mac OS X 10.12; rv:72.0) Gecko/20100101 Firefox/72.0"
    }

    page = s.get(url, headers=headers)

    page=requests.get(url)
    
    # Desem una còpia local de la pàgina descarregada.
    f = open(filename,"a", encoding="utf-8")
    f.write(page.text)
    f.close()

    contingut = page.text

  return contingut

# llegir_indicador_world_bank: Funció per obtenir un indicador del Banc Mundial (via API)

def llegir_indicador_world_bank(indicador):
  # Consultem via API la web del Banc Mundial.
  # La funció retorna un Panda DataFrame amb les columnes "country","year","<indicador>"
  
  filename = os.getcwd() + "/" + indicador + ".jsonstat"
  url = "https://api.worldbank.org/v2/country/all/indicator/" + indicador + "?format=jsonstat"

  if os.path.isfile(filename):
    jstat = jsonstat.from_file(filename)
  else:
    jstat = jsonstat.from_string(jsonstat.download(url,filename))

  df = jstat.dataset(0).to_data_frame(content='id')
  
  df.drop(columns="series",inplace=True)
  df.rename(columns={"Value":indicador},inplace=True)

  return df

# Funció que retorna un dataset amb la llista de paisos ISO3166 de la web del IBAN
def obtenir_llista_iso3166():
  ccodes = llegir_pagina("https://www.iban.com/country-codes","iso_country_codes.html")

  bs = BeautifulSoup(ccodes, features="html5lib")

  ll = []
  for i in bs.body.table.tbody.find_all("tr"): 
    r =i.find_all("td"); 
    ll.append([r[0].text,r[1].text,r[2].text])

  df = pd.DataFrame(ll,columns=['country','ISO2','ISO3'])

  return df