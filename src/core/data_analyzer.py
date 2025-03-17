# src/core/data_analyzer.py
from dataclasses import dataclass
from pathlib import Path
import numpy as np
import pandas as pd
from typing import List, Tuple, Dict, Optional
import logging


@dataclass
class YarnPulloutConfig:
    """Konfigurationsdaten für die Yarn Pull-Out Analyse"""
    data_ending: str = ".steps.tracking.csv"  # Dateiendung
    distance_limit: float = 2.5  # mm
    force_threshold_low: float = 0.2  # 20% für Modulberechnung
    force_threshold_high: float = 0.7  # 70% für Modulberechnung


class YarnPulloutAnalyzer:
    """Hauptklasse für die Analyse von Yarn Pull-Out Tests"""
    
    def __init__(self, config: YarnPulloutConfig = YarnPulloutConfig()):
        self.config = config
        self.measurements: List[List[Tuple[float, float]]] = []
        self.max_forces: List[float] = []
        self.force_moduli: List[float] = []
        self.total_work: List[Tuple[int, float]] = []
        self.logger = self._setup_logger()
        
        # Statistische Ergebnisse
        self.mean_max_force: Optional[float] = None
        self.force_stddev: Optional[float] = None
        self.mean_work: Optional[float] = None
        self.work_stddev: Optional[float] = None
        self.mean_force_modulus: Optional[float] = None
        self.force_modulus_stddev: Optional[float] = None
    
    def _setup_logger(self) -> logging.Logger:
        """Richtet das Logging ein"""
        logger = logging.getLogger('YarnPullout')
        logger.setLevel(logging.INFO)
        if not logger.handlers:
            handler = logging.StreamHandler()
            formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
            handler.setFormatter(formatter)
            logger.addHandler(handler)
        return logger
    
    def load_data(self, filepath: Path) -> None:
        """
        Lädt die Daten aus einer CSV-Datei.

        Args:
            filepath: Pfad zur CSV-Datei
        """
        try:
            dataset = pd.read_csv(
                filepath,
                sep=";",
                usecols=[7, 8],  # [x in mm, y in kN]
                decimal=',',
                encoding='utf-8'
            )
            
            # Normalisiere x-Werte (Weg)
            x_values = dataset.iloc[:, 0]
            x_offset = x_values.iloc[0]
            x_normalized = x_values - x_offset
            
            # Normalisiere y-Werte (Kraft)
            y_values = dataset.iloc[:, 1]
            y_offset = y_values.iloc[0]
            y_normalized = y_values - y_offset
            
            # Erstelle Liste von Tupeln
            measurement_data = [
                (round(float(x), 4), round(float(y), 4))
                for x, y in zip(x_normalized, y_normalized)
            ]
            
            self.measurements.append(measurement_data)
            # Finde maximale Kraft
            max_force = max(measurement_data, key=lambda x: x[1])[1]
            self.max_forces.append(max_force)
            
            self.logger.info(f"Daten erfolgreich geladen: {filepath.name}")
        
        except Exception as e:
            self.logger.error(f"Fehler beim Laden der Datei {filepath}: {str(e)}")
            raise
    
    def calculate_force_modulus(self) -> None:
        """
        Berechnet den Kraft-Modul für alle Messungen.

        Der Modul wird aus dem Anstieg zwischen 20% und 70% der Maximalkraft berechnet,
        wobei nur Datenpunkte VOR dem Erreichen der Maximalkraft berücksichtigt werden.
        Dies verhindert Verfälschungen durch mögliche Kraftanstiege nach dem ersten Maximum.
        """
        self.force_moduli = []
        
        for measurement, max_force in zip(self.measurements, self.max_forces):
            try:
                # Finde Punkt mit maximaler Kraft und dessen Index
                max_point = max(measurement, key=lambda point: point[1])
                max_force_index = measurement.index(max_point)
                
                # Berechne Schwellwerte
                threshold_20 = max_point[1] * self.config.force_threshold_low
                threshold_70 = max_point[1] * self.config.force_threshold_high
                
                # Initialisiere Indizes
                index_20 = None
                index_70 = None
                
                # Suche nur in Datenpunkten VOR dem Maximum
                for i, point in enumerate(measurement[:max_force_index]):
                    if point[1] >= threshold_20 and index_20 is None:
                        index_20 = i
                    if point[1] >= threshold_70 and index_70 is None:
                        index_70 = i
                
                # Überprüfe, ob beide Punkte gefunden wurden
                if index_20 is None or index_70 is None:
                    self.logger.warning("Nicht genügend Werte vor Maximalkraft für die Berechnung.")
                    self.force_moduli.append(0.0)
                    continue
                
                # Stelle sicher, dass index_20 kleiner ist als index_70
                if index_20 > index_70:
                    index_20, index_70 = index_70, index_20
                
                # Hole die entsprechenden Punkte
                point_20 = measurement[index_20]
                point_70 = measurement[index_70]
                
                # Berechne den Modul (Anstieg)
                modulus = (point_70[1] - point_20[1]) / (point_70[0] - point_20[0])
                self.force_moduli.append(round(modulus, 2))
                
                self.logger.debug(f"Modul berechnet: {modulus:.2f} "
                                  f"(20% bei {point_20}, 70% bei {point_70})")
            
            except Exception as e:
                self.logger.error(f"Fehler bei der Modulberechnung: {str(e)}")
                self.force_moduli.append(0.0)
    
    def calculate_work(self) -> None:
        """Berechnet die verrichtete Arbeit für alle Messungen"""
        self.total_work = []
        
        for i, measurement in enumerate(self.measurements):
            try:
                # Filtere Daten bis zum Distance Limit
                filtered_data = [
                    (x, y) for x, y in measurement
                    if x <= self.config.distance_limit
                ]
                
                if not filtered_data:
                    continue
                
                x_values = [x for x, _ in filtered_data]
                y_values = [y for _, y in filtered_data]
                
                # Berechne Integral
                work = np.trapezoid(y_values, x_values)
                self.total_work.append((i, round(work, 2)))
            
            except Exception as e:
                self.logger.error(f"Fehler bei der Arbeitsberechnung für Messung {i}: {str(e)}")
    
    def calculate_statistics(self) -> None:
        """Berechnet statistische Kennwerte"""
        try:
            # Maximalkraft-Statistiken
            if self.max_forces:
                self.mean_max_force = round(np.mean(self.max_forces), 2)
                self.force_stddev = round(np.std(self.max_forces), 2)
            
            # Arbeits-Statistiken
            if self.total_work:
                work_values = [work[1] for work in self.total_work]
                self.mean_work = round(np.mean(work_values), 2)
                self.work_stddev = round(np.std(work_values), 2)
            
            # Modul-Statistiken
            if self.force_moduli:
                self.mean_force_modulus = round(np.mean(self.force_moduli), 2)
                self.force_modulus_stddev = round(np.std(self.force_moduli), 2)
        
        except Exception as e:
            self.logger.error(f"Fehler bei der statistischen Berechnung: {str(e)}")
    
    def get_statistics(self) -> Dict:
        """
        Gibt alle statistischen Kennwerte zurück.

        Returns:
            Dictionary mit allen statistischen Kennwerten
        """
        return {
            'max_force': {
                'mean': self.mean_max_force,
                'std': self.force_stddev
            },
            'work': {
                'mean': self.mean_work,
                'std': self.work_stddev
            },
            'modulus': {
                'mean': self.mean_force_modulus,
                'std': self.force_modulus_stddev
            }
        }