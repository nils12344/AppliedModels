# -*- coding: utf-8 -*-
"""
Erstellt am 30.06.2022

@author: Nils Heimbach, Christian T. Seidler

Das Hauptskript. Soll später als Jupyter-Notebook umgesetzt werden.
"""

import os
import logging
import pandas as pd

import config as c
import load_data as load
import prepare_data as prep
import data_visualization as vis
import outlier_analysis as outlier
import regression as reg
import linear_regression_diagnostics as diagnostics


def main():

    # Konfigurationsdatei laden
    config_filepath = r'D:\HS Albstadt\Sommersemester 2022' \
        r'\Python Applied Models\Abschlussaufgabe\Data\Input\Config.json'
    config = c.load_config(config_filepath)

    # Neues Run-Directory anlegen
    run_directory = c.create_run_directory(config)

    # Logger anlegen
    logger = logging.getLogger()
    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])
    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=os.path.join(run_directory,
                                              config['Log_Filename']),
                        level=logging.INFO)
    logging.info('Das Dashboard wurde gestartet.')
    logging.info('Die Konfigurationsparameter wurden erfolgreich eingelesen.')
    logging.info('Das Run-Directory wurde erfolgreich angelegt.')

    # Fossil-Fuel-Daten einlesen
    df_fossil_fuel = load.load_fossil_fuel_data_to_dataframe(config)
    df_fossil_fuel = prep.prepare_fossil_fuel_dataframe(config, df_fossil_fuel)
    print(df_fossil_fuel.shape)
    logging.info('Die CO2-Daten wurden erfolgreich eingelesen.')

    # Temperaturdaten einlesen
    df_temperature = load.load_temperature_dataframe(config)
    df_temperature = prep.prepare_temperature_dataframe(config, df_temperature)
    print(df_temperature.shape)
    logging.info('Die mittlere Temperaturabweichungsdaten wurden '
                 'erfolgreich eingelesen.')

    # Datensätze zusammenfügen
    df_merged = pd.merge(df_fossil_fuel, df_temperature, how='inner',
                         on='Year')
    print(df_merged)
    logging.info('Die Datensätze wurden erfolgreich zusammengeführt.')

    # Tabelle zur Validierung in Datei abspeichern (.csv)
    filepath = os.path.join(run_directory, 'merged_dataset.csv')
    df_merged.to_csv(filepath)
    logging.info('Der zusammengeführte Datensatz wurde unter %s'
                 ' gespeichert.', filepath)

    # Visualisierung von CO2-Daten und Temperaturabweichung
    # Verlauf von Temperatur
    vis.show_scatterplot(x='Year', y='Mean', data=df_merged,
                         title='Year vs. Mean')
    vis.savefig(run_directory, 'plot1')

    # Temperaturwerte über 800 entfernen (Jahre 1928 & 1984)
    df_final = df_merged[(df_merged.Mean) < 800]

    # Verlauf der Temperatur
    vis.show_scatterplot(x='Year', y='Mean', data=df_final,
                         title='Year vs. Mean after outlier removal')
    vis.savefig(run_directory, 'plot2')

    # Verlauf von CO2-Emissionen
    vis.show_scatterplot(x='Year', y='Total', data=df_final,
                         title='Year vs. Total CO2-Emissions of Germany')
    vis.savefig(run_directory, 'plot3')

    # Scatterplot Temperatur vs. CO2-Emissionen
    vis.show_scatterplot(x='Total', y='Mean', data=df_final,
                         title='Yearly Temperature Deviation vs.'
                         'Total CO2-Emissions of Germany')
    vis.savefig(run_directory, 'plot4')

    # Regressionsplot
    vis.show_regressionplot(x='Total', y='Mean', data=df_final,
                            title='Yearly Temperature Deviation vs.'
                            'Total CO2-Emissions of Germany')
    vis.savefig(run_directory, 'plot5')

    # Ausreißer (Flats und Spikes) in Daten entdecken und behandeln
    # Boxplot
    outlier.show_boxplot(y='Mean', data=df_final,
                         title='Boxplot for average yearly'
                         ' temperature deviation')
    vis.savefig(run_directory, 'plot6')

    outlier.show_boxplot(y='Total', data=df_final,
                         title='Boxplot for total CO2-Emissions of Germany'
                         ' per year')
    vis.savefig(run_directory, 'plot7')

    # Histogramme
    outlier.show_histogramm(x='Mean', data=df_final,
                            title='Average yearly temperature deviation')
    vis.savefig(run_directory, 'plot8')

    outlier.show_histogramm(x='Total', data=df_final,
                            title='Average total CO2-Emissions of Germany'
                            ' per year')
    vis.savefig(run_directory, 'plot9')

    # Ausreißer (Spikes) mittels Z-Score
    outlier.calc_and_print_outliers_with_z_score(data=df_final, column='Mean')
    outlier.calc_and_print_outliers_with_z_score(data=df_final, column='Total')

    # Ausreißer (Spikes) mittels Interquartilabstand
    outlier.calc_and_print_outliers_with_iqr(data=df_final, column='Mean')
    outlier.calc_and_print_outliers_with_iqr(data=df_final, column='Total')

    # Suche nach Flats
    outlier.print_num_of_flats(data=df_final, column='Mean')
    outlier.print_num_of_flats(data=df_final, column='Total')

    # Abspeichern zu Validierungszwecken
    filepath = os.path.join(run_directory, 'final_dataset.csv')
    df_final.to_csv(filepath)

    # Durchführen einer Regression (-1, um Intercept zu entfernen
    # I(Total**3) für kubischen Term)
    models = config["Regression_Models"]
    for key, value in models.items():
        # Unterverzeichnis anlegen
        model_directory = c.create_model_directory(run_directory, key)

        df_teil_zeitraum = df_final
        df_validation = None

        # Teilzeitraum bestimmen
        teil_zeitraum = reg.get_teil_zeitraum_from_config(
            value['Teil_Zeitraeume'])
        # Datensatz nach Teilzeitraum filtern
        if teil_zeitraum is not None:
            df_teil_zeitraum = df_final[df_final['Year'].isin(teil_zeitraum)]

        # Validation Sample
        teil_zeitraum = reg.get_teil_zeitraum_from_config(
            value['Validation_Sample'])
        # Extra Datensatz für Validierungssample
        if teil_zeitraum is not None:
            df_validation = df_final[df_final['Year'].isin(teil_zeitraum)]
            x_val = df_validation['Total']

        # Regression durchführen
        regression_model = reg.fit_regression_model(config=value,
                                                    data=df_teil_zeitraum)

        # Validierung durchführen
        if df_validation is not None:
            predictions = regression_model.predict(x_val)
            # Grafische Darstellung
            vis.visualize_validation_sample(df_validation, predictions)
            vis.savefig(model_directory, 'Validation_Results')

        print(regression_model.summary())

        # Grafische Darstellung des Ergebnisses
        vis.visualize_regression_results(df_final, regression_model)
        vis.savefig(model_directory, 'Regression_Results')

        # Abspeichern der Regressionsergebnisse als .csv
        filename = str(key) + '_Regression'
        reg.save_regression_results_as_csv(model=regression_model,
                                           run_directory=model_directory,
                                           filename=filename+'_Results.csv')

        # Gesamte Summary abspeichern
        reg.save_regression_summary_as_csv(model=regression_model,
                                           run_directory=model_directory,
                                           filename=filename+'_Summary.csv')

        # Erweiterung um Überprüfung der Annahmen der Regression
        cls = diagnostics.Linear_Reg_Diagnostic(regression_model)
        cls()
        vis.savefig(model_directory, 'model_assumptions')

    # Logger abschalten
    logging.shutdown()


if __name__ == '__main__':
    main()
