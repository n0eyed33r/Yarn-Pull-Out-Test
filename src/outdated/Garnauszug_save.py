import Garnauszug_config
import Garnauszug_plotten


def graphspeichern():
    # speicherformat
    saveformat = ".png"
    # speicherortangabe vorab
    savepath = "C:\\Users\\Tortelloni\\Google Drive\\02_Work_synch\\m" \
                  "isc\\03_Kooperationen\\2022_Koop_D01_Tobias" \
               "\\02_Ergebnisse\\Graphen\\Toni_py\\Traversenweg_2mm\\"
    # namensvergabe vorab
    foldername = Garnauszug_config.mainfolder
    last_slash_index = foldername.rfind('\\')
    if last_slash_index != -1:
        foldername = foldername[last_slash_index + 1:]
    # Dialog zum Auswählen des Speicherorts öffnen
    file_path = str(savepath) + str(foldername) \
                + str(saveformat)
    # Plotten des Graphen im Plot-Modul
    plt = \
        Garnauszug_plotten.dataplot()
    # Speichern des Graphen
    plt.savefig(file_path)
    plt.close()
