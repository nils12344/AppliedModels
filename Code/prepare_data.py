# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zum Aufbereiten der Daten.
"""

import pandas as pd


def prepare_temperature_dataframe(config, df_temperature):
    """Eingelesenen Datensatz zur Temperaturabweichung für Regression
    vorbereiten (angegebene Quelle extrahieren, jährlichen Mittelwert bilden,
    Einfügen einer Spalte 'Year')."""

    df_temperature = extract_mean_source(df_temperature, config)
    monthly_temp_series = monthly_temp_into_yearly_mean(df_temperature)
    df_prepared = series_into_df(monthly_temp_series)
    df_prepared['Year'] = df_prepared['Year'].astype(int)

    return df_prepared


def extract_mean_source(df_temperature, config):
    """Den eingelesen Datensatz zur Temperaturabweichung gemäß der in der
    Config.json angegebenen Source (GISTEMP oder GCAG) filtern."""

    df_temperature = df_temperature[df_temperature["Source"] ==
                                    config['Temperature_Source']]
    return df_temperature


def monthly_temp_into_yearly_mean(df_temp):
    """Jährlichen Mittelwert aus monatlichen Daten der Temperaturabweichung
    bestimmen."""

    yearly_mean = df_temp.groupby(df_temp['Date'].dt.strftime('%Y'))['Mean'] \
        .mean()
    return yearly_mean


def series_into_df(series):
    """pd.Series in pd.DataFrame umwandeln, Index zurücksetzen und
    Spalte 'Date' in 'Year' umbenennen."""

    df_prepared = pd.DataFrame(series)
    df_prepared = df_prepared.reset_index(level=0)
    df_prepared = df_prepared.rename(columns={'Date': 'Year'})
    return df_prepared


def prepare_fossil_fuel_dataframe(config, df_fossil_fuel):
    """Eingelesenen Datensatz der CO2-Emissionen für die Regression vorbereiten
    (extrahieren der Spalte 'Total', filtern nach dem in Config.json
     angegebenen Country: Falls GERMANY, dann berücksichtung der Teilung
     Deutschlands von 1945 bis 1990)."""

    df_input = extract_fossil_fuel_columns(df_fossil_fuel)
    country = config['Fossil_Fuel_Country']

    # Berücksichtung der Teilung Deutschlands (Jahre 1945 bis 1990)
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
    """pd.DataFrame auf die Spalten 'Year', 'Country' und 'Total'
    reduzieren."""

    df_res = df_fossil_fuel.iloc[:, :3]
    return df_res


def filter_country(df_fossil_fuel, country):
    """pd.DataFrame gemäß dem in der Config.json angegebenen Land filtern."""

    df_country = df_fossil_fuel[df_fossil_fuel['Country'] == country]
    return df_country


def filter_country_germany(df_fossil_fuel):
    """pd.DataFrame für Deutschland filtern. Umfasst Deutschland,
    Westdeutschland und die DDR."""

    df_germany = df_fossil_fuel[(df_fossil_fuel['Country'] == 'GERMANY') |
                                (df_fossil_fuel['Country'] ==
                                 'FORMER GERMAN DEMOCRATIC REPUBLIC') |
                                (df_fossil_fuel['Country'] ==
                                 'FEDERAL REPUBLIC OF GERMANY')]
    return df_germany


def aggregate_west_and_east_germany(df_fossil_fuel):
    """Summe der Emissionen für Westdeutschland und die DDR für den Zeitraum
    von 1945 bis 1990 bilden."""

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

    # Jahr aös Index setzen
    df_sum_emissions.set_index('Year', inplace=True)

    return df_sum_emissions


def merge_sum_emissions_and_normal_country_dataframe(df_germany,
                                                     df_sum_emissions):
    """Berechnete Summe der Emissionen von Deutschland für den Zeitraum
    1945 bis 1990 in den pd.DataFrame einfügen."""

    # Jahre 1945 bis 1990 aus gesamten Frame entfernen
    df_germany = df_germany.drop(index=range(1945, 1991))
    df_germany.reset_index(inplace=True)

    # Datensätze zusammenfügen
    df_sum_emissions = df_sum_emissions.reset_index()
    df_merged = pd.concat([df_germany, df_sum_emissions])

    # Werte nach Jahr sortieren
    df_final = df_merged.sort_values(by='Year')

    return df_final
