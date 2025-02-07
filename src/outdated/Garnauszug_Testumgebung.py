import os
import tkinter as tk
from tkinter import filedialog
import numpy as np
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


def meanmaximalforce():
    yvalue = []
    for i in range(len(Garnauszug_config.kraftmaximum)):
        yvalue.append(float(Garnauszug_config.kraftmaximum[i]))
    mean = sum(yvalue) / len(yvalue)
    forceround = round(mean, 2)
    Garnauszug_config.meanmaxforce.append(forceround)
    Garnauszug_config.kraftstddev = round(np.std(Garnauszug_config.kraftmaximum),2)


def gesamtintegral():
    for i in range(len(Garnauszug_config.measurements)):
        x = []
        y = []
        # iterierbar
        listenarray = np.array(Garnauszug_config.measurements[i])
        for k in listenarray:
            # nur bis distancelimit die Arbeit auswerten
            if k[0] <= Garnauszug_config.distancelimit:
                x.append(k[0])
                y.append(k[1])
        xarray = np.array(x)
        yarray = np.array(y)
        integraltotal = np.trapz(yarray, xarray)
        Garnauszug_config.wtotal.append((i, round(integraltotal, 2)))
    secondval = [tup[1] for tup in Garnauszug_config.wtotal]
    Garnauszug_config.wstddev = round(np.std(secondval),2)

def maxforceslope():
    for measurement, maxforce in zip(
            Garnauszug_config.measurements, Garnauszug_config.kraftmaximum):
        # Finden Sie den Punkt mit dem maximalen y-Wert
        max_point = max(measurement, key=lambda point: point[1])
        # Finde den nächsten Index zum gewünschten 20%-Punkt
        index_20 = min(range(len(measurement)),
                       key=lambda i: abs(measurement[i][1] - max_point[1] * 0.2))
        # Finde den nächsten Index zum gewünschten 70%-Punkt
        index_70 = min(range(len(measurement)),
                       key=lambda i: abs(measurement[i][1] - max_point[1] * 0.7))
        if index_20 > index_70:
            index_20, index_70 =index_70, index_20
        # Die Punkte bei 20% und 70% von max_force
        point_20 = measurement[index_20]
        point_70 = measurement[index_70]
        #print(point_20,point_70)
        #print(index_points)
        # Den Anstieg (modulus) zwischen den beiden Punkten berechnen
        modulus = ((point_70[1] - point_20[1]) /
                   (point_70[0] - point_20[0]))  # y-Differenz / x-Differenz
        modulus = round(modulus, 2)
        print(str(point_70[1]) +"-"+ str(point_20[1]) +"/"+
              str(point_70[0]) +"-"+ str(point_20[0]) +"="+
              str((point_70[1] - point_20[1]) / (point_70[0] - point_20[0])))

        print("\n")
        #print("\n")
        Garnauszug_config.forcemodulus.append(modulus)  # Den berechneten Modulus zur Ergebnisliste hinzufügen


def meanwork():
    y = [i[1] for i in Garnauszug_config.wtotal]
    mean = sum(y) / len(y)
    meanround = round(mean, 2)
    Garnauszug_config.meanwork.append(meanround)



def maxforceslope_test():
    measurement = Garnauszug_config.measurements[6]  # Die 7. Messung (Index 6)
    maxforce = Garnauszug_config.kraftmaximum[6]  # Maximalkraft für die 7. Messung

    # Finden Sie den Punkt mit dem maximalen y-Wert
    max_point = max(measurement, key=lambda point: point[1])

    # Finde den nächsten Index zum gewünschten 20%-Punkt
    index_20 = min(range(len(measurement)),
                   key=lambda i: abs(measurement[i][1] - max_point[1] * 0.2))
    # Finde den nächsten Index zum gewünschten 70%-Punkt
    index_70 = min(range(len(measurement)),
                   key=lambda i: abs(measurement[i][1] - max_point[1] * 0.7))

    # Stelle sicher, dass index_20 kleiner oder gleich index_70 ist
    if index_20 > index_70:
        index_20, index_70 = index_70, index_20

    print(f"Measurement: {measurement}")
    print(f"Max point: {max_point}")
    print(f"Index 20: {index_20}")
    print(f"Index 70: {index_70}")

    # Die Punkte bei 20% und 70% von max_force
    point_20 = measurement[index_20]
    point_70 = measurement[index_70]
    print(f"Point 20: {point_20}")
    print(f"Point 70: {point_70}")

    # Den Anstieg (modulus) zwischen den beiden Punkten berechnen
    modulus = ((point_70[1] - point_20[1]) /
               (point_70[0] - point_20[0]))  # y-Differenz / x-Differenz
    modulus = round(modulus, 2)
    print(f"Modulus: {modulus}")


# Testumgebung aufrufen
maxforceslope_test()


