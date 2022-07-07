# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Datei mit Funktionen zum Einlesen und Aufbereiten der Daten.
"""

import pandas as pd


def prepare_temperature_dataframe(config, df_temperature):
    df_temperature = extract_mean_source(df_temperature, config)
    monthly_temp_series = monthly_temp_into_yearly_mean(df_temperature)
    df = series_into_df(monthly_temp_series)
    df['Year'] = df['Year'].astype(int)
    return df


def read_json_as_dataframe(filepath):
    df = pd.read_json(filepath)
    return df


def extract_mean_source(df, config):
    df = df[df["Source"] == config['Temperature_Source']]
    return df


def monthly_temp_into_yearly_mean(df):
    yearly_mean = df.groupby(df['Date'].dt.strftime('%Y'))['Mean'].mean()
    return yearly_mean


def series_into_df(series):
    df = pd.DataFrame(series)
    df = df.reset_index(level=0)
    df = df.rename(columns={'Date': 'Year'})
    return df


# Für Datei Fossil_Fuel
def prepare_fossil_fuel_dataframe(config, df_fossil_fuel):
    df_input = extract_fossil_fuel_columns(df_fossil_fuel)
    country = config['Fossil_Fuel_Country']
    if country == "GERMANY":
        df_country = filter_country_germany(df_input)
        df_country.set_index('Year', inplace=True)
        df_sum_emissions = aggregate_west_and_east_germany(df_country)
        df_fossil_fuel = merge_sum_emissions_and_normal_country_dataframe(
            df_country, df_sum_emissions)
    else:
        df_fossil_fuel = filter_country(df_fossil_fuel, country)
    return df_fossil_fuel


def extract_fossil_fuel_columns(df_fossil_fuel):
    df_res = df_fossil_fuel.iloc[:, :3]
    return df_res


def filter_country(df_fossil_fuel, country):
    df_country = df_fossil_fuel[df_fossil_fuel['Country'] == country]
    return df_country


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
        # Ausreißer in den Jahren 1945 & 1946 werden nicht entfernt
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
