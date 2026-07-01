import streamlit as st
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
import io
from utils import calculate_ber, gaussian_pulse

st.set_page_config(page_title="OpticWaveSim 🌊", layout="wide", page_icon="🌊", initial_sidebar_state="expanded")

st.title("🌊 OpticWaveSim 1.0 - Meilleur Simulateur Open Source Optique")
st.subheader("Simulation Télécoms Optiques + Grok AI Hyperdrive")

# Sidebar paramètres
with st.sidebar:
    st.header("Paramètres Globaux")
    L = st.slider("Longueur de la fibre (km)", 1, 2000, 80)
    alpha = st.slider("Atténuation (dB/km)", 0.0, 1.0, 0.2)
    D = st.slider("Dispersion chromatique (ps/nm/km)", -100.0, 100.0, 16.0)
    P_dbm = st.slider("Puissance d'entrée (dBm)", -20, 20, 0)
    mode = st.selectbox("Mode de Simulation", 
        ["Propagation Linéaire", "Bruit ASE & BER", "Modulation QPSK", "Effets Non-Linéaires", "Assistant Grok IA"])

# Simulation core
t = np.linspace(-100, 100, 2000)
pulse = gaussian_pulse(t, width=10)

if mode == "Propagation Linéaire":
    st.header("💡 Propagation Linéaire en Fibre Optique")
    
    # Dispersion simple
    beta2 = D * (-1.27e-3)  # conversion approx
    phase = beta2 * L * 1e3 * (t**2) / 2
    pulse_out = pulse * np.exp(1j * phase)
    
    # Atténuation
    attenuation = 10**(-alpha * L / 10)
    pulse_out *= np.sqrt(attenuation)
    
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Entrée", "Sortie après dispersion"))
    fig.add_trace(go.Scatter(x=t, y=np.abs(pulse), name="Amplitude Entrée", line=dict(color="blue")), row=1, col=1)
    fig.add_trace(go.Scatter(x=t, y=np.abs(pulse_out), name="Amplitude Sortie", line=dict(color="red")), row=1, col=2)
    fig.update_xaxes(title_text="Temps (ps)", row=1, col=1)
    fig.update_xaxes(title_text="Temps (ps)", row=1, col=2)
    st.plotly_chart(fig, use_container_width=True)
    
    # Statistiques
    col1, col2, col3 = st.columns(3)
    col1.metric("Longueur", f"{L} km")
    col2.metric("Atténuation totale", f"{alpha * L:.2f} dB")
    col3.metric("Puissance sortie", f"{P_dbm - alpha * L:.2f} dBm")

elif mode == "Bruit ASE & BER":
    st.header("🔊 Analyse Bruit ASE et Taux d'Erreur Bit")
    
    osnr_range = np.linspace(5, 25, 50)
    ber_values = [calculate_ber(osnr) for osnr in osnr_range]
    
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=osnr_range, y=ber_values, mode='lines+markers', name='BER', line=dict(color='darkred', width=3)))
    fig.update_layout(title="Courbe BER vs OSNR", xaxis_title="OSNR (dB)", yaxis_title="BER", yaxis_type="log")
    st.plotly_chart(fig, use_container_width=True)
    
    # Simulation interactive
    osnr_db = st.slider("OSNR de test (dB)", 5, 25, 15)
    ber = calculate_ber(osnr_db)
    st.success(f"✅ BER à {osnr_db} dB: **{ber:.2e}**")

elif mode == "Modulation QPSK":
    st.header("📊 Modulation QPSK (Quadrature Phase Shift Keying)")
    st.info("Mode Modulation QPSK - Implémentation en cours")
    
    # Constellation QPSK
    symbols = np.array([1+1j, 1-1j, -1+1j, -1-1j]) / np.sqrt(2)
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=symbols.real, y=symbols.imag, mode='markers+text', text=['00', '01', '10', '11'],
                            marker=dict(size=15, color='blue')))
    fig.update_layout(title="Constellation QPSK", xaxis_title="I (In-phase)", yaxis_title="Q (Quadrature)", 
                     xaxis=dict(scaleanchor="y", scaleratio=1), yaxis=dict(scaleanchor="x", scaleratio=1))
    st.plotly_chart(fig, use_container_width=True)

elif mode == "Effets Non-Linéaires":
    st.header("⚡ Effets Non-Linéaires (SPM, XPM)")
    st.info("Mode Effets Non-Linéaires - À implémenter avec OptCommPy")
    
    # Placeholder pour SPM
    gamma = st.slider("Coefficient non-linéaire γ (W⁻¹km⁻¹)", 0.5, 3.0, 1.3)
    st.write(f"Configuration: γ = {gamma} W⁻¹km⁻¹")

elif mode == "Assistant Grok IA":
    st.header("🤖 Assistant Grok IA")
    st.info("🧠 Assistant Grok IA - Intégration API en cours de déploiement")
    user_query = st.text_area("Posez une question sur la simulation optique:")
    if st.button("Envoyer à Grok"):
        st.write(f"Query envoyée: {user_query}")

# Export PDF
st.divider()
st.subheader("📄 Export et Rapports")

if st.button("📄 Exporter Rapport PDF Professionnel"):
    buffer = io.BytesIO()
    c = canvas.Canvas(buffer, pagesize=letter)
    c.setFont("Helvetica-Bold", 16)
    c.drawString(100, 750, "Rapport de Simulation OpticWaveSim 1.0")
    c.setFont("Helvetica", 12)
    c.drawString(100, 700, f"Longueur fibre : {L} km")
    c.drawString(100, 680, f"Dispersion : {D} ps/nm/km")
    c.drawString(100, 660, f"Atténuation : {alpha} dB/km")
    c.drawString(100, 640, f"Puissance entrée : {P_dbm} dBm")
    c.drawString(100, 620, f"Mode : {mode}")
    c.save()
    buffer.seek(0)
    st.download_button("⬇️ Télécharger le PDF", buffer, f"OpticWaveSim_Report_{mode}.pdf", "application/pdf")

st.divider()
st.success("✅ Simulation terminée ! Grok AI prêt pour optimisations avancées.")
st.caption("🌍 Projet open source - Amélioré par Grok pour devenir la référence mondiale")