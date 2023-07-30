import pandas as pd
import requests
from datetime import date
from datetime import datetime
  # Obtenir le numéro du mois en cours
import pandas as pd
from datetime import datetime

# Ici, nous supposons que vous avez déjà le DataFrame df

# Obtenez la date actuelle
now = datetime.now()

# Formate la date au format "toto{année mois}"




mois_actuel = datetime.now().month

# Étape 1: Importer le fichier liste_station2.csv et créer le DataFrame "stations"
stations = pd.read_csv('liste stations2.csv')#, sep=';', header=0)
station_df=stations

def fetch_data_from_api():
    url = 'https://hubeau.eaufrance.fr/api/v1/hydrometrie/observations_tr.csv?distance=55&grandeur_hydro=H&latitude=43.64&longitude=0.42&size=20000&sort=desc'
    response = requests.get(url)
    df = pd.read_csv(response.url, sep=';', header=0, decimal=',')
    return df

def update_stock_hydro_csv(df, station_df):
    # Filtrer les données pour les stations dont le code est contenu dans le DataFrame "stations"
    station_codes = station_df['code_station'].tolist()
    station_data = df[df['code_station'].isin(station_codes)]

    # Trouver la valeur maximale dans la colonne 'resultat_obs' pour chaque station
    max_values = station_data.groupby('code_station')['resultat_obs'].max().reset_index()

    # Ajouter la colonne 'max{datedujour}' contenant la valeur maximale du jour
    max_column_name = f'max{date.today()}'
    max_values.rename(columns={'resultat_obs': max_column_name}, inplace=True)

    # Charger le fichier CSV existant ou créer un nouveau s'il n'existe pas
    file_path = (f"stock_hydro{now.strftime('%Y%m')}.csv")
    #file_path = (f'stock_hydro{mois_actuel}.csv')
    try:
        existing_data = pd.read_csv(file_path)
        # Fusionner les nouvelles valeurs maximales avec les données existantes
        updated_data = pd.merge(existing_data, max_values, on='code_station', how='outer')
        updated_data.to_csv(file_path, index=False)
    except FileNotFoundError:
        # Si le fichier n'existe pas, créer un nouveau fichier CSV avec les valeurs maximales
        max_values.to_csv(file_path, index=False)

if __name__ == "__main__":
    # Récupérer les données de l'API
    data = fetch_data_from_api()
    
    # Mettre à jour le fichier CSV de stockage avec les valeurs maximales pour les stations dans le DataFrame "stations"
    update_stock_hydro_csv(data, stations)

    # Afficher le DataFrame stock_hydro pour une meilleure lisibilité
    stock_hydro_df = pd.read_csv(f"stock_hydro{now.strftime('%Y%m')}.csv")

# rajouter colonne stations en concaténant avec stations et changement index      
stock_hydro_df = pd.concat([stock_hydro_df, stations[['nom_station']]], axis=1)
stock_hydro_df.set_index('nom_station', inplace=True)
   
stock_hydro_df.to_csv((f"stock_hydro{now.strftime('%Y%m')}.csv"), index=True)

 


    #stock_hydro_df.to_csv('stock_hydro6.csv', index=False)
