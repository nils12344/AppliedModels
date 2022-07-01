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

    def load_temp(path):
        df = read_json(path)
        df = extract_mean_GISTEMP(df)
        FLOAT = monthly_temp_into_yearly_mean(df)
        df = float_into_df(FLOAT)
        return df

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

    # Konfigurationsdatei einlesen
    CONFIG_FILEPATH = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = load_config(CONFIG_FILEPATH)

    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Temperature'])
    df = load_temp(filepath)
    print(df)

    # joining dataframe temperatur and dataframe co2
    # df_cd = pd.merge(df_temp, df_co2, how='inner', on = 'Date')


# Für Datei Fossil_Fuel
def import_and_prepare_fossil_fuel_dataframe(config):
    df_input = load_fossil_fuel_data_to_dataframe(config)
    df_input = extract_fossil_fuel_columns(df_input)
    df_country = filter_country_germany(df_input)
    df_country.set_index('Year', inplace=True)
    df_sum_emissions = aggregate_west_and_east_germany(df_country)
    df_fossil_fuel = merge_sum_emissions_and_normal_country_dataframe(
        df_country, df_sum_emissions)
    return df_fossil_fuel


def load_fossil_fuel_data_to_dataframe(config):
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Fossil_Fuel'])
    df_input = pd.read_csv(filepath)
    return df_input


def extract_fossil_fuel_columns(df_fossil_fuel):
    df_res = df_fossil_fuel.iloc[:, :3]
    return df_res


def filter_country_germany(df_fossil_fuel):
    df_germany = df_fossil_fuel[(df_fossil_fuel['Country'] == 'GERMANY') |
                                (df_fossil_fuel['Country'] ==
                                 'FORMER GERMAN DEMOCRATIC REPUBLIC') |
                                (df_fossil_fuel['Country'] ==
                                 'FEDERAL REPUBLIC OF GERMANY')]
    return df_germany


# TODO: Funktion aufspalten
def aggregate_west_and_east_germany(df_fossil_fuel):
    # Kopie erstellen und filtern
    df_sum_emissions = pd.DataFrame(index=df_fossil_fuel.index.copy())
    df_sum_emissions = df_sum_emissions.iloc[1945:1990]
    # Für jedes Jahr die Summe der Emissionen erstellen
    for year in range(1945, 1991):
        subset = df_fossil_fuel.loc[year]
        # Ausreißer in den Jahren 1945 & 1946 werden nicht entfernt,
        # da vernachlässigbar klein
        emissions = subset['Total'].sum()
        df_year = pd.DataFrame({'Year': [year],
                                'Country': ['GERMANY'],
                                'Total': [emissions]})
        # Jahre 1945-1990 in einen Dataframe packen
        df_sum_emissions = pd.concat([df_sum_emissions, df_year])
    # Index setzen
    df_sum_emissions.set_index('Year', inplace=True)
    return df_sum_emissions


def merge_sum_emissions_and_normal_country_dataframe(df_germany,
                                                     df_sum_emissions):
    # Jahre 1945 bis 1990 aus gesamten Frame entfernen
    df_germany = df_germany.drop(index=range(1945, 1991))
    df_germany.reset_index(inplace=True)

    # Datensätze zusammenfügen
    df_sum_emissions = df_sum_emissions.reset_index()
    df_merged = pd.concat([df_germany, df_sum_emissions])

    # Werte nach Jahr sortieren
    df_final = df_merged.sort_values(by='Year')

    return df_final


def main():
    # Konfigurationsdatei laden
    CONFIG_FILEPATH = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = load_config(CONFIG_FILEPATH)

    # Fossil-Fuel-Daten einlesen
    df_fossil_fuel = import_and_prepare_fossil_fuel_dataframe(config)
    print(df_fossil_fuel)

    # Temperaturdaten einlesen

    # Datensätze zusammenfügen

    # Tabelle zur Validierung in Datei abspeichern

    # Visualisierung von CO2-Daten und Temperaturabweichung

    # Abspeichern der Visualisierung

    # Ausreißer in Daten behandeln

    # Durchführen einer Regression

    # Abspeichern der Regression


if __name__ == '__main__':
    main()
    main_nils()
