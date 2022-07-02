# -*- coding: utf-8 -*-
"""
Erstellt am 30.06.2022

@author: Nils Heimbach, Christian T. Seidler

Das Hauptskript. Soll später als Jupyter-Notebook umgesetzt werden.
"""

import os
import pandas as pd
import json
import matplotlib.pyplot as plt
import seaborn as sns
import statsmodels.formula.api as smf
import time
from scipy import stats
import numpy as np
import logging


def load_config(filepath):
    """Einlesen der Konfigurationsdatei aus angebenen Pfad."""
    with open(filepath, 'r') as c:
        config = json.load(c)
    return config


def import_and_prepare_temperature_dataframe(config):
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Temperature'])
    df = read_json(filepath)
    df = extract_mean_gistemp(df)
    FLOAT = monthly_temp_into_yearly_mean(df)
    df = float_into_df(FLOAT)
    df['Year'] = df['Year'].astype(int)
    return df


def read_json(PATH):
    df = pd.read_json(PATH)
    return df


def extract_mean_gistemp(df):
    df = df[df["Source"] == "GISTEMP"]
    return df


def monthly_temp_into_yearly_mean(df):
    yearly_mean = df.groupby(df['Date'].dt.strftime('%Y'))['Mean'].mean()
    return yearly_mean


def float_into_df(FLOAT):
    df = pd.DataFrame(FLOAT)
    df = df.reset_index(level=0)
    df = df.rename(columns={'Date': 'Year'})
    return df


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


def create_run_directory(config):
    current_time = time.strftime("%Y-%b-%d_%H-%M-%S")
    run_directory_string = "Run_" + current_time

    Run_Directory = os.path.join(config['Output_Directory'],
                                 run_directory_string)
    os.mkdir(Run_Directory)

    return Run_Directory


