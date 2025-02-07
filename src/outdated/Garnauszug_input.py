import os
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import Garnauszug_config


def choosemainfoldername():
    root = tk.Tk()
    root.withdraw()
    mainfolder = \
        filedialog.askdirectory(
            title="Überordner auswählen").replace('/','\\')
    Garnauszug_config.mainfolder = mainfolder


# Funktion zur Vergleich von Tupeln anhand des x-Werts
def equilibriumfunction(tupel):
    return tupel[1]


def extractcolumns():
    for i in os.scandir(Garnauszug_config.mainfolder):
        if i.is_dir():
            Garnauszug_config.subfolder.append(i.name)
    for k in range(len(Garnauszug_config.subfolder)):
        dataset = pd.read_csv(str(Garnauszug_config.mainfolder) + "\\"
                              + str(Garnauszug_config.subfolder[k]) + "\\"
                              + str(Garnauszug_config.subfolder[k])
                              + str(Garnauszug_config.dataending), sep=";",
                              #wenn erste col > zweite col dann tupelliste aendern
                              usecols=[7, 8], # [x in mm, y in kN]
                              decimal=',')
        # erster Wert der Weg
        firstxvalue = dataset.iloc[:, 0].iloc[0]
        #print("erster x wert: " + str(firstxvalue))
        # einnullen x
        if firstxvalue < 0:
            dataset.iloc[:, 0] = dataset.iloc[:, 0] + abs(firstxvalue)
        elif firstxvalue > 0:
            dataset.iloc[:, 0] = dataset.iloc[:, 0] - firstxvalue
        else:
            pass
        # erster Wert des Kraft
        firstyvalue = dataset.iloc[:, 1].iloc[0]
        #print("erster y wert: " + str(firstyvalue))
        # einnullen y
        if firstyvalue < 0:
            dataset.iloc[:, 1] = dataset.iloc[:, 1] + abs(firstyvalue)
        elif firstyvalue > 0:
            dataset.iloc[:, 1] = dataset.iloc[:, 1] - firstyvalue
        else:
            pass
        #gute Rundungen
        tupleliste_k = [
            (round(x, 4), round(y, 4))
             for x, y in zip(dataset.iloc[:, 0], dataset.iloc[:, 1])
        ]
        tuplelistefloat_k = [
            (float(x), float(y))for x, y in tupleliste_k
        ]
        Garnauszug_config.measurements.append(tuplelistefloat_k)
        # Größten y-Wert finden
        maxyvalue = max(tuplelistefloat_k, key=equilibriumfunction)[1]
        Garnauszug_config.kraftmaximum.append(maxyvalue)
