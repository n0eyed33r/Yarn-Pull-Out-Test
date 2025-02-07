# src/core/excel_exporter.py
import pandas as pd
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional
from src.core.file_handler import FileHandler

class ExcelExporter:
    """Klasse für den Export von Analyseergebnissen nach Excel"""
    
    def __init__(self):
        self.results = {
            'Messreihe': [],
            'F_max [kN]': [],
            'F_max_std [kN]': [],
            'Mean Work [Nm]': [],
            'Work_std [Nm]': [],
            'Force Modulus': [],
            'Force Modulus_std': []
        }
    
    def add_measurement_series(self, name: str, stats: Dict) -> None:
        """
        Fügt eine Messreihe zu den Ergebnissen hinzu.

        Args:
            name: Name der Messreihe
            stats: Dictionary mit statistischen Werten
        """
        self.results['Messreihe'].append(name)
        self.results['F_max [kN]'].append(stats['max_force']['mean'])
        self.results['F_max_std [kN]'].append(stats['max_force']['std'])
        self.results['Mean Work [Nm]'].append(stats['work']['mean'])
        self.results['Work_std [Nm]'].append(stats['work']['std'])
        self.results['Force Modulus'].append(stats['modulus']['mean'])
        self.results['Force Modulus_std'].append(stats['modulus']['std'])
    
    def save_to_excel(self, save_path: Optional[Path] = None, initial_dir: Optional[Path] = None) -> Optional[Path]:
        """
        Speichert die Ergebnisse in einer Excel-Datei.

        Args:
            save_path: Optionaler Speicherpfad. Wenn None, wird nach einem Pfad gefragt.

        Returns:
            Path-Objekt zum gespeicherten File oder None bei Abbruch
        """
        if not save_path:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            default_name = f"YarnPullout_Ergebnisse_{timestamp}.xlsx"
            save_path = FileHandler.select_save_location(default_name, "Excel",
                                                         initial_dir=initial_dir)  # initial_dir hinzugefügt
        
        if save_path:
            df = pd.DataFrame(self.results)
            df.to_excel(save_path, index=False)
            return save_path
        return None