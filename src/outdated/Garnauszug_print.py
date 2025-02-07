import Garnauszug_config


def printconfig():
    print("Mainfolderpath: " + str(Garnauszug_config.mainfolder))
    print("Subfolderliste: " + str(Garnauszug_config.subfolder))
    print("Die Kräfte sind : " + str(Garnauszug_config.kraftmaximum))
    print("Die Durchschnittsarbeit ist: " + str(Garnauszug_config.meanwork))
    print("Die Daten: " + str(Garnauszug_config.measurements))


def printinput():
    #print(Garnauszug_config.measurements[0])
    #print(Garnauszug_config.forcemodulus)
    #print(Garnauszug_config.kraftmaximum)
    return 


def datacalculate():
    print("Measurements: " + str(Garnauszug_config.measurements[1]))
    print("Type: " + str(type(Garnauszug_config.measurements[1])))
    print("Länge: " + str(len(Garnauszug_config.measurements[1])))