def main():

    # Konfigurationsdatei laden
    CONFIG_FILEPATH = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = load_config(CONFIG_FILEPATH)

    # Neues Run-Directory anlegen
    Run_Directory = create_run_directory(config)

    # Logger anlegen
    logger = logging.getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=os.path.join(Run_Directory,
                                              config['Log_Filename']),
                        level=logging.INFO)
    logging.info('Das Dashboard wurde gestartet.')
    logging.info('Die Konfigurationsparameter wurden erfolgreich eingelesen.')
    logging.info('Das Run-Directory wurde erfolgreich angelegt.')

    # Fossil-Fuel-Daten einlesen
    df_fossil_fuel = import_and_prepare_fossil_fuel_dataframe(config)
    print(df_fossil_fuel.shape)
    logging.info('Die CO2-Daten wurden erfolgreich eingelesen.')

    # Temperaturdaten einlesen
    df_temperature = import_and_prepare_temperature_dataframe(config)
    print(df_temperature.shape)
    logging.info('Die mittlere Temperaturabweichungsdaten wurden '
                 'erfolgreich eingelesen.')

    # Datensätze zusammenfügen
    df_merged = pd.merge(df_fossil_fuel, df_temperature, how='inner',
                         on='Year')
    print(df_merged)

    # Tabelle zur Validierung in Datei abspeichern (.csv)
    filepath = os.path.join(Run_Directory, 'merged_dataset.csv')
    df_merged.to_csv(filepath)

    # Visualisierung von CO2-Daten und Temperaturabweichung
    # Verlauf von Temperatur
    plt.figure(1)
    sns.scatterplot(x='Year', y='Mean', data=df_merged)
    plt.title('Year vs. Mean')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot1'))

    # Temperaturwerte über 800 entfernen (Jahre 1928 & 1984)
    df_final = df_merged[(df_merged.Mean) < 800]

    # Verlauf der Temperatur
    plt.figure(2)
    sns.scatterplot(x='Year', y='Mean', data=df_final)
    plt.title('Year vs. Mean after outlier removal')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot2'))

    # Verlauf von CO2-Emissionen
    plt.figure(3)
    sns.scatterplot(x='Year', y='Total', data=df_final)
    plt.title('Year vs. Total CO2-Emissions of Germany')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot3'))

    # Scatterplot Temperatur vs. CO2-Emissionen
    plt.figure(4)
    sns.scatterplot(x='Total', y='Mean', data=df_final)
    plt.title('Yearly Temperature Deviation vs.'
              'Total CO2-Emissions of Germany')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot4'))

    # Regressionsplot
    plt.figure(5)
    sns.regplot(x='Total', y='Mean', data=df_final, order=1)
    plt.title('Yearly Temperature Deviation vs.'
              'Total CO2-Emissions of Germany')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot5'))

    # Abspeichern der Visualisierung
    # Done

    # Ausreißer (Flats und Spikes) in Daten entdecken und behandeln
    # Boxplot
    plt.figure(6)
    sns.boxplot(y='Mean', data=df_final)
    plt.title('Boxplot for average yearly temperature deviation')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot6'))

    plt.figure(7)
    sns.boxplot(y='Total', data=df_final)
    plt.title('Boxplot for total CO2-Emissions of Germany per year')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot7'))

    # Histogramme
    plt.figure(8)
    sns.histplot(x='Mean', data=df_final, kde=True)
    plt.title('Average yearly temperature deviation')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot8'))

    plt.figure(9)
    sns.histplot(x='Total', data=df_final, kde=True)
    plt.title('Average total CO2-Emissions of Germany per year')
    plt.show()
    plt.savefig(os.path.join(Run_Directory, 'plot9'))

    # Ausreißer (Spikes) mittels Z-Score
    z = np.abs(stats.zscore(df_final['Mean']))
    threshold = 3  # Position of the outlier
    print("Outliers in Mean:", np.where(z > threshold))

    z = np.abs(stats.zscore(df_final['Total']))
    threshold = 3  # Position of the outlier
    print("Outliers in Total:", np.where(z > threshold))

    # Ausreißer (Spikes) mittels Interquartilabstand
    Q1 = np.percentile(df_final['Mean'], 25,
                       method='midpoint')
    Q3 = np.percentile(df_final['Mean'], 75,
                       method='midpoint')
    IQR = Q3 - Q1
    # Above Upper bound
    upper = df_final['Mean'] >= (Q3+1.5*IQR)
    print(np.where(upper))
    # Below Lower bound
    lower = df_final['Mean'] <= (Q1-1.5*IQR)
    print(np.where(lower))

    Q1 = np.percentile(df_final['Total'], 25,
                       method='midpoint')
    Q3 = np.percentile(df_final['Total'], 75,
                       method='midpoint')
    IQR = Q3 - Q1
    # Above Upper bound
    upper = df_final['Total'] >= (Q3+1.5*IQR)
    print(np.where(upper))
    # Below Lower bound
    lower = df_final['Total'] <= (Q1-1.5*IQR)
    print(np.where(lower))

    # Suche nach Flats
    df_final['Total_diff'] = df_final['Total'].diff()
    df_final['Mean_diff'] = df_final['Mean'].diff()
    print("Flats in Total:", df_final[df_final['Total_diff'] == 0])
    print("Flats in Mean:", df_final[df_final['Mean_diff'] == 0])

    # Abspeichern zu Validierungszwecken
    filepath = os.path.join(Run_Directory, 'final_dataset.csv')
    df_final.to_csv(filepath)

    # Durchführen einer Regression (-1, um Intercept zu entfernen
    # I(Total**3) für kubischen Term)
    res = smf.ols(formula='Mean ~ 1 + Total', data=df_final).fit()
    print(res.summary())

    # Abspeichern der Regressionsergebnisse als .csv
    print(res.params)     # Koeffizienten
    print(res.rsquared)     # R2-Wert
    regression_results = {'parameter': res.params.to_list(),
                          'intercept': res.params[0],
                          'total': res.params[1],
                          'r2_score': res.rsquared
                          }
    filepath = os.path.join(Run_Directory, 'Regression_Results.csv')
    with open(filepath, 'w') as f:
        for key in regression_results.keys():
            f.write("%s, %s\n" % (key, regression_results[key]))
    # gesamte Summary abspeichern
    # Note that tables is a list. The table at index 1 is the "core" table.
    # Additionally, read_html puts dfs in a list, so we want index 0
    results_as_html = res.summary().tables[1].as_html()
    df_summary = pd.read_html(results_as_html, header=0, index_col=0)[0]
    filepath = os.path.join(Run_Directory, 'Regression_Summary.csv')
    df_summary.to_csv(filepath)
    print(df_summary)


if __name__ == '__main__':
    main()
