import pytest
import numpy as np
from optics_engine import OpticalFiber, QAMModulator, BERCalculator, ChannelImpairments

def test_fiber_initialization():
    fiber = OpticalFiber(L=80, alpha=0.2)
    assert fiber.L == 80
    assert fiber.alpha > 0

def test_linear_propagation():
    fiber = OpticalFiber(L=10, alpha=0.2)
    t = np.linspace(-50, 50, 1000)
    pulse = np.exp(-(t**2) / 10)
    out = fiber.linear_propagation(pulse, t)
    assert len(out) == len(pulse)
    assert np.max(np.abs(out)) <= np.max(np.abs(pulse))

def test_qpsk_modulate():
    bits = [0,1,0,0,1,1]
    symbols = QAMModulator.qpsk_modulate(bits)
    assert len(symbols) == 3
    assert np.allclose(np.abs(symbols), 1.0, atol=0.01)

def test_ber_qpsk_theory():
    ber = BERCalculator.theoretical_ber_qpsk(20)
    assert 0 < ber < 1e-3

def test_add_ase_noise():
    signal = np.ones(100, dtype=complex)
    noisy = ChannelImpairments.add_ase_noise(signal, osnr_db=20)
    assert len(noisy) == len(signal)
