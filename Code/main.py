# -*- coding: utf-8 -*-
"""
Erstellt am 30.06.2022

@author: Nils Heimbach, Christian T. Seidler

Das Hauptskript. Soll später als Jupyter-Notebook umgesetzt werden.
"""
import pandas as pd

PATH = r"C:\Users\heimb\Desktop\Master\2. Semester\5. Python Applied Modells\Projektaufgabe\Datenquellen_Referat_Regression"
PATH_TEMP = PATH+"\\TemperaturZeitreihe.json"

df_temp = pd.read_json(PATH+"\\TemperaturZeitreihe.json")
df_co2 = pd.read_csv(PATH+"\\fossil-fuel-co2-emissions-by-nation.csv")

def main_nils():
    def read_json(PATH):
        df = pd.read_json(PATH)
        return df

    def extract_mean_GISTEMP(df):
        df = df[df["Source"] == "GISTEMP"]
        return df

    def monthly_temp_into_yearly_mean(df):
        yearly_mean = df.groupby(df['Date'].dt.strftime('%Y'))['Mean'].mean()
        return yearly_mean

    def float_into_df(FLOAT):
        df = pd.DataFrame(FLOAT)
        df = df.reset_index(level=0)
        return df

    def load_temp(path):
        df = read_json(path)
        df = extract_mean_GISTEMP(df)
        FLOAT = monthly_temp_into_yearly_mean(df)
        df = float_into_df(FLOAT)
        return df

    df = load_temp(PATH_TEMP)
    print(df)



def main_christian():
    pass


if __name__ == '__main__':
    main_nils()
    main_christian()
