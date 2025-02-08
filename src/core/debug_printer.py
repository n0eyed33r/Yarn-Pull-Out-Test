# src/core/debug_printer.py
import logging
import sys


class DebugPrinter:
    def __init__(self):
        self.logger = logging.getLogger('YarnPullout')
        self._setup_logger()

    def _setup_logger(self):
        # Erstelle Handler für die Konsolenausgabe
        handler = logging.StreamHandler(sys.stdout)

        # Erstelle einen Formatter, der die Farbe basierend auf dem Log-Level setzt
        class ColorFormatter(logging.Formatter):
            grey = "\x1b[38;20m"
            yellow = "\x1b[33;20m"
            red = "\x1b[31;20m"
            reset = "\x1b[0m"

            FORMATS = {
                logging.DEBUG: grey + "%(message)s" + reset,
                logging.INFO: "%(message)s" + reset,
                logging.WARNING: yellow + "%(message)s" + reset,
                logging.ERROR: red + "%(message)s" + reset,
                logging.CRITICAL: red + "%(message)s" + reset
            }

            def format(self, record):
                log_fmt = self.FORMATS.get(record.levelno)
                formatter = logging.Formatter(log_fmt)
                return formatter.format(record)

        handler.setFormatter(ColorFormatter())
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.INFO)  # Standard-Level auf INFO setzen

    def print_progress(self, message: str):
        """Normale Fortschrittsmeldungen"""
        self.logger.info(message)

    def print_debug(self, message: str):
        """Detaillierte Debug-Informationen"""
        self.logger.debug(message)

    def print_warning(self, message: str):
        """Warnungen, die nicht kritisch sind"""
        self.logger.warning(message)

    def print_error(self, message: str):
        """Fehlermeldungen"""
        self.logger.error(message)