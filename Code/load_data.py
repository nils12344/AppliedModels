# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zum Einlesen der Daten.
"""

import os
import pandas as pd


def load_temperature_dataframe(config):
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Temperature'])
    df = read_json_as_dataframe(filepath)
    return df


def read_json_as_dataframe(filepath):
    df = pd.read_json(filepath)
    return df


def load_fossil_fuel_dataframe(config):
    df = load_fossil_fuel_data_to_dataframe(config)
    return df


def load_fossil_fuel_data_to_dataframe(config):
    filepath = os.path.join(config['Input_Directory'],
                            config['Filename_Fossil_Fuel'])
    df_input = pd.read_csv(filepath)
    return df_input
