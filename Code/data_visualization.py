# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Datei mit Funktionen zur Visualisierung des Datensets.
"""

import os
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np


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


def visualize_validation_sample(df_validation, predictions):
    fig, ax = plt.subplots()
    ax.plot(df_validation['Total'], df_validation['Mean'], "o",
            label="True")
    ax.plot(df_validation['Total'], predictions, "o",
            label="Predictions")
    ax.legend(loc="best")
    plt.title('Visualization of the validation sample')
    plt.xlabel('Total')
    plt.ylabel('Mean')
    plt.show()


def visualize_regression_results(df, regression_model):
    parameters = regression_model.params
    # generate x-values for your regression line (two is sufficient)
    x = np.arange(df['Total'].min(), df['Total'].max())
    # scatter-plot data
    ax = df.plot(x='Total', y='Mean', kind='scatter')
    # plot regression line on the same axes, set x-axis limits
    try:
        ax.plot(x, parameters.Intercept + parameters.Total * x, color='r')
    except AttributeError:
        ax.plot(x, parameters.Total * x, color='r')
    plt.title('Regression Results')
    plt.show()
