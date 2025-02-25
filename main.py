# src/main.py
from src.core.data_analyzer import YarnPulloutConfig, YarnPulloutAnalyzer
from src.core.data_plotter import YarnPulloutPlotter
from src.core.excel_exporter import ExcelExporter
from src.core.file_handler import FileHandler
from src.core.debug_printer import DebugPrinter
from pathlib import Path
import matplotlib.pyplot as plt
from typing import Optional
import shutil # Hinzugefügt für das Kopieren von Dateien


def process_measurement_series(folder_path: Path, analyzer: YarnPulloutAnalyzer, debug_printer: DebugPrinter) -> None:
    """Verarbeitet eine einzelne Messreihe."""
    measurement_folders = [f for f in folder_path.iterdir() if f.is_dir()]
    debug_printer.print_progress(f"Gefundene Messordner: {[f.name for f in measurement_folders]}")

    for meas_folder in measurement_folders:
        base_name = meas_folder.name
        csv_files = list(meas_folder.glob(f"{base_name}.steps.tracking.csv"))
        debug_printer.print_progress(f"Suche in {meas_folder.name} nach {base_name}.steps.tracking.csv")
        debug_printer.print_progress(f"Gefundene CSVs: {[f.name for f in csv_files]}")

        if csv_files:
            try:
                debug_printer.print_progress(f"Verarbeite: {csv_files[0].name}")
                analyzer.load_data(csv_files[0])
            except Exception as e:
                debug_printer.print_progress(f"Fehler beim Laden von {csv_files[0]}: {str(e)}")


def process_single_analysis(folder_path: Path, config: YarnPulloutConfig,
                            plotter: YarnPulloutPlotter, exporter: ExcelExporter,
                            debug_printer: DebugPrinter) -> Optional[bool]:
    """Führt die Analyse einer einzelnen Messreihe durch."""
    debug_printer.print_progress(f"Verarbeite Einzelanalyse für: {folder_path}")

    analyzer = YarnPulloutAnalyzer(config)
    process_measurement_series(folder_path, analyzer, debug_printer)

    if not analyzer.measurements:
        debug_printer.print_progress("Keine Messungen gefunden")
        return None

    debug_printer.print_progress(f"Anzahl geladener Messungen: {len(analyzer.measurements)}")

    try:
        analyzer.calculate_force_modulus()
        analyzer.calculate_work()
        analyzer.calculate_statistics()
        stats = analyzer.get_statistics()
        debug_printer.print_progress(f"Berechnete Statistiken: {stats}")
        exporter.add_measurement_series(folder_path.name, stats)

        debug_printer.print_progress("Wähle Speicherort für Excel-Datei...")
        excel_path = exporter.save_to_excel() # Speicherpfad ermitteln, *bevor* Plot-Ordner erstellt wird
        excel_saved = False # Flag, um zu merken, ob Excel gespeichert wurde
        if excel_path:
            debug_printer.print_progress(f"Excel-Datei gespeichert: {excel_path}")
            excel_saved = True # Excel wurde erfolgreich gespeichert


            try: # Plot-Ordner und Plot erst jetzt erstellen, wenn excel_path bekannt ist
                plot_folder_parent = excel_path.parent # Übergeordneter Ordner der Excel-Datei
                plot_folder = plot_folder_parent / "plots" # Plot-Ordner im selben Ordner wie Excel
                plot_folder.mkdir(exist_ok=True)
                plot_path = plot_folder / f"{folder_path.name}_analysis.png"
                figure = plotter.create_plot(analyzer, folder_path.name)
                figure.savefig(plot_path, dpi=300, bbox_inches='tight')
                plt.close(figure)
                debug_printer.print_progress(f"Plot gespeichert: {plot_path}")
            except Exception as e:
                debug_printer.print_progress(f"Fehler beim Plotting: {str(e)}")


            return excel_saved # Gib zurück, ob Excel gespeichert wurde

        else:  # falls der Benutzer den Speichern-Dialog abbricht
            return False

    except Exception as e:
        debug_printer.print_progress(f"Fehler bei der Berechnung: {str(e)}")
        return None


