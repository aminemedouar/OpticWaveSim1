import numpy as np
from scipy.special import erfc

def calculate_ber(osnr_db):
    """Calcul BER approximatif pour QPSK
    
    Args:
        osnr_db: Optical Signal-to-Noise Ratio en dB
        
    Returns:
        float: Bit Error Rate
    """
    snr = 10**(osnr_db/10)
    return 0.5 * erfc(np.sqrt(snr/2))

def gaussian_pulse(t, width=10):
    """Génère une impulsion gaussienne
    
    Args:
        t: Vecteur temps
        width: Largeur de l'impulsion (ps)
        
    Returns:
        ndarray: Impulsion gaussienne normalisée
    """
    return np.exp(-(t/width)**2)

def calculate_dispersion(D, L, wavelength_span):
    """Calcul de la dispersion chromatique totale
    
    Args:
        D: Dispersion (ps/nm/km)
        L: Longueur fibre (km)
        wavelength_span: Largeur spectrale (nm)
        
    Returns:
        float: Dispersion totale (ps)
    """
    return D * L * wavelength_span

def calculate_attenuation(alpha, L, P_in_dbm):
    """Calcul de la puissance atténuée
    
    Args:
        alpha: Coefficient d'atténuation (dB/km)
        L: Longueur fibre (km)
        P_in_dbm: Puissance entrée (dBm)
        
    Returns:
        float: Puissance sortie (dBm)
    """
    return P_in_dbm - alpha * L

def generate_qpsk_symbols(n_symbols):
    """Génère des symboles QPSK aléatoires
    
    Args:
        n_symbols: Nombre de symboles à générer
        
    Returns:
        ndarray: Symboles QPSK complexes
    """
    bits = np.random.randint(0, 2, (n_symbols, 2))
    symbols = np.zeros(n_symbols, dtype=complex)
    for i in range(n_symbols):
        if bits[i, 0] == 0 and bits[i, 1] == 0:
            symbols[i] = (1 + 1j) / np.sqrt(2)
        elif bits[i, 0] == 0 and bits[i, 1] == 1:
            symbols[i] = (1 - 1j) / np.sqrt(2)
        elif bits[i, 0] == 1 and bits[i, 1] == 0:
            symbols[i] = (-1 + 1j) / np.sqrt(2)
        else:
            symbols[i] = (-1 - 1j) / np.sqrt(2)
    return symbols