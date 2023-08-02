import pandas as pd

import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

import pyfolio as pf
import requests 
import csv as csv
import mpld3 
import math
import pandas as pd
import requests
from datetime import date
from datetime import datetime

from datetime import datetime


# Obtenez la date actuelle
now = datetime.now()



mois_actuel = datetime.now().month



url = 'https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr.csv?distance=55&grandeur_hydro=H&latitude=43.64&longitude=0.42&size=20000&sort=desc'
df = pd.read_csv(url, sep=';', header=0, decimal=',')
#df=pd.DataFrame(index = range(1,100),columns=['code_site','code_station', 'date_obs','resultat_obs'])




df['date_obs'] = pd.to_datetime(df['date_obs'])

# Transformer la colonne en nombre
df['resultat_obs'] = pd.to_numeric(df['resultat_obs'])




df.head(5)

df.index = df['date_obs']
#df.sort_values(by = ['code_station'], ascending = True)

df2=df[['code_station', 'date_obs', 'resultat_obs']]

#df2=df2[:19000]
df2['count']= 0
resultat = df2['code_station'].value_counts()
#print(resultat)

df2.drop_duplicates(subset=['code_station'], keep='first', inplace=True)
#df2.head(35)
df2['nom station'] =0

resultat = df2['code_station'].value_counts()
#print(resultat)


df33 = pd.read_csv('liste stations2.csv')#, sep=';', header=0, decimal='.')


df007= df33[['code_station', 'nom_station']]
df007
df007.index=df007['code_station']
df007
df33['seuil jaune bas'] = pd.to_numeric(df33['seuil jaune bas'])
df33['seuil orange bas'] = pd.to_numeric(df33['seuil orange bas'])
df33['seuil jaune haut'] = pd.to_numeric(df33['seuil jaune haut'])
df33['seuil orange haut'] = pd.to_numeric(df33['seuil orange haut'])
df33['seuil rouge bas'] = pd.to_numeric(df33['seuil rouge bas'])

df99= pd.merge(df33,df2)
df99.drop(columns = ['count', 'nom station'], inplace = True)

df100 = df99.copy()
df100.index = df100.code_station
df100['cote(m)']=0
df100['max probable'] =0
df100['max de max probable'] =0
df100['previ deb'] = 0
df100['previ orange'] =0
#df100['resultat_obs'] = pd.to_numeric(df['resultat_obs'])
df100['cote(m)'] = df100['resultat_obs']/1000
df100['nom station'] = 'toto'
df100['nom station'] = df100['nom_station'] 

df100['marge 1er debord']=0
df100['marge seuil orange']=0
df100['marge 1er debord'] =  df100['seuil jaune bas']- df100['cote(m)']
df100['marge seuil orange'] = df100['seuil orange bas']- df100['cote(m)']

#calcul du max par station et remplissage colonne max :

df100['max']=0
df100['datemax']='**'

for code_station in list (df007.index) :

       
      df25 = df.copy()
      df25=df25[['code_station','resultat_obs']]
      nom=df007.loc[code_station,'nom_station']
      df25.rename(columns = {'resultat_obs': nom})
      
      df25 = df25.sort_values(by = ['date_obs'], ascending = True)
      
      df25= df25[df25['code_station']==code_station]
        
     
      df25['max'] = (df25['resultat_obs'].max())/1000
      df100.loc[code_station,'max'] = df25['max'][25]
      df25['dif'] = df25['max']-df25['resultat_obs']/1000
      df25['date max'] = '**'
      
     
      df25['datobs']= df25.index
    
      df25['date max'] = df25.loc[df25['dif'] == 0, 'datobs'].values[0]
      df100.loc[code_station,'datemax'] = df25['date max'][25]
      
df100
#df25.head(5)
df_max=df100[['nom_station', 'max']]
df_max

 # Filtrer les données pour les stations dont le code est contenu dans le DataFrame "stations"
#station_codes = station_df['code_station'].tolist()
#station_data = df[df['code_station'].isin(station_codes)]

    # Trouver la valeur maximale dans la colonne 'resultat_obs' pour chaque station
max_values = df_max['max']

    # Ajouter la colonne 'max{datedujour}' contenant la valeur maximale du jour
max_column_name = f'max{date.today()}'
#datemax_column_name = f'datemax{date.today()}'
df_max.rename(columns={'max': max_column_name},inplace=True)

df_max 

import pandas as pd
import datetime


# Obtenez la date actuelle
aujourd_hui = datetime.datetime.now()
mois_annee_en_cours = aujourd_hui.strftime('%m_%Y')  # Format : mois_année

# Créez une nouvelle colonne avec la date du jour au format 'jour_mois_annee'
colonne_date = aujourd_hui.strftime('%d_%m_%Y')
#df_max[colonne_date] = None  # Vous pouvez remplir les valeurs de la colonne si nécessaire

# Si le fichier CSV existe déjà, lisez-le pour ajouter les nouvelles colonnes
try:
    df_existant = pd.read_csv(f'{mois_annee_en_cours}.csv', index_col=0,sep=';', header=0, decimal=',')
    #df = pd.read_csv(url, sep=';', header=0, decimal=',')
    df_max = pd.concat([df_existant, df_max], axis=1)
except FileNotFoundError:
    pass  # Le fichier n'existe pas encore

# Sauvegardez le DataFrame mis à jour dans un fichier CSV
df_max.to_csv(f'{mois_annee_en_cours}.csv')

print(f"Données mises à jour pour le {colonne_date} et sauvegardées dans le fichier {mois_annee_en_cours}.csv.")