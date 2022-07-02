# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Datei mit Funktionen zur Visualisierung des Datensets.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns


def show_scatterplot(x, y, data, title):
    plt.figure()
    sns.scatterplot(x=x, y=y, data=data)
    plt.title(title)
    plt.show()


def show_regressionplot(x, y, data, title, order=1):
    plt.figure()
    sns.regplot(x=x, y=y, data=data, order=order)
    plt.title(title)
    plt.show()


def savefig(save_directory, filename):
    plt.savefig(os.path.join(save_directory, filename))
