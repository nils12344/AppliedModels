# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zur Initialisierung des Programms.
"""

import json
import time
import os


def load_config(filepath):
    """Einlesen der Konfigurationsdatei aus angebenen Pfad."""

    with open(filepath, 'r') as file:
        config = json.load(file)
    return config


def create_run_directory(config):
    """Erstellen einesn neuen Run-Directories."""

    current_time = time.strftime("%Y-%b-%d_%H-%M-%S")
    run_directory_string = "Run_" + current_time

    run_directory = os.path.join(config['Output_Directory'],
                                 run_directory_string)
    os.mkdir(run_directory)

    return run_directory


def create_model_directory(run_directory, model_name):
    """Erstellen eines neuen Model-Directories."""

    model_directory = os.path.join(run_directory, model_name)
    os.mkdir(model_directory)

    return model_directory
