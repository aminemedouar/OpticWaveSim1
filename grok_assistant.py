#!/usr/bin/env python3
"""
Grok Assistant Module - HYPERDRIVE ON
Integrated AI Assistant for OpticWaveSim
Handles chat, calculations, and optical physics explanations
"""

import re
from datetime import datetime
import json

class GrokAssistant:
    """
    Grok AI Assistant for OpticWaveSim
    Provides real-time assistance with optical simulations
    """
    
    def __init__(self):
        self.conversation_history = []
        self.knowledge_base = self._initialize_knowledge_base()
        self.calculation_context = {}
    
    def _initialize_knowledge_base(self):
        """Initialize optical physics knowledge base"""
        return {
            "planck_constant": 6.62607015e-34,  # J·s
            "speed_of_light": 299792458,  # m/s
            "electron_charge": 1.602176634e-19,  # C
            "wavelength_to_frequency": lambda wl: 299792458 / (wl * 1e-9),
            "frequency_to_wavelength": lambda f: 299792458 / (f * 1e12),
            "power_dbm_to_linear": lambda p: 10 ** (p / 10) / 1000,
            "power_linear_to_dbm": lambda p: 10 * np.log10(p * 1000),
        }
    
    def process_query(self, user_input, mode="chat"):
        """
        Process user query and generate response
        
        Args:
            user_input (str): User query
            mode (str): "chat", "calculation", or "explanation"
        
        Returns:
            str: Assistant response
        """
        self.conversation_history.append({
            "timestamp": datetime.now().isoformat(),
            "mode": mode,
            "user_input": user_input
        })
        
        if mode == "calculation":
            return self._handle_calculation(user_input)
        elif mode == "explanation":
            return self._handle_explanation(user_input)
        else:  # chat
            return self._handle_chat(user_input)
    
    def _handle_chat(self, query):
        """Handle general chat queries"""
        query_lower = query.lower()
        
        # Greeting
        if any(word in query_lower for word in ["hello", "hi", "hey", "salut", "bonjour"]):
            return "🤖 Bonjour! Je suis Grok, ton assistant IA pour OpticWaveSim. Comment puis-je t'aider avec tes simulations optiques? 🔷"
        
        # Help request
        if any(word in query_lower for word in ["help", "aide", "how", "comment"]):
            return """
🚀 **HYPERDRIVE ON - Grok Assistant Help**

Je peux t'aider avec:
• **Simulations optiques** - Tous les 6 modes disponibles
• **Calculs de physique** - Longueur d'onde, fréquence, puissance, atténuation
• **Explications** - Concepts fondamentaux de l'optique
• **Optimisation** - Meilleurs paramètres pour tes simulations
• **Troubleshooting** - Résoudre les problèmes techniques

💡 **Exemples:**
- "Convertis 1550nm en THz"
- "Explique la modulation QPSK"
- "Quel est le meilleur type de fibre pour 100km?"
- "Comment fonctionne l'effet Faraday?"
"""
        
        # Mode explanations
        if "mode" in query_lower and "1" in query:
            return "**Mode 1: Single Signal** - Analyse d'un signal optique unique avec visualisation temps/fréquence et polarisation. Parfait pour comprendre les propriétés de base des ondes optiques."
        
        if "mode" in query_lower and "2" in query:
            return "**Mode 2: Comparison** - Compare deux signaux différents et visualise leur superposition. Idéal pour étudier les battements et interférences."
        
        if "mode" in query_lower and "3" in query:
            return "**Mode 3: Modulation** - Simule les modulations numériques BPSK, QPSK et 16-QAM avec diagrammes de constellation et oeil."
        
        if "mode" in query_lower and "4" in query:
            return "**Mode 4: 3D Loss** - Optimise les pertes d'atténuation dans les fibres optiques sur longue distance. Supporte SMF-28, OM3, DSF."
        
        if "mode" in query_lower and "5" in query:
            return "**Mode 5: Young's Slit** - Simule le phénomène d'interférence à deux fentes de Young avec visualisation complète."
        
        if "mode" in query_lower and "6" in query:
            return "**Mode 6: Faraday Effect** - Démontre la rotation de polarisation sous influence d'un champ magnétique externe."
        
        # Fiber types
        if "fiber" in query_lower or "smf" in query_lower or "om3" in query_lower:
            return """
📡 **Types de Fibres Optiques:**

**SMF-28** (Single Mode)
- Atténuation: 0.2 dB/km @ 1550nm
- Distance max: ~200km sans répéteur
- Idéal pour: Télécoms longue distance

**OM3** (Multi-Mode)
- Atténuation: 3.0 dB/km
- Distance max: ~2km
- Idéal pour: LAN, centres de données

**DSF** (Dispersion Shifted)
- Atténuation: 0.18 dB/km @ 1550nm
- Distance max: ~250km
- Idéal pour: DWDM haute performance
"""
        
        # Default response
        return f"🤖 Grok: Je vais analyser ta question... '{query}'. Peux-tu être plus spécifique? Veux-tu une explication physique, un calcul, ou de l'aide avec un mode particulier?"
    
    def _handle_calculation(self, query):
        """Handle calculation queries"""
        query_lower = query.lower()
        
        # Wavelength to frequency
        wavelength_match = re.search(r'(\d+(?:\.\d+)?)\s*nm', query_lower)
        if "thz" in query_lower or "frequency" in query_lower:
            if wavelength_match:
                wl = float(wavelength_match.group(1))
                freq = self.knowledge_base["wavelength_to_frequency"](wl)
                return f"📊 **Calcul de Fréquence**\n\nLongueur d'onde: {wl} nm\n**Fréquence: {freq/1e12:.3f} THz**\n\n(Utilisé la formule: f = c/λ)"
        
        # Frequency to wavelength
        freq_match = re.search(r'(\d+(?:\.\d+)?)\s*(?:thz|ghz)', query_lower)
        if "wavelength" in query_lower or "nm" in query_lower:
            if freq_match:
                freq_val = float(freq_match.group(1))
                if "ghz" in query_lower:
                    freq_val = freq_val / 1000  # Convert to THz
                wl = self.knowledge_base["frequency_to_wavelength"](freq_val)
                return f"📊 **Calcul de Longueur d'Onde**\n\nFréquence: {freq_val:.3f} THz\n**Longueur d'onde: {wl:.2f} nm**\n\n(Utilisé la formule: λ = c/f)"
        
        # Power calculations
        if "power" in query_lower or "dbm" in query_lower:
            dbm_match = re.search(r'([+-]?\d+(?:\.\d+)?)\s*dbm', query_lower)
            if dbm_match:
                dbm = float(dbm_match.group(1))
                linear = self.knowledge_base["power_dbm_to_linear"](dbm)
                return f"📊 **Conversion Puissance**\n\nPuissance: {dbm} dBm\n**Puissance linéaire: {linear*1000:.3f} mW** ({linear:.3e} W)\n\n(Formule: P(W) = 10^(P(dBm)/10) / 1000)"
        
        # Default calculation response
        return f"🔢 Grok: Pour faire un calcul, indique les paramètres. Par exemple:\n- 'Convertis 1550nm en THz'\n- 'Quel est 0 dBm en watts?'\n- 'Atténuation sur 100km à 0.2dB/km?'"
    
    def _handle_explanation(self, query):
        """Handle explanation queries"""
        query_lower = query.lower()
        
        # Polarization
        if "polarization" in query_lower or "polarisation" in query_lower:
            return """
🔷 **Polarisation Optique**

La polarisation décrit l'orientation du champ électrique d'une onde lumineuse.

**Types:**
- **Linéaire**: Champ électrique oscille selon une direction fixe
- **Circulaire**: Le champ tourne circulairement (droit ou gauche)
- **Elliptique**: Cas général combinant les deux

**Importance:**
- Fondamentale pour QPSK et modulations optiques
- Affecte la transmission dans les fibres optiques
- Essentielle pour l'effet Faraday et les isolateurs optiques

**En Simulation:**
Mode 1 te permet d'explorer différentes polarisations et voir leur impact!
"""
        
        # Modulation
        if "modulation" in query_lower or "bpsk" in query_lower or "qpsk" in query_lower or "qam" in query_lower:
            return """
📡 **Modulation Digitale Optique**

Technique pour encoder des données numériques sur une porteuse optique.

**BPSK** (Binary Phase Shift Keying)
- 1 bit par symbole
- 2 états: 0° et 180°
- Débit: 1x symbolRate

**QPSK** (Quadrature Phase Shift Keying)
- 2 bits par symbole
- 4 états: 45°, 135°, 225°, 315°
- Débit: 2x symbolRate
- Standard pour 10 & 25 Gbps

**16-QAM** (16 Quadrature Amplitude Modulation)
- 4 bits par symbole
- 16 états (combinaisons amplitude/phase)
- Débit: 4x symbolRate
- Utilisation: 50 Gbps+
- Sensibilité: Demande meilleur SNR
"""
        
        # Fiber optics
        if "fiber" in query_lower or "atténuation" in query_lower or "dispersion" in query_lower:
            return """
🌐 **Optique Fibrée**

**Atténuation** (perte de puissance)
- Dépend de la longueur d'onde
- Minimum @ 1550nm (~0.2 dB/km pour SMF-28)
- S'exprime en dB/km

**Dispersion Chromatique**
- Différents longueurs d'onde voyagent à différentes vitesses
- Limite la distance et le débit
- Peut être compensée avec DSF ou DCM

**Mode Traditionnel vs Multi-mode**
- Single-mode: Longue distance, faible bande
- Multi-mode: Courte distance, haute bande

**Optimisation (Mode 4)**
Simule l'atténuation sur longue distance et aide à choisir les meilleurs paramètres!
"""
        
        # Interference
        if "interference" in query_lower or "young" in query_lower or "double slit" in query_lower:
            return """
🌊 **Interférence - Double Fente de Young**

Phénomène fondamental montrant la nature ondulatoire de la lumière.

**Principe:**
- Deux sources cohérentes créent deux ondes
- Constructive interference: Crêtes + Crêtes = Lumière forte
- Destructive interference: Crête + Creux = Noirceur

**Formules Clés:**
- Espacement des franges: Δy = λD/d
  - λ = longueur d'onde
  - D = distance à l'écran
  - d = séparation des fentes

**Mode 5** te permet d'explorer cette expérience classique avec paramètres variables!
"""
        
        # Faraday effect
        if "faraday" in query_lower or "magnéto-optique" in query_lower:
            return """
🧲 **Effet Faraday - Rotation de Polarisation**

Un champ magnétique externe peut faire tourner la polarisation d'une onde optique!

**Découverte:** Michael Faraday (1845)

**Formule:**
θ = V × B × L
- θ = angle de rotation (radians)
- V = constante de Verdet (rad/(T·m))
- B = champ magnétique (Tesla)
- L = longueur d'interaction (m)

**Applications:**
- Isolateurs optiques (unilatéraux)
- Gyroscopes à fibre optique
- Capteurs de courant
- Modulateurs magnéto-optiques

**Propriété Unique:** Non-réciproque! La rotation est toujours dans le même sens indépendamment de la direction de propagation.

**Mode 6** simule cet effet avec différents matériaux!
"""
        
        # Default explanation
        return """
📚 **Sujets d'Explication Disponibles:**

Je peux expliquer:
- Polarisation optique
- Modulation digitale (BPSK, QPSK, 16-QAM)
- Fibres optiques et atténuation
- Interférence et diffraction (Young)
- Effet Faraday
- Principes généraux d'optique

Pose ta question! 🔷
"""
    
    def get_conversation_summary(self):
        """Get summary of conversation"""
        return {
            "total_queries": len(self.conversation_history),
            "modes_used": [q.get("mode") for q in self.conversation_history],
            "history": self.conversation_history
        }

# Import numpy for calculations
import numpy as np
