import Garnauszug_datacalculate
import Garnauszug_input
import Garnauszug_plotten
import Garnauszug_graphsetup
import Garnauszug_print
import Garnauszug_save


if __name__ == "__main__":
    Garnauszug_input.choosemainfoldername()
    Garnauszug_input.extractcolumns()
    Garnauszug_datacalculate.gesamtintegral()
    Garnauszug_datacalculate.meanmaximalforce()
    Garnauszug_datacalculate.meanwork()
    Garnauszug_datacalculate.maxforceslope()
    Garnauszug_datacalculate.meanforecmodulus()
    Garnauszug_graphsetup.graphsetup()
    Garnauszug_plotten.dataplot()
    Garnauszug_save.graphspeichern()
    #Garnauszug_print.printinput()

