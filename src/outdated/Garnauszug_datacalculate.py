import numpy as np
import Garnauszug_config
import statistics

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
        # Finden Sie den Punkt mit dem maximalen y-Wert (maxforce)
        max_point = max(measurement, key=lambda point: point[1])

        # Finden Sie den Index des maxforce-Tupels
        maxforce_index = measurement.index(max_point)

        # Ermitteln Sie die Indizes für index_20 und index_70 basierend auf 20% und 70% von maxforce
        threshold_20 = max_point[1] * 0.2
        threshold_70 = max_point[1] * 0.7

        index_20 = None
        index_70 = None

        for i, point in enumerate(measurement[:maxforce_index]):
            if point[1] >= threshold_20 and index_20 is None:
                index_20 = i
            if point[1] >= threshold_70 and index_70 is None:
                index_70 = i

        if index_20 is None or index_70 is None:
            print("Nicht genügend Werte vor maxforce für die Berechnung.")
            continue

        # Stelle sicher, dass index_20 kleiner oder gleich index_70 ist
        if index_20 > index_70:
            index_20, index_70 = index_70, index_20

        # Die Punkte bei index_20 und index_70
        point_20 = measurement[index_20]
        point_70 = measurement[index_70]

        # Den Anstieg (modulus) zwischen den beiden Punkten berechnen
        modulus = (point_70[1] - point_20[1]) / (point_70[0] - point_20[0])
        modulus = round(modulus, 2)
        Garnauszug_config.forcemodulus.append(modulus)  # Den berechneten Modulus zur Ergebnisliste hinzufügen

def meanforecmodulus():
        Garnauszug_config.meanforcemodulus = (
            round(statistics.mean(Garnauszug_config.forcemodulus),2))
        print(Garnauszug_config.meanforcemodulus)
        Garnauszug_config.meanforcemodulusstddev = (
            round(statistics.stdev(Garnauszug_config.forcemodulus),2))
        print(Garnauszug_config.meanforcemodulusstddev)



def meanwork():
    y = [i[1] for i in Garnauszug_config.wtotal]
    mean = sum(y) / len(y)
    meanround = round(mean, 2)
    Garnauszug_config.meanwork.append(meanround)
