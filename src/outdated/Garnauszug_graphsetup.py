import Garnauszug_config
import matplotlib.pyplot as plt
from matplotlib.ticker import MaxNLocator

dpi = 150  # gewünschte DPI
pxwidth = 1600  # gewünschte Breite (4:3)
pxheight = 1200  # gewünschte Höhe (4:3)

inchwidth = pxwidth / dpi  # Umrechnung der Pixelangaben in Zoll
inchheight = pxheight / dpi  # Umrechnung der Pixelangaben in Zoll


def graphsetup():
    # Figure und Achsen generieren
    fig, ax = plt.subplots(figsize=(inchwidth, inchheight), dpi=dpi)
    # Graph zuschneiden
    ax.axis([0, 4.05, 0, 2])
    # Beschriftung aka Labels Schriftart
    labelfont = {'fontname': 'Arial'}
    titlefont = {'fontname': 'Arial'}
    # Begrenzung der Anzahl der Ticks auf der Y-Achse
    ax.yaxis.set_major_locator(MaxNLocator(nbins=5))
    # Begrenzung der Anzahl der Ticks auf der X-Achse
    ax.xaxis.set_major_locator(MaxNLocator(nbins=4))
    ax.set_xticks([0, 1, 2, 3, 4])
    # Benennung der Achsen
    ax.set_xlabel(
        'Displacement [mm]',
        fontsize=28,
        fontweight='bold',
        **labelfont
    )
    ax.set_ylabel(
        'Force [kN]',
        fontsize=28,
        fontweight='bold',
        **labelfont
    )
    ax.tick_params(axis='both', labelsize=22, width=4)
    for tick in ax.get_xticklabels() + ax.get_yticklabels():
        tick.set_fontweight('bold')
    # Titelvergabe Detail
    foldername = Garnauszug_config.mainfolder
    last_slash_index = foldername.rfind('\\')
    if last_slash_index != -1:
        foldername = foldername[last_slash_index + 1:]
    strsplit = foldername.split('_')
    # Dateipfadabhängigkeit beachten!
    graphtitel = " ".join(strsplit)
    # Getitelt
    # Rahmen Details
    ax.spines["top"].set_linewidth(4)
    ax.spines["bottom"].set_linewidth(4)
    ax.spines["left"].set_linewidth(4)
    ax.spines["right"].set_linewidth(4)
    # Ticks Timmmyyyyy
    ax.tick_params(
        axis='x',
        labelsize=22,
        which='major',
        direction='out',
        width=4
    )
    ax.tick_params(
        axis='y',
        labelsize=22,
        which='major',
        direction='out',
        width=4
    )
    # Tight Layout hinzufügen
    plt.tight_layout()
"""
    ax.set_title(
        str(graphtitel),
        fontsize=15,
        fontweight='bold',
        **titlefont)
"""
