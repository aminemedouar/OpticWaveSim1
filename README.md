#!/usr/bin/env python3
"""
OpticWaveSim - GitHub Upload Guide PDF Generator
Creates a clean, mobile-friendly PDF with everything needed to publish on GitHub
"""

from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import cm, mm
from reportlab.lib.colors import HexColor, black, white
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, PageBreak, 
    Table, TableStyle, Preformatted, KeepTogether
)
from reportlab.lib.enums import TA_CENTER, TA_LEFT, TA_JUSTIFY
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
import os

# Output path
output_path = "/home/workdir/artifacts/OpticWaveSim_GitHub_Upload_Guide.pdf"

# Colors (matching the app style)
PRIMARY = HexColor("#00d4ff")
SECONDARY = HexColor("#7a2ff4")
ACCENT = HexColor("#f72585")
DARK_BG = HexColor("#0a0e27")
TEXT_COLOR = HexColor("#e0e0e0")
CODE_BG = HexColor("#1a1f3a")

def create_pdf():
    doc = SimpleDocTemplate(
        output_path,
        pagesize=A4,
        rightMargin=1.5*cm,
        leftMargin=1.5*cm,
        topMargin=1.5*cm,
        bottomMargin=1.5*cm
    )
    
    styles = getSampleStyleSheet()
    
    # Custom styles
    title_style = ParagraphStyle(
        'CustomTitle',
        parent=styles['Title'],
        fontSize=24,
        textColor=PRIMARY,
        spaceAfter=20,
        alignment=TA_CENTER,
        fontName='Helvetica-Bold'
    )
    
    heading1_style = ParagraphStyle(
        'CustomH1',
        parent=styles['Heading1'],
        fontSize=16,
        textColor=PRIMARY,
        spaceBefore=20,
        spaceAfter=10,
        fontName='Helvetica-Bold'
    )
    
    heading2_style = ParagraphStyle(
        'CustomH2',
        parent=styles['Heading2'],
        fontSize=13,
        textColor=SECONDARY,
        spaceBefore=15,
        spaceAfter=8,
        fontName='Helvetica-Bold'
    )
    
    body_style = ParagraphStyle(
        'CustomBody',
        parent=styles['Normal'],
        fontSize=10,
        textColor=black,
        spaceAfter=8,
        alignment=TA_JUSTIFY,
        leading=14
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Code'],
        fontSize=8,
        fontName='Courier',
        backColor=HexColor("#f5f5f5"),
        borderColor=HexColor("#cccccc"),
        borderWidth=0.5,
        borderPadding=6,
        spaceAfter=10,
        leading=10
    )
    
    highlight_style = ParagraphStyle(
        'Highlight',
        parent=styles['Normal'],
        fontSize=10,
        textColor=HexColor("#d32f2f"),
        fontName='Helvetica-Bold',
        spaceAfter=6
    )
    
    story = []
    
    # ========== PAGE 1: Title & Quick Start ==========
    story.append(Paragraph("🔷 OpticWaveSim", title_style))
    story.append(Paragraph("Guide d'Upload sur GitHub - 01/07/2026", ParagraphStyle(
        'Subtitle', parent=styles['Normal'], fontSize=12, alignment=TA_CENTER, textColor=HexColor("#666666")
    )))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph(
        "<b>Code source complet</b> • 3 fichiers Python • Prêt pour GitHub",
        ParagraphStyle('Center', parent=body_style, alignment=TA_CENTER)
    ))
    story.append(Spacer(1, 20))
    
    # Quick steps box
    story.append(Paragraph("📋 ÉTAPES RAPIDES (3 minutes)", heading1_style))
    
    steps = """
    <b>1.</b> Crée un nouveau repo sur GitHub → <b>github.com/new</b><br/>
    <b>2.</b> Nom : <b>OpticWaveSim</b> • Public • Ajoute README<br/>
    <b>3.</b> Dans le repo → <b>Add file → Upload files</b><br/>
    <b>4.</b> Upload les 3 fichiers .py depuis le PDF original<br/>
    <b>5.</b> Upload README.md + requirements.txt + .gitignore (ci-dessous)<br/>
    <b>6.</b> Commit → Push → C'est en ligne !
    """
    story.append(Paragraph(steps, body_style))
    story.append(Spacer(1, 15))
    
    # Important note
    story.append(Paragraph(
        "⚠️ <b>IMPORTANT</b> : Le fichier PDF original <b>OpticWaveSim_Code_Source.pdf</b> contient déjà tout le code source complet (app.py + grok_assistant.py + translations.py). Ouvre-le et copie les 3 fichiers Python depuis les pages correspondantes.",
        highlight_style
    ))
    
    story.append(PageBreak())
    
    # ========== PAGE 2: README.md ==========
    story.append(Paragraph("📄 README.md (à uploader)", heading1_style))
    story.append(Paragraph("Copie tout le bloc ci-dessous dans un fichier nommé <b>README.md</b>", body_style))
    story.append(Spacer(1, 8))
    
    readme_content = """# 🔷 OpticWaveSim

**Simulation professionnelle d'ondes optiques**  
Interface Streamlit moderne + **Assistant IA Grok (HYPERDRIVE ON)**

> Code source complet • 6 modes de simulation • 7 langues (RTL arabe) • Exports PDF & partage social

## ✨ Fonctionnalités

- **6 modes** : Signal unique, Comparaison, Modulation (BPSK/QPSK/16-QAM), Optimisation pertes 3D, Double fente de Young, Effet Faraday
- **Assistant Grok intégré** dans la sidebar (chat, calculs, explications)
- **7 langues** complètes (FR/EN/ES/IT/AR avec RTL/DE/NL)
- Design futuriste (gradients, boutons flottants, animations)
- Exports **PDF pro** avec graphiques + **CSV**
- Partage instantané **WhatsApp** & **Telegram**
- Mode Low-Res optimisé pour mobile
- Préréglages réalistes de fibres (SMF-28, OM3, DSF)

## 🚀 Installation rapide

```bash
git clone https://github.com/aminemedouar/OpticWaveSim.git
cd OpticWaveSim
pip install -r requirements.txt
streamlit run app.py
```

Ouvre http://localhost:8501

## 📦 Fichiers inclus

| Fichier              | Description                        | Lignes |
|----------------------|------------------------------------|--------|
| app.py               | Application Streamlit principale   | ~2970  |
| grok_assistant.py    | Module HYPERDRIVE ON (Grok AI)     | 266    |
| translations.py      | Système multilingue (7 langues)    | 1214   |

## 📜 Licence

Apache License 2.0 – 100% libre

## 👤 Auteur

**@AmineMedouar** – 01/07/2026

> L'homme crée l'IA. L'IA aide l'homme à créer plus librement.
"""
    
    # Use Preformatted for code block
    story.append(Preformatted(readme_content, code_style))
    
    story.append(PageBreak())
    
    # ========== PAGE 3: requirements.txt + .gitignore ==========
    story.append(Paragraph("📦 requirements.txt (à uploader)", heading1_style))
    story.append(Paragraph("Crée un fichier nommé <b>requirements.txt</b> avec ce contenu :", body_style))
    story.append(Spacer(1, 6))
    
    req_content = """streamlit>=1.35.0
numpy>=1.26.0
matplotlib>=3.8.0
plotly>=5.20.0
scipy>=1.13.0
reportlab>=4.2.0
Pillow>=10.3.0
pandas>=2.2.0"""
    story.append(Preformatted(req_content, code_style))
    story.append(Spacer(1, 15))
    
    story.append(Paragraph("📄 .gitignore (à uploader)", heading1_style))
    story.append(Paragraph("Crée un fichier nommé <b>.gitignore</b> avec ce contenu :", body_style))
    story.append(Spacer(1, 6))
    
    gitignore_content = """__pycache__/
*.py[cod]
*.so
.env
.streamlit/secrets.toml
.DS_Store
*.png
*.pdf
attached_assets/"""
    story.append(Preformatted(gitignore_content, code_style))
    story.append(Spacer(1, 20))
    
    # Final instructions
    story.append(Paragraph("✅ Après upload", heading2_style))
    story.append(Paragraph(
        "Une fois les fichiers uploadés sur GitHub, ton repo sera public et prêt. Tu pourras ensuite ajouter des screenshots depuis le PDF original si tu veux embellir le README.",
        body_style
    ))
    
    story.append(Spacer(1, 15))
    story.append(Paragraph(
        "🚀 Besoin d'aide pour améliorer le code, ajouter des features ou générer des visuels ? Reviens me le dire !",
        ParagraphStyle('Footer', parent=body_style, textColor=PRIMARY, alignment=TA_CENTER)
    ))
    
    # Build PDF
    doc.build(story)
    print(f"✅ PDF créé avec succès : {output_path}")
    return output_path

if __name__ == "__main__":
    create_pdf()
