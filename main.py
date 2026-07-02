import streamlit as st
import numpy as np
import plotly.graph_objects as go

# === Configuration de la page ===
st.set_page_config(
    page_title="OpticWaveSim",
    page_icon="🌊",
    layout="wide"
)

# === Titre principal ===
st.title("🌊 OpticWaveSim 1.1")
st.markdown("**Outil de Simulation d'Ondes Optiques** - Version améliorée avec atténuation réelle")

# === Sidebar (Panneau de contrôle) ===
with st.sidebar:
    st.header("⚙️ Paramètres de la Fibre")
    L = st.slider("Longueur de la fibre (km)", 1, 1000, 80, step=1)
    alpha = st.slider("Atténuation (dB/km)", 0.0, 1.0, 0.2, step=0.01)
    mode = st.radio(
        "Mode de simulation",
        ["Linear Propagation", "QPSK Constellation"],
        index=0
    )
    st.markdown("---")
    st.caption("Fait avec ❤️ + Grok AI")

# === Mode Linear Propagation (AMÉLIORÉ) ===
if mode == "Linear Propagation":
    st.subheader("📡 Propagation Linéaire")
    
    # === Calcul de l'atténuation RÉELLE ===
    total_loss_db = alpha * L                          # Perte totale en dB
    attenuation_factor = 10 ** (-total_loss_db / 20)   # Facteur d'amplitude (formule physique)
    
    # Signal d'entrée (pulse gaussien)
    t = np.linspace(-50, 50, 1000)
    signal_in = np.exp(-(t**2) / 10)
    
    # Signal de sortie avec atténuation réelle
    signal_out = signal_in * attenuation_factor
    
    # Affichage en deux colonnes
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Signal d'entrée**")
        fig1 = go.Figure()
        fig1.add_trace(go.Scatter(x=t, y=signal_in, name="Input", line=dict(color="blue")))
        fig1.update_layout(title="Signal avant la fibre", xaxis_title="Temps (ps)", yaxis_title="Amplitude")
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        st.write("**Signal de sortie**")
        fig2 = go.Figure()
        fig2.add_trace(go.Scatter(x=t, y=signal_out, name="Output", line=dict(color="red")))
        fig2.update_layout(title=f"Signal après {L} km", xaxis_title="Temps (ps)", yaxis_title="Amplitude")
        st.plotly_chart(fig2, use_container_width=True)
    
    # Résultats numériques
    st.success(f"✅ Perte totale : **{total_loss_db:.2f} dB** | Facteur d'atténuation : **{attenuation_factor:.4f}**")
    
    with st.expander("📚 Explication physique"):
        st.markdown(f"""
        - Atténuation totale = α × L = **{alpha}** × **{L}** = **{total_loss_db:.2f} dB**
        - Facteur d'amplitude = 10^(-perte/20)
        - Plus la fibre est longue ou l'atténuation élevée → le signal sort plus faible
        """)

# === Mode QPSK (placeholder pour l'instant) ===
else:
    st.subheader("📡 Constellation QPSK")
    st.info("🚧 Mode QPSK en cours de développement... On l'améliorera ensemble plus tard !")
    st.caption("Tu veux qu'on l'attaque tout de suite ? Dis-moi.")

# === Footer ===
st.markdown("---")
st.caption("Made with Grok AI • OpticWaveSim © 2026")
