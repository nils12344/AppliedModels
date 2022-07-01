# -*- coding: utf-8 -*-
"""
Erstellt am 30.06.2022

@author: Nils Heimbach, Christian T. Seidler

Das Hauptskript. Soll später als Jupyter-Notebook umgesetzt werden.
"""

# import config as c

import os
import pandas as pd
import json


def load_config(filepath):
    """Einlesen der Konfigurationsdatei aus angebenen Pfad."""
    with open(filepath, 'r') as c:
        config = json.load(c)
    return config



def main_nils():
    def read_json(PATH):
        df = pd.read_json(PATH)
        return df

    def extract_mean_GISTEMP(df):
        df = df[df["Source"] == "GISTEMP"]
        return df

    def monthly_temp_into_yearly_mean(df):
        yearly_mean = df.groupby(df['Date'].dt.strftime('%Y'))['Mean'].mean()
        return yearly_mean

    def float_into_df(FLOAT):
        df = pd.DataFrame(FLOAT)
        df = df.reset_index(level=0)
        return df

    def load_temp(path):
        df = read_json(path)
        df = extract_mean_GISTEMP(df)
        FLOAT = monthly_temp_into_yearly_mean(df)
        df = float_into_df(FLOAT)
        return df
    
    # Konfigurationsdatei einlesen
    CONFIG_FILEPATH = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = load_config(CONFIG_FILEPATH)
    
    
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Temperature'])
    df = load_temp(filepath)
    print(df)



def main_christian():
    # Konfigurationsdatei einlesen
    CONFIG_FILEPATH = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = load_config(CONFIG_FILEPATH)
    
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Fossil_Fuel'])
    
    # Datensatz einlesen
    df_input = pd.read_csv(filepath)
    
    # Entfernen aller überflüssigen Spalten
    df = df_input.iloc[:, :3]
    
    # Extrahieren von Deutschland
    df = df[(df['Country'] == 'GERMANY') | 
            (df['Country'] == 'FORMER GERMAN DEMOCRATIC REPUBLIC') |
            (df['Country'] == 'FEDERAL REPUBLIC OF GERMANY')]
    
    # Jahr als Index setzen
    df = df.set_index('Year')
        
    # Zusammenfügen der beiden Werte von 1945 bis 1990
    # Kopie erstellen und filtern
    df_sum_emissions = pd.DataFrame(index=df.index.copy())
    df_sum_emissions = df_sum_emissions.iloc[1945:1990]
    # Für jedes Jahr die Summe der Emissionen erstellen
    for year in range(1945, 1991):
        subset = df.loc[year]
        # Ausreißer in den Jahren 1945 & 1946 werden nicht entfernt,
        # da vernachlässigbar klein
        emissions = subset['Total'].sum()
        df_year = pd.DataFrame({'Year': [year],
                                'Country': ['GERMANY'],
                                'Total': [emissions]})
        # Jahre 1945-1990 in einen Dataframe packen
        df_sum_emissions = pd.concat([df_sum_emissions, df_year])
    df_sum_emissions.set_index('Year', inplace=True)
    
    # Zusammenfügen der Daten
    df = df.drop(index=range(1945, 1991))
    df.reset_index(inplace=True)
    
    df_sum_emissions = df_sum_emissions.reset_index()
    df_summed = pd.concat([df, df_sum_emissions])
        
    df_summed = df_summed[df_summed['Country'] == 'GERMANY']
    
    df_summed = df_summed.sort_values(by='Year').set_index('Year')
    # print(df_summed.loc[1990])
    
    df_final = df_summed.reset_index()
    print(df_final)


if __name__ == '__main__':
    main_nils()
    main_christian()
