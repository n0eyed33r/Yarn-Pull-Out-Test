# src/core/data_plotter.py
from pathlib import Path  # Für die Pfadverwaltung der Plots
import matplotlib.pyplot as plt  # Hauptbibliothek für das Plotting
from typing import Dict  # Für Type Hints
from .data_analyzer import YarnPulloutAnalyzer  # Für den Zugriff auf die Analysedaten


class YarnPulloutPlotter:
	"""Klasse für das Plotten von Yarn Pull-Out Daten"""

	def __init__(self):
		self.figure_size = (16, 12)
		self.dpi = 150
		self.setup_plot_style()

	def setup_plot_style(self):
		"""Konfiguriert den grundlegenden Plot-Stil"""
		plt.style.use('default')
		plt.rcParams['lines.linewidth'] = 4
		plt.rcParams['axes.linewidth'] = 4
		plt.rcParams['xtick.major.width'] = 4
		plt.rcParams['ytick.major.width'] = 4

	def create_plot(self, analyzer: YarnPulloutAnalyzer, title: str) -> None:
		"""Erstellt einen Plot für die Yarn Pull-Out Daten"""
		fig, ax = plt.subplots(figsize=self.figure_size, dpi=self.dpi)

		# Achsenlimits
		ax.set_xlim(0, 4.05)
		ax.set_ylim(0, 2)

		# Achsenbeschriftungen
		ax.set_xlabel('Displacement [mm]', fontsize=28, fontweight='bold', fontname='Arial')
		ax.set_ylabel('Force [kN]', fontsize=28, fontweight='bold', fontname='Arial')

		# Ticks
		ax.set_xticks([0, 1, 2, 3, 4])
		ax.tick_params(axis='both', labelsize=22, width=4)

		# Plot Daten
		for i, measurement in enumerate(analyzer.measurements):
			x_values = [x for x, _ in measurement if x <= 4]
			y_values = [y for x, y in measurement if x <= 4]
			color = plt.cm.plasma(i / len(analyzer.measurements))
			ax.plot(x_values, y_values, color=color, linewidth=4)

		# Statistik-Text
		stats = analyzer.get_statistics()
		self._add_statistics_text(ax, stats)

		plt.tight_layout()

	def _add_statistics_text(self, ax, stats: Dict) -> None:
		"""Fügt statistische Informationen zum Plot hinzu"""
		text_props = {'ha': 'right', 'va': 'top', 'weight': 'bold',
		              'size': 24, 'transform': ax.transAxes}

		# Maximalkraft
		ax.text(0.97, 0.97,
		        f"F_max:\n{stats['max_force']['mean']} ± {stats['max_force']['std']} kN",
		        **text_props)

		# Arbeit
		ax.text(0.97, 0.82,
		        f"Work {analyzer.config.distance_limit} mm:\n"
		        f"{stats['work']['mean']} ± {stats['work']['std']} Nm",
		        **text_props)

		# Modul
		ax.text(0.97, 0.67,
		        f"Bond Modulus:\n{stats['modulus']['mean']} ± {stats['modulus']['std']}",
		        **text_props)