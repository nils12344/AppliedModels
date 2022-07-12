# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zur Initailisierung des Loggings.
"""

import logging
import os


def start_logger(config, run_directory):
    """Einstellen und Starten des Loggers im angegebenen Run-Directory."""

    logger = logging.getLogger()

    while logger.hasHandlers():
        logger.removeHandler(logger.handlers[0])

    logging.basicConfig(format='%(levelname)s:%(asctime)s %(message)s',
                        datefmt='%m/%d/%Y %I:%M:%S %p',
                        filename=os.path.join(run_directory,
                                              config['Log_Filename']),
                        level=logging.INFO)
