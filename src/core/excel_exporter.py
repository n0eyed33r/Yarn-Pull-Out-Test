# src/core/excel_exporter.py
from pathlib import Path
import pandas as pd
import numpy as np
from datetime import datetime
import logging
from typing import Optional, Dict, List
from .data_analyzer import YarnPulloutAnalyzer


class YarnPulloutExcelExporter:
	"""
	Klasse zum Exportieren von Yarn Pull-Out Analyseergebnissen in Excel-Dateien.
	Erstellt verschiedene Tabellenblätter für unterschiedliche Aspekte der Analyse.
	"""

	def __init__(self):
		self.logger = self._setup_logger()

	def _setup_logger(self) -> logging.Logger:
		"""Richtet das Logging für den Excel-Export ein"""
		logger = logging.getLogger('YarnPullout.ExcelExporter')
		logger.setLevel(logging.INFO)
		if not logger.handlers:
			handler = logging.StreamHandler()
			formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
			handler.setFormatter(formatter)
			logger.addHandler(handler)
		return logger

	def export_results(self, analyzer: YarnPulloutAnalyzer, save_path: Path) -> None:
		"""
		Exportiert alle Analyseergebnisse in eine Excel-Datei.

		Args:
			analyzer: YarnPulloutAnalyzer-Instanz mit den Analyseergebnissen
			save_path: Pfad zum Speichern der Excel-Datei
		"""
		try:
			# Excel-Writer mit xlsxwriter Engine für bessere Formatierung
			with pd.ExcelWriter(save_path, engine='xlsxwriter') as writer:
				# Hauptergebnisse exportieren
				self._export_main_results(analyzer, writer)

				# Detaillierte Kraft-Daten exportieren
				self._export_force_data(analyzer, writer)

				# Arbeits-Daten exportieren
				self._export_work_data(analyzer, writer)

				# Rohdaten exportieren
				self._export_raw_data(analyzer, writer)

				# Formatierung anwenden
				self._apply_formatting(writer)

			self.logger.info(f"Excel-Datei erfolgreich gespeichert: {save_path}")

		except Exception as e:
			self.logger.error(f"Fehler beim Excel-Export: {str(e)}")
			raise

	def _export_main_results(self, analyzer: YarnPulloutAnalyzer,
	                         writer: pd.ExcelWriter) -> None:
		"""Exportiert die Hauptergebnisse in ein übersichtliches Tabellenblatt"""

		# Statistiken sammeln
		stats = analyzer.get_statistics()

		# DataFrame für Hauptergebnisse erstellen
		main_results = pd.DataFrame({
			'Parameter': [
				'Maximalkraft [kN]',
				'Standardabweichung Kraft [kN]',
				f'Arbeit bis {analyzer.config.distance_limit}mm [Nm]',
				'Standardabweichung Arbeit [Nm]',
				'Kraft-Modul [kN/mm]',
				'Standardabweichung Kraft-Modul [kN/mm]'
			],
			'Wert': [
				stats['max_force']['mean'],
				stats['max_force']['std'],
				stats['work']['mean'],
				stats['work']['std'],
				stats['modulus']['mean'],
				stats['modulus']['std']
			]
		})

		# Timestamp hinzufügen
		timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
		info_df = pd.DataFrame({
			'Information': ['Analysezeitpunkt'],
			'Wert': [timestamp]
		})

		# DataFrames in Excel schreiben
		main_results.to_excel(writer, sheet_name='Hauptergebnisse',
		                      index=False, startrow=1)
		info_df.to_excel(writer, sheet_name='Hauptergebnisse',
		                 index=False, startrow=len(main_results) + 3)

	def _export_force_data(self, analyzer: YarnPulloutAnalyzer,
	                       writer: pd.ExcelWriter) -> None:
		"""Exportiert detaillierte Kraftdaten"""

		# Maximalkräfte
		force_df = pd.DataFrame({
			'Messung': range(1, len(analyzer.max_forces) + 1),
			'Maximalkraft [kN]': analyzer.max_forces,
			'Kraft-Modul [kN/mm]': analyzer.force_moduli
		})

		# Statistiken
		force_stats = pd.DataFrame({
			'Statistik': ['Mittelwert', 'Standardabweichung',
			              'Minimum', 'Maximum', 'Median'],
			'Maximalkraft [kN]': [
				np.mean(analyzer.max_forces),
				np.std(analyzer.max_forces),
				np.min(analyzer.max_forces),
				np.max(analyzer.max_forces),
				np.median(analyzer.max_forces)
			],
			'Kraft-Modul [kN/mm]': [
				np.mean(analyzer.force_moduli),
				np.std(analyzer.force_moduli),
				np.min(analyzer.force_moduli),
				np.max(analyzer.force_moduli),
				np.median(analyzer.force_moduli)
			]
		})

		# In Excel schreiben
		force_df.to_excel(writer, sheet_name='Kraft-Analyse',
		                  index=False, startrow=1)
		force_stats.to_excel(writer, sheet_name='Kraft-Analyse',
		                     index=False, startrow=len(force_df) + 3)

	def _export_work_data(self, analyzer: YarnPulloutAnalyzer,
	                      writer: pd.ExcelWriter) -> None:
		"""Exportiert Arbeitsdaten"""

		# Arbeitsberechnungen
		work_values = [work[1] for work in analyzer.total_work]
		work_df = pd.DataFrame({
			'Messung': range(1, len(work_values) + 1),
			f'Arbeit bis {analyzer.config.distance_limit}mm [Nm]': work_values
		})

		# Statistiken
		work_stats = pd.DataFrame({
			'Statistik': ['Mittelwert', 'Standardabweichung',
			              'Minimum', 'Maximum', 'Median'],
			'Wert [Nm]': [
				np.mean(work_values),
				np.std(work_values),
				np.min(work_values),
				np.max(work_values),
				np.median(work_values)
			]
		})

		# In Excel schreiben
		work_df.to_excel(writer, sheet_name='Arbeits-Analyse',
		                 index=False, startrow=1)
		work_stats.to_excel(writer, sheet_name='Arbeits-Analyse',
		                    index=False, startrow=len(work_df) + 3)

	def _export_raw_data(self, analyzer: YarnPulloutAnalyzer,
	                     writer: pd.ExcelWriter) -> None:
		"""Exportiert die Rohdaten aller Messungen"""

		for i, measurement in enumerate(analyzer.measurements, 1):
			# Erstelle DataFrame für jede Messung
			df = pd.DataFrame(measurement, columns=['Weg [mm]', 'Kraft [kN]'])
			df.to_excel(writer, sheet_name=f'Rohdaten_Messung_{i}',
			            index=False)

	def _apply_formatting(self, writer: pd.ExcelWriter) -> None:
		"""Wendet Formatierung auf die Excel-Arbeitsmappe an"""
		workbook = writer.book

		# Definiere Formate
		header_format = workbook.add_format({
			'bold': True,
			'font_size': 12,
			'bg_color': '#CCCCCC',
			'border': 1
		})

		data_format = workbook.add_format({
			'font_size': 11,
			'border': 1
		})

		# Wende Formatierung auf alle Worksheets an
		for worksheet in writer.sheets.values():
			# Setze Spaltenbreite
			worksheet.set_column('A:Z', 15)

			# Formatiere Header
			worksheet.set_row(0, 20, header_format)

			# Formatiere Datenzellen
			last_row = worksheet.dim_rowmax
			last_col = worksheet.dim_colmax
			worksheet.conditional_format(1, 0, last_row, last_col, {
				'type': 'no_blanks',
				'format': data_format
			})


def create_excel_report(analyzer: YarnPulloutAnalyzer,
                        base_path: Path) -> Optional[Path]:
	"""
	Erstellt einen Excel-Bericht mit allen Analyseergebnissen.

	Args:
		analyzer: YarnPulloutAnalyzer-Instanz mit den Analyseergebnissen
		base_path: Basispfad für die Speicherung

	Returns:
		Path zur erstellten Excel-Datei oder None bei Fehler
	"""
	try:
		# Erstelle Zeitstempel für Dateinamen
		timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
		filename = f"YarnPullout_Analyse_{timestamp}.xlsx"
		save_path = base_path / filename

		# Erstelle und speichere Excel-Datei
		exporter = YarnPulloutExcelExporter()
		exporter.export_results(analyzer, save_path)

		return save_path

	except Exception as e:
		print(f"Fehler beim Erstellen des Excel-Reports: {str(e)}")
		return None