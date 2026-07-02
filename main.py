import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="OpticWaveSim", layout="wide", page_icon="🌊")

st.title("🌊 OpticWaveSim 1.1")
st.markdown("Simulation d'ondes optiques")

with st.sidebar:
    st.header("Paramètres")
    L = st.slider("Longueur de la fibre (km)", 1, 1000, 80)
    alpha = st.slider("Atténuation (dB/km)", 0.0, 1.0, 0.2)
    mode = st.radio("Mode de simulation", )

if mode == "Propagation Linéaire":
    st.subheader("Propagation Linéaire")
    t = np.linspace(-50, 50, 1000)
    signal = np.exp(-(t**2) / 10)
    col1, col2 = st.columns(2)
    with col1:
        st.write("Signal d'entrée")
        fig1 = go.Figure(data=go.Scatter(x=t, y=signal))
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.write("Signal de sortie")
        fig2 = go.Figure(data=go.Scatter(x=t, y=signal * 0.8))
        st.plotly_chart(fig2, use_container_width=True)
else:
    st.subheader("Constellation QPSK")
    st.info("Simulation QPSK en cours de développement...")
    st.success("Application fonctionnelle !")
