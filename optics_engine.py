"""
OpticWaveSim - Moteur de Simulation Optique Avancé
Équations NLSE, Split-Step Fourier, SPM, XPM
"""

import numpy as np
from scipy.integrate import odeint
from scipy.fft import fft, ifft, fftfreq
import warnings
warnings.filterwarnings('ignore')

class OpticalFiber:
    """Classe pour simuler la propagation en fibre optique"""
    
    def __init__(self, L=80, D=16.0, alpha=0.2, gamma=1.3, wavelength=1550e-9):
        """
        Args:
            L: Longueur fibre (km)
            D: Dispersion chromatique (ps/nm/km)
            alpha: Atténuation (dB/km)
            gamma: Coefficient non-linéaire (W^-1 km^-1)
            wavelength: Longueur d'onde (m)
        """
        self.L = L  # km
        self.D = D  # ps/nm/km
        self.alpha = alpha / 4.343  # conversion dB/km -> Np/km
        self.gamma = gamma  # W^-1 km^-1
        self.wavelength = wavelength
        self.c = 3e8  # vitesse lumière m/s
        
        # Calcul beta2 (dispersion parameter)
        self.beta2 = -D * 1.27e-3  # ps^2/km approx
        
    def split_step_fourier(self, pulse, t, num_steps=100, include_nonlinearity=True):
        """
        Résolution NLSE via méthode Split-Step Fourier
        
        ∂u/∂z + (α/2)u + (β2/2)∂²u/∂t² + γ|u|²u = 0
        
        Args:
            pulse: Impulsion d'entrée complexe
            t: Vecteur temps
            num_steps: Nombre d'étapes de propagation
            include_nonlinearity: Inclure effets non-linéaires
            
        Returns:
            pulse_out: Impulsion après propagation
        """
        dt = t[1] - t[0]
        dz = (self.L * 1000) / num_steps  # m
        
        # Fréquences
        freq = fftfreq(len(t), dt)
        omega = 2 * np.pi * freq
        
        # Opérateur linéaire dispersif
        D_op = np.exp(-self.alpha * dz / 2) * np.exp(1j * self.beta2 * dz / 2 * omega**2)
        
        u = pulse.copy()
        
        for _ in range(num_steps):
            # Demi-pas non-linéaire (domaine temps)
            if include_nonlinearity:
                u = u * np.exp(1j * self.gamma * np.abs(u)**2 * dz / 2)
            
            # Pas linéaire complet (domaine fréquence)
            u_f = fft(u)
            u_f = u_f * D_op
            u = ifft(u_f)
            
            # Demi-pas non-linéaire (domaine temps)
            if include_nonlinearity:
                u = u * np.exp(1j * self.gamma * np.abs(u)**2 * dz / 2)
        
        return u
    
    def linear_propagation(self, pulse, t):
        """Propagation linéaire simple (dispersion + atténuation)"""
        beta2 = self.beta2
        phase = beta2 * (self.L * 1000) * (t**2) / 2
        attenuation = np.exp(-self.alpha * self.L * 1000 / 2)
        return pulse * np.exp(1j * phase) * attenuation
    
    def calculate_eye_diagram(self, pulse, t, num_bits=128, bit_rate=10e9):
        """Génère un diagramme de l'oeil pour analyse BER"""
        bit_period = 1 / bit_rate
        samples_per_bit = len(t) // num_bits
        
        eye_data = []
        for i in range(num_bits - 1):
            start = i * samples_per_bit
            end = (i + 2) * samples_per_bit
            if end < len(pulse):
                eye_data.append(np.abs(pulse[start:end]))
        
        return np.array(eye_data) if eye_data else pulse


