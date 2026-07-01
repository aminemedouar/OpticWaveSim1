# 🌊 OpticWaveSim 1.0 - Simulateur Optique World-Class

**Le meilleur simulateur open-source d'ondes optiques au monde** | Streamlit + Grok AI

## 🚀 Fonctionnalités

- ✅ **Propagation Linéaire** - Simulation de dispersion chromatique en fibre optique
- ✅ **Bruit ASE & BER** - Analyse du bruit et taux d'erreur bit avec courbes de performance
- ✅ **Modulation QPSK** - Simulation de modulation avancée avec constellation
- ✅ **Effets Non-Linéaires** - SPM, XPM et autres phénomènes (à compléter)
- ✅ **Assistant Grok IA** - Optimisations intelligentes en temps réel
- ✅ **Export PDF** - Rapports professionnels automatisés

## 📦 Installation

```bash
git clone https://github.com/aminemedouar/OpticWaveSim1.git
cd OpticWaveSim1
pip install -r requirements.txt
```

## 🎯 Utilisation

```bash
streamlit run main.py
```

Accédez à `http://localhost:8501` et explorez les simulations !

## 🔧 Dépendances

- **Streamlit** - Interface web interactive
- **Plotly** - Visualisations avancées et interactives
- **NumPy/SciPy** - Calculs scientifiques et statistiques
- **ReportLab** - Génération de rapports PDF professionnels
- **OptCommPy** - Simulations optiques avancées (optionnel)

## 📁 Structure du Projet

```
OpticWaveSim1/
├── main.py              # Application Streamlit principale
├── utils.py             # Fonctions utilitaires (BER, pulses, etc.)
├── requirements.txt     # Dépendances Python
└── README.md           # Documentation
```

## 🔬 Modes de Simulation

### 1. Propagation Linéaire
- Simulation de dispersion chromatique
- Atténuation en fibre optique
- Visualisation de l'élargissement d'impulsion

### 2. Bruit ASE & BER
- Courbe de performance BER vs OSNR
- Calcul approché pour QPSK
- Analyse interactive de dégradation

### 3. Modulation QPSK
- Constellation de symboles
- Génération de séquences aléatoires
- Codage bits-symboles

### 4. Effets Non-Linéaires
- SPM (Self-Phase Modulation)
- XPM (Cross-Phase Modulation)
- Compression de pulses

### 5. Assistant Grok IA
- Recommandations d'optimisation
- Analyse de scénarios complexes
- Suggestions intelligentes en temps réel

## 📊 Exemple de Résultats

**Mode Propagation Linéaire (L=80 km, D=16 ps/nm/km):**
- Impulsion d'entrée: gaussienne 10 ps
- Élargissement temporel observable
- Atténuation calculée automatiquement

**Mode BER:**
- BER @ 15 dB OSNR: ~1e-6
- Courbe de performance complète
- Seuil d'erreur défini

## 🛣️ Roadmap v1.1

- [ ] Intégration complète API Grok
- [ ] Simulations NDSF (Non-Dispersion Shifted Fiber)
- [ ] Mode multi-canal WDM (Wavelength Division Multiplexing)
- [ ] Optimisation par machine learning
- [ ] Exportation formats avancés (HDF5, NetCDF)
- [ ] Validation avec OptComm.jl
- [ ] Benchmark de performance

## 📈 Performance

- Simulations temps réel pour L < 2000 km
- Interface responsive et fluide
- Génération PDF instantanée
- Calculs vectorisés NumPy

## 📝 License

Open Source - Apache 2.0 License

---

**Créé par Amine Medouar** | Alimenté par Grok AI 🤖

**Contact:** [@aminemedouar](https://github.com/aminemedouar)