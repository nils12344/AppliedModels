# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Datei mit Funktionen zur Initialisierung.
"""

import json
import time
import os


def load_config(filepath):
    """Einlesen der Konfigurationsdatei aus angebenen Pfad."""

    with open(filepath, 'r') as c:
        config = json.load(c)
    return config


def create_run_directory(config):
    """Erstellen eines neue Run-Directories."""

    current_time = time.strftime("%Y-%b-%d_%H-%M-%S")
    run_directory_string = "Run_" + current_time

    Run_Directory = os.path.join(config['Output_Directory'],
                                 run_directory_string)
    os.mkdir(Run_Directory)

    return Run_Directory