class QAMModulator:
    """Modulateur QAM/QPSK pour télécoms optiques"""
    
    @staticmethod
    def qpsk_modulate(bits):
        """Modulation QPSK 4-PSK"""
        symbols = []
        for i in range(0, len(bits), 2):
            b1, b0 = bits[i], bits[i+1] if i+1 < len(bits) else 0
            if b1 == 0 and b0 == 0:
                symbols.append((1 + 1j) / np.sqrt(2))
            elif b1 == 0 and b0 == 1:
                symbols.append((1 - 1j) / np.sqrt(2))
            elif b1 == 1 and b0 == 0:
                symbols.append((-1 + 1j) / np.sqrt(2))
            else:
                symbols.append((-1 - 1j) / np.sqrt(2))
        return np.array(symbols)
    
    @staticmethod
    def qam16_modulate(bits):
        """Modulation QAM-16"""
        mapping = {
            (0,0,0,0): (-3-3j), (0,0,0,1): (-3-1j), (0,0,1,0): (-3+3j), (0,0,1,1): (-3+1j),
            (0,1,0,0): (-1-3j), (0,1,0,1): (-1-1j), (0,1,1,0): (-1+3j), (0,1,1,1): (-1+1j),
            (1,0,0,0): (3-3j),  (1,0,0,1): (3-1j),  (1,0,1,0): (3+3j),  (1,0,1,1): (3+1j),
            (1,1,0,0): (1-3j),  (1,1,0,1): (1-1j),  (1,1,1,0): (1+3j),  (1,1,1,1): (1+1j),
        }
        symbols = []
        for i in range(0, len(bits), 4):
            key = tuple(bits[i:i+4])
            if len(key) == 4:
                symbols.append(mapping[key] / np.sqrt(10))
        return np.array(symbols)
    
    @staticmethod
    def demodulate_qpsk_with_noise(symbols, osnr_db):
        """Démodulation QPSK avec bruit AWGN"""
        snr = 10**(osnr_db / 10)
        noise_var = 1 / snr
        noise = np.random.normal(0, np.sqrt(noise_var/2), len(symbols)) + \
                1j * np.random.normal(0, np.sqrt(noise_var/2), len(symbols))
        noisy_symbols = symbols + noise
        return noisy_symbols


class ChannelImpairments:
    """Modèle des dégradations du canal optique"""
    
    @staticmethod
    def add_ase_noise(signal, osnr_db, bit_rate=10e9):
        """Ajoute bruit ASE (Amplified Spontaneous Emission)"""
        signal_power = np.mean(np.abs(signal)**2)
        noise_power = signal_power / (10**(osnr_db/10))
        noise = np.sqrt(noise_power/2) * (np.random.randn(len(signal)) + 
                                          1j * np.random.randn(len(signal)))
        return signal + noise
    
    @staticmethod
    def add_pmd(signal, t, dmd=0.5):
        """Polarization Mode Dispersion (ps)"""
        # Simule biréfringence de fibre
        delay_samples = int(dmd * 1e-12 / (t[1] - t[0]))
        if delay_samples > 0:
            signal_delayed = np.zeros_like(signal)
            signal_delayed[delay_samples:] = signal[:-delay_samples]
            return (signal + signal_delayed) / np.sqrt(2)
        return signal
    
    @staticmethod
    def add_phase_noise(signal, linewidth=1e6, num_samples=None):
        """Ajoute bruit de phase (laser linewidth)"""
        if num_samples is None:
            num_samples = len(signal)
        phase_noise = np.cumsum(np.random.normal(0, linewidth, num_samples))
        return signal * np.exp(1j * phase_noise)


class BERCalculator:
    """Calcul du Taux d'Erreur Bit"""
    
    @staticmethod
    def theoretical_ber_qpsk(osnr_db):
        """BER théorique QPSK"""
        from scipy.special import erfc
        snr = 10**(osnr_db/10)
        return 0.5 * erfc(np.sqrt(snr/2))
    
    @staticmethod
    def theoretical_ber_qam16(osnr_db):
        """BER théorique QAM-16"""
        from scipy.special import erfc
        snr = 10**(osnr_db/10)
        return (3/8) * erfc(np.sqrt(snr/5))
    
    @staticmethod
    def simulate_ber(symbols, osnr_db):
        """Simule BER par démodulation avec bruit"""
        noisy_symbols = symbols + np.sqrt(1/(2*10**(osnr_db/10))) * \
                       (np.random.randn(len(symbols)) + 1j*np.random.randn(len(symbols)))
        
        errors = 0
        for sym, noisy_sym in zip(symbols, noisy_symbols):
            # Détecteur optimal: distance minimale
            qpsk_constellation = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
            distances = np.abs(noisy_sym - qpsk_constellation)
            if distances.argmin() != np.abs(sym - qpsk_constellation).argmin():
                errors += 1
        
        return errors / len(symbols)