def process_multiple_analysis(parent_folder: Path, config: YarnPulloutConfig,
                              plotter: YarnPulloutPlotter, exporter: ExcelExporter,
                              debug_printer: DebugPrinter) -> Optional[bool]:
    """Führt die Analyse mehrerer Messreihen durch."""
    plot_dir_gesamt = parent_folder / "plots_gesamt" #  Plot-Ordner *gesamt* VOR der Schleife erstellen, damit er bereit ist
    plot_dir_gesamt.mkdir(exist_ok=True) # Erstelle den Ordner *gesamt* *vor* der Schleife!
    debug_printer.print_progress(f"Plot-Ordner (gesamt) erstellt: {plot_dir_gesamt}") # Debug-Ausgabe angepasst


    series_folders = [f for f in parent_folder.iterdir()
                      if f.is_dir() and not f.name == "plots" and not f.name == "plots_gesamt"] # "plots_gesamt" ausgeschlossen

    for folder in series_folders:
        debug_printer.print_progress(f"\nVerarbeite Messreihe: {folder.name}")
        analyzer = YarnPulloutAnalyzer(config)
        process_measurement_series(folder, analyzer, debug_printer)

        if analyzer.measurements:
            try:
                analyzer.calculate_force_modulus()
                analyzer.calculate_work()
                analyzer.calculate_statistics()
                stats = analyzer.get_statistics()
                exporter.add_measurement_series(folder.name, stats)

                # Plot-Erstellung *innerhalb* der Schleife (wie gehabt)
                try:
                    figure = plotter.create_plot(analyzer, folder.name)
                    plot_folder_serie = folder / "plots" # Plot-Ordner *pro Messreihe* (wie gehabt)
                    plot_folder_serie.mkdir(exist_ok=True)
                    plot_path = plot_folder_serie / f"{folder.name}_analysis.png"
                    figure.savefig(plot_path, dpi=300, bbox_inches='tight')
                    plt.close(figure)
                    debug_printer.print_progress(f"Plot gespeichert für {folder.name}: {plot_path}")

                    # NEU: Plot in den 'plots_gesamt' Ordner KOPIEREN
                    plot_path_gesamt = plot_dir_gesamt / f"{folder.name}_analysis.png" # Pfad für den 'gesamt' Plot
                    shutil.copy2(plot_path, plot_path_gesamt) # Kopiere den Plot in den 'gesamt' Ordner (copy2 kopiert auch Metadaten)
                    debug_printer.print_progress(f"Plot kopiert nach: {plot_path_gesamt}") # Debug-Ausgabe für das Kopieren

                except Exception as e:
                    debug_printer.print_progress(f"Fehler beim Plotting von {folder.name}: {str(e)}")

            except Exception as e:
                debug_printer.print_progress(f"Fehler bei der Verarbeitung von {folder.name}: {str(e)}")
                continue

    # Speichern der zusammenfassenden Excel-Datei (wie gehabt)
    if exporter.results['Messreihe']:
        debug_printer.print_progress("Wähle Speicherort für zusammengefasste Excel-Datei...")
        excel_path = exporter.save_to_excel()
        if excel_path:
            debug_printer.print_progress(f"Excel-Datei mit allen Messreihen gespeichert: {excel_path}")
            return True
        else:  # falls der Benutzer den Speichern-Dialog abbricht
            return False
    else:  # falls keine Ergebnisse vorhanden sind
        debug_printer.print_progress("Keine Ergebnisse zum Speichern in Excel.")
        return None


def main():
    """Hauptfunktion für die Yarn Pull-Out Analyse."""
    debug_printer = DebugPrinter()
    config = YarnPulloutConfig()
    plotter = YarnPulloutPlotter()
    exporter = ExcelExporter()

    try:
        debug_printer.print_progress("Starte Yarn Pull-Out Analyse")
        analysis_type = FileHandler.select_analysis_type()
        debug_printer.print_progress(f"Gewählter Analysetyp: {analysis_type}")

        if analysis_type == '1':
            folder_path = FileHandler.select_folder("Messreihe auswählen")
            if not folder_path:
                debug_printer.print_progress("Kein Ordner ausgewählt")
                return

            process_single_analysis(folder_path, config, plotter, exporter, debug_printer)

        else:
            parent_folder = FileHandler.select_folder("Zusammenfassungsordner auswählen")
            if not parent_folder:
                debug_printer.print_progress("Kein Ordner ausgewählt")
                return

            process_multiple_analysis(parent_folder, config, plotter, exporter, debug_printer)

    except Exception as e:
        debug_printer.print_progress(f"Fehler bei der Analyse: {str(e)}")


if __name__ == "__main__":
    main()