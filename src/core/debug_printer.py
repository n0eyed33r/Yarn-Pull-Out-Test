# src/core/debug_printer.py
import logging


class DebugPrinter:
    def __init__(self):
        self.logger = logging.getLogger('YarnPullout.debug')
        self._setup_logger()
    
    def _setup_logger(self):
        handler = logging.StreamHandler()
        formatter = logging.Formatter('%(message)s')  # Vereinfachtes Format
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.setLevel(logging.DEBUG)
    
    def print_progress(self, message: str):
        self.logger.debug(message)