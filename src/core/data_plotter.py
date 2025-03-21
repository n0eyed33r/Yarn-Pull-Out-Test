# src/core/data_plotter.py

import matplotlib.pyplot as plt
from src.core.data_analyzer import YarnPulloutAnalyzer


class YarnPulloutPlotter:
    def __init__(self):
        self.figure_size = (10, 7)
        self.dpi = 300
        self.setup_plot_style()

    def setup_plot_style(self):
        plt.style.use('default')  # Start with a clean slate

        # Achsen und Ticks
        plt.rcParams['axes.linewidth'] = 4  # Achsdicke
        plt.rcParams['xtick.major.width'] = 4  # Tickdicke x-Achse
        plt.rcParams['ytick.major.width'] = 4  # Tickdicke y-Achse
        plt.rcParams['xtick.major.size'] = 8 # Tick Länge x-Achse
        plt.rcParams['ytick.major.size'] = 8 # Tick Länge y-Achse
        plt.rcParams['xtick.minor.size'] = 4 # Tick Länge x-Achse
        plt.rcParams['ytick.minor.size'] = 4 # Tick Länge y-Achse

        # Schriftgrößen
        plt.rcParams['font.size'] = 22  # Standard-Textgröße (wird für Ticks verwendet)
        plt.rcParams['axes.labelsize'] = 24  # Achsenbeschriftung
        plt.rcParams['xtick.labelsize'] = 22  # Tick-Beschriftung x-Achse
        plt.rcParams["font.weight"] = "bold"
        plt.rcParams['ytick.labelsize'] = 22  # Tick-Beschriftung y-Achse
        plt.rcParams['axes.titlesize'] = 24  # Titelgröße

        # Linien
        plt.rcParams['lines.linewidth'] = 3  # Liniendicke der Messdaten


    def create_plot(self, analyzer: YarnPulloutAnalyzer, title: str) -> plt.Figure:
        fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

        ax.set_xlim(0, 4.05)
        ax.set_ylim(0, 2)

        ax.set_xlabel('Displacement [mm]', fontweight='bold', fontname='Arial') # Schriftgröße wird über rcParams gesetzt
        ax.set_ylabel('Force [kN]', fontweight='bold', fontname='Arial')  # Schriftgröße wird über rcParams gesetzt

        ax.set_xticks([0, 1, 2, 3, 4])
        #ax.tick_params(axis='both', labelsize=22, width=3) # width ist bereits global gesetzt
        ax.set_yticks([0, 0.5, 1, 1.5, 2])

        for i, measurement in enumerate(analyzer.measurements):
            x_values = [x for x, _ in measurement if x <= 4]
            y_values = [y for x, y in measurement if x <= 4]
            color = plt.cm.plasma(i / len(analyzer.measurements))
            ax.plot(x_values, y_values, color=color) # Linienstärke ist global gesetzt

        # ax.set_title(title, fontweight='bold', fontname='Arial') # Titel setzen
        plt.grid(True)
        plt.tight_layout()
        return fig