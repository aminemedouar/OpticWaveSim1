"""
OpticWaveSim - Multi-Language Support (FR/EN/ES/DE/PT)
Full internationalization
"""

from typing import Dict, List

class Translator:
    """Translation manager"""
    
    TRANSLATIONS = {
        "global_params": {
            "fr": "Paramètres Globaux",
            "en": "Global Parameters",
            "es": "Parámetros Globales",
            "de": "Globale Parameter",
            "pt": "Parâmetros Globais"
        },
        "fiber_length": {
            "fr": "Longueur de la fibre (km)",
            "en": "Fiber Length (km)",
            "es": "Longitud de Fibra (km)",
            "de": "Faserlänge (km)",
            "pt": "Comprimento da Fibra (km)"
        },
        "attenuation": {
            "fr": "Atténuation (dB/km)",
            "en": "Attenuation (dB/km)",
            "es": "Atenuación (dB/km)",
            "de": "Dämpfung (dB/km)",
            "pt": "Atenuação (dB/km)"
        },
        "dispersion": {
            "fr": "Dispersion chromatique (ps/nm/km)",
            "en": "Chromatic Dispersion (ps/nm/km)",
            "es": "Dispersión Cromática (ps/nm/km)",
            "de": "Chromatische Dispersion (ps/nm/km)",
            "pt": "Dispersão Cromática (ps/nm/km)"
        },
        "power": {
            "fr": "Puissance d'entrée (dBm)",
            "en": "Input Power (dBm)",
            "es": "Potencia de Entrada (dBm)",
            "de": "Eingabeleistung (dBm)",
            "pt": "Potência de Entrada (dBm)"
        },
    }
    
    def __init__(self, language: str = "fr"):
        self.current_language = language.lower()[:2]
        if self.current_language not in ["fr", "en", "es", "de", "pt"]:
            self.current_language = "en"
    
    def translate(self, key: str) -> str:
        """Translate a key"""
        if key in self.TRANSLATIONS:
            return self.TRANSLATIONS[key].get(
                self.current_language,
                self.TRANSLATIONS[key].get("en", key)
            )
        return key
    
    def get_available_languages(self) -> List[str]:
        """List available languages"""
        return ["Français (fr)", "English (en)", "Español (es)", "Deutsch (de)", "Português (pt)"]

translator = Translator("fr")