# src/core/file_handler.py
import tkinter as tk
from tkinter import filedialog
from pathlib import Path
from typing import Optional


class FileHandler:
    """Klasse zur Verwaltung von Dateioperationen"""
    
    @staticmethod
    def select_analysis_type() -> str:
        """
        Zeigt ein Fenster zur Auswahl des Analysetyps
        Returns:'1' für Einzelanalyse, '2' für Mehrfachanalyse
        """
        root = tk.Tk()
        root.title("Yarn Pull-Out Analyzer - Analysetyp wählen")
        
        # Fenster in den Vordergrund
        root.lift()
        root.attributes('-topmost', True)
        
        # Fenster zentrieren
        window_width = 300
        window_height = 150
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        x = (screen_width / 2) - (window_width / 2)
        y = (screen_height / 2) - (window_height / 2)
        root.geometry(f'{window_width}x{window_height}+{int(x)}+{int(y)}')
        
        choice = tk.StringVar(value="1")
        
        tk.Label(root, text="Bitte Analysetyp wählen:").pack(pady=10)
        tk.Radiobutton(root, text="Einzelne Messreihe", variable=choice, value="1").pack()
        tk.Radiobutton(root, text="Alle Messreihen im Ordner", variable=choice, value="2").pack()
        
        result = []
        
        def on_button_click():
            result.append(choice.get())
            root.destroy()
        
        tk.Button(root, text="Bestätigen", command=on_button_click).pack(pady=20)
        
        root.mainloop()
        return result[0] if result else "1"
    
    @staticmethod
    def select_folder(title: str = "Ordner auswählen") -> Optional[Path]:
        """Öffnet einen Dialog zur Ordnerauswahl"""
        root = tk.Tk()
        root.withdraw()
        
        folder_path = filedialog.askdirectory(title=title)
        return Path(folder_path) if folder_path else None
    
    @staticmethod
    def select_save_location(default_name: str, file_type: str = "Excel", initial_dir: Optional[Path] = None) -> Optional[Path]:
        """Öffnet einen Dialog zur Auswahl des Speicherorts"""
        root = tk.Tk()
        root.withdraw()
        
        file_types = {
            "Excel": [("Excel files", "*.xlsx")],
            "PNG": [("PNG files", "*.png")]
        }
        
        file_path = filedialog.asksaveasfilename(
            defaultextension=".xlsx" if file_type == "Excel" else ".png",
            initialfile=default_name,
            filetypes=file_types[file_type],
            title=f"Speicherort für {file_type}-Datei wählen",
            initialdir=str(initial_dir) if initial_dir else None,  # initialdir hinzufügen
        )
        
        return Path(file_path) if file_path else None