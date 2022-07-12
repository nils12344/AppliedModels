# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zur Visualisierung der eingelesenen Daten.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


def show_scatterplot(x, y, data, title):
    """Erstellen und Anzeigen eines Scatterplots in einer neuen Figure."""

    plt.figure()
    sns.scatterplot(x=x, y=y, data=data)
    plt.title(title)
    plt.subplots_adjust(left=0.15, right=0.9, top=0.9, bottom=0.1)
    plt.show()


def show_regressionplot(x, y, data, title, order=1):
    """Erstellen und Anzeigen eines Regressionsplots in einer neuen Figure."""

    plt.figure()
    sns.regplot(x=x, y=y, data=data, order=order)
    plt.title(title)
    plt.show()


def savefig(save_directory, filename):
    """Abspeichern eines Plots unter dem angegebenen Verzeichnis."""

    plt.savefig(os.path.join(save_directory, filename))


def visualize_validation_sample(df_validation, predictions):
    """Visualisieren der Ergebnisse für das Validierungssample."""

    fig, axis = plt.subplots()
    axis.plot(df_validation['Total'], df_validation['Mean'], "o",
              label="True")
    axis.plot(df_validation['Total'], predictions, "o",
              label="Predictions")
    axis.legend(loc="best")
    plt.title('Visualization of the validation sample')
    plt.xlabel('Total')
    plt.ylabel('Mean')
    plt.show()


def visualize_regression_results(df, regression_model):
    """Visualisieren der Ergebnisse der Regression (gefittete Funktion,
    sowie die Datenpunkte)."""

    parameters = regression_model.params
    # Anlegen des Intervalls, in welchem die Regressionsgerade dargestellt
    # werden soll
    x = np.arange(df['Total'].min(), df['Total'].max())
    # Erzeugen des Scatterplots mit dem pd.DataFrame
    axis = df.plot(x='Total', y='Mean', kind='scatter')
    # Ergänzen der Regressionsgerade
    try:
        axis.plot(x, parameters.Intercept + parameters.Total * x, color='r')
    except AttributeError:
        axis.plot(x, parameters.Total * x, color='r')
    plt.title('Regression Results')
    plt.show()
