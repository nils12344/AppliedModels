# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Datei mit Funktionen zur Überprüfung auf Ausreißer (Spikes und Flats).
"""

import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from scipy import stats
import logging


def show_boxplot(y, data, title):
    plt.figure()
    sns.boxplot(y=y, data=data)
    plt.title(title)
    plt.show()


def show_histogramm(x, data, title, kde=True):
    plt.figure()
    sns.histplot(x=x, data=data, kde=kde)
    plt.title(title)
    plt.show()


def calc_and_print_outliers_with_z_score(data, column, threshold=3):
    z_scores = calc_outliers_with_z_score(data, column)
    print_outliers_from_z_score(z_scores, threshold, column)


def calc_outliers_with_z_score(data, column):
    z = np.abs(stats.zscore(data[column]))
    return z


def print_outliers_from_z_score(z_scores, threshold, column):
    print("Outliers in Column", column + ":", np.where(z_scores > threshold))
    logging.info("Anzahl der Ausreißer über dem Treshhold von %i sind %i .",
                 threshold, len(np.where(z_scores > threshold))-1)


def calc_and_print_outliers_with_iqr(data, column, threshold=1.5):
    upper, lower = calc_outliers_with_iqr(data, column, threshold)
    print_outliers_from_iqr(upper, lower, column)


def calc_outliers_with_iqr(data, column, threshold):
    q1, q3 = calc_q1_and_q3(data, column)
    iqr = q3 - q1
    # Above Upper bound
    upper = data[column] >= (q3 + threshold*iqr)
    # Below Lower bound
    lower = data[column] <= (q1 - threshold*iqr)
    logging.info('Anzahl der Ausreißer über dem Treshhold %i .', upper)
    logging.info("Anzahl der Ausreißer unter dem Treshhold %i .", lower)
    return upper, lower


def calc_q1_and_q3(data, column):
    q1 = np.percentile(data[column], 25, method='midpoint')
    q3 = np.percentile(data[column], 75, method='midpoint')
    return q1, q3


def print_outliers_from_iqr(upper, lower, column):
    print("Upper Outliers in Column", column + ":", np.where(upper))
    print("Lower Outliers in Column", column + ":", np.where(lower))


def print_num_of_flats(data, column, threshold=0):
    df = data.copy()
    df[column + '_diff'] = df[column].diff()
    print("Flats in column", column + ":",
          df[df[column + '_diff'].abs() <= threshold])
    logging.info('Die Anzahl an Flats der Spalte %s sind %i.', column,
                 len(df[df[column + '_diff'].abs() <= threshold]))
