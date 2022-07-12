# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zum Einlesen der Daten.
"""

import os
import pandas as pd


def load_temperature_dataframe(config):
    """Einlesen des Datensatzes 'TemperaturZeitreihe.json'
    und Umwandeln in pd.DataFrame."""

    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Temperature'])
    df_input = read_json_as_dataframe(filepath)
    return df_input


def read_json_as_dataframe(filepath):
    """Einlesen eines JSON-Files und Umwandeln in pd.DataFrame."""

    df_json = pd.read_json(filepath)
    return df_json


def load_fossil_fuel_data_as_dataframe(config):
    """Einlesen des Datensatzes 'fossil-fuel-co2-emissions-by-nation.csv'
    und Umwandeln in pd.DataFrame."""

    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Fossil_Fuel'])
    df_input = pd.read_csv(filepath)
    return df_input
