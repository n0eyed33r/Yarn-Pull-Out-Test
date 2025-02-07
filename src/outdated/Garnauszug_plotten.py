import Garnauszug_config
import matplotlib.pyplot as plt

def dataplot():
    # Iterieren über jedes Dataset
    for i, data in enumerate(Garnauszug_config.measurements):
        # falls nur ein Graph anzuschauen ist if an und bist plt.plot einrücken
        #if i == 0:
        # Extrahieren der x- und y-Werte aus den Tupeln
        x_values = [tupel[0] for tupel in data]  # Weg
        y_values = [tupel[1] for tupel in data]  # Kraft
        # Filtern der Daten, um nur x-Werte kleiner oder gleich 4 zu behalten
        filtered_x_values = [x for x in x_values if x <= 4]
        filtered_y_values = [y for x, y in zip(x_values, y_values) if x <= 4]
        # Farbverlauf definieren
        # Farbverlauf basierend auf 'plasma' oder 'summer' colormap
        color = plt.cm.plasma(i / len(Garnauszug_config.measurements))
        # Plotten der Daten
        plt.plot( filtered_x_values, filtered_y_values, linewidth = 4,color=color)
        # Anzeigen des Graphen
    #plt.show()
    return plt

'''
plt.text(0.97, 0.97,
                 f"F_max:\n"
                 f"{str(Garnauszug_config.meanmaxforce).replace('[',' ').replace(']',' ')}"
                 f"\u00B1 "
                 f"{str(Garnauszug_config.kraftstddev)}  kN",
                 ha='right', va='top', weight='bold', size=24,
                 transform=plt.gca().transAxes
                 )
        plt.text(0.97, 0.82,
                 f"Work "
                 f"{Garnauszug_config.distancelimit}"
                 f" mm:\n"
                 f"{str(Garnauszug_config.meanwork).replace('[',' ').replace(']',' ')}"
                 f"\u00B1 "
                 f"{str(Garnauszug_config.wstddev)} Nm",
                 ha='right', va='top', weight='bold', size=24,
                 transform=plt.gca().transAxes
                 )
        plt.text(0.97, 0.67,
                 f"Bond Modulus:\n"
                 f" {str(Garnauszug_config.meanforcemodulus).replace('[',' ').replace(']',' ')}"
                 f" \u00B1 "
                 f"{str(Garnauszug_config.meanforcemodulusstddev)} ",
                 ha='right', va='top', weight='bold', size=24,
                 transform=plt.gca().transAxes
                 )
'''
