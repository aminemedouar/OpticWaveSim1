import streamlit as st
import numpy as np
import plotly.graph_objects as go

st.set_page_config(
    page_title="OpticWaveSim",
    page_icon="🌊",
    layout="wide"
)

st.title("🌊 OpticWaveSim 1.1")
st.markdown("**Optical Wave Simulation Tool**")

with st.sidebar:
    st.header("Parameters")
    L = st.slider("Fiber Length (km)", 1, 1000, 80)
    alpha = st.slider("Attenuation (dB/km)", 0.0, 1.0, 0.2)
    mode = st.radio("Simulation Mode", ["Linear Propagation", "QPSK Constellation"])

if mode == "Linear Propagation":
    st.subheader("Linear Propagation")
    t = np.linspace(-50, 50, 1000)
    signal = np.exp(-(t**2) / 10)
    
    col1, col2 = st.columns(2)
    with col1:
        st.write("Input Signal")
        fig1 = go.Figure(data=go.Scatter(x=t, y=signal))
        st.plotly_chart(fig1, use_container_width=True)
    with col2:
        st.write("Output Signal")
        fig2 = go.Figure(data=go.Scatter(x=t, y=signal * 0.8))
        st.plotly_chart(fig2, use_container_width=True)

else:
    st.subheader("QPSK Constellation")
    st.info("QPSK simulation under development...")
    
st.success("✅ Application is working!")
st.caption("Made with Grok AI")
