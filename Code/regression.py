# -*- coding: utf-8 -*-
"""
Erstellt am 02.07.2022

@author: Nils Heimbach, Christian T. Seidler

Funktionen zur Durchführung der Regression.
"""

import os
import pandas as pd
import statsmodels.formula.api as smf


def fit_regression_model(config, data):
    regression_model = smf.ols(formula=config['Formula'],
                               data=data).fit()

    return regression_model


def save_regression_results_as_csv(model, run_directory, filename):
    regression_results = {'parameter': model.params.to_list(),
                          'r2_score': model.rsquared
                          }
    filepath = os.path.join(run_directory, filename)
    with open(filepath, 'w') as f:
        for key in regression_results.keys():
            f.write("%s, %s\n" % (key, regression_results[key]))


def save_regression_summary_as_csv(model, run_directory, filename):
    results_as_html = model.summary().tables[1].as_html()
    df_summary = pd.read_html(results_as_html, header=0, index_col=0)[0]
    filepath = os.path.join(run_directory, filename)
    df_summary.to_csv(filepath)


def get_teil_zeitraum_from_config(value):
    teil_zeitraum = None
    zeitraum = value
    start_end = zeitraum.split('-')
    if len(start_end) > 1:
        start = int(start_end[0])
        end = int(start_end[1])
        teil_zeitraum = list(range(start, end+1))
    return teil_zeitraum
