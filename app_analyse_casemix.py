#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Dashboard Casemix GHM - Version optimisée
Analyse des données hospitalières 2022-2024
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from pathlib import Path
import numpy as np
import json
import base64

# Configuration de la page
st.set_page_config(
    page_title="Casemix Dashboard",
    page_icon="assets/3xS.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Design épuré et responsive avec animations
st.markdown("""
<meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=5.0, user-scalable=yes">
<style>
    /* Variables de couleurs */
    :root {
        --primary-color: #307E84;
        --secondary-color: #823B8A;
        --accent-color: #FFB500;
        --dark-color: #075289;
        --light-gray: #F5F5F5;
        --border-color: #E0E0E0;
    }

    /* Animations globales */
    @keyframes fadeInUp {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }

    @keyframes slideInRight {
        from {
            opacity: 0;
            transform: translateX(-30px);
        }
        to {
            opacity: 1;
            transform: translateX(0);
        }
    }

    @keyframes shimmer {
        0% {
            background-position: -1000px 0;
        }
        100% {
            background-position: 1000px 0;
        }
    }

    @keyframes pulse {
        0%, 100% {
            opacity: 1;
        }
        50% {
            opacity: 0.8;
        }
    }

    /* Réduire les marges globales */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
        animation: fadeInUp 0.6s ease-out;
    }

    /* Header personnalisé avec animation */
    .custom-header {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--accent-color);
        animation: slideInRight 0.8s ease-out;
        transition: all 0.3s ease;
        box-shadow: 0 2px 8px rgba(0,0,0,0.04);
    }

    .custom-header:hover {
        box-shadow: 0 4px 12px rgba(0,0,0,0.08);
        transform: translateY(-2px);
    }

    .custom-header h1 {
        color: var(--primary-color);
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
        background: linear-gradient(135deg, var(--primary-color), var(--secondary-color));
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
    }

    .custom-header p {
        color: #666;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }

    /* Cards KPI avec animations */
    [data-testid="stMetric"] {
        background: linear-gradient(135deg, #FFFFFF 0%, #FAFBFC 100%);
        border-radius: 12px;
        padding: 1rem;
        border: 1px solid var(--border-color);
        transition: all 0.3s ease;
        animation: fadeInUp 0.8s ease-out;
    }

    [data-testid="stMetric"]:hover {
        transform: translateY(-4px) scale(1.02);
        box-shadow: 0 8px 16px rgba(0,0,0,0.1);
        border-color: var(--accent-color);
    }

    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-color);
        transition: color 0.3s ease;
    }

    [data-testid="stMetric"]:hover [data-testid="stMetricValue"] {
        color: var(--accent-color);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }

    /* Tabs styling avec animations */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
        background-color: transparent;
        border-bottom: 2px solid var(--border-color);
    }

    .stTabs [data-baseweb="tab"] {
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: #666;
        border: none;
        background-color: transparent;
        transition: all 0.3s ease;
        position: relative;
    }

    .stTabs [data-baseweb="tab"]:hover {
        color: var(--accent-color);
        transform: translateY(-2px);
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-color);
        border-bottom: 3px solid var(--accent-color);
        background-color: transparent;
        animation: slideInRight 0.4s ease-out;
    }

    .stTabs [aria-selected="true"]::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 100%;
        height: 3px;
        background: linear-gradient(90deg, var(--accent-color), var(--tertiary-color));
        animation: shimmer 2s infinite;
    }

    /* Sidebar styling avec animation */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E1E1E 0%, #252525 100%);
        animation: slideInRight 0.5s ease-out;
        box-shadow: 2px 0 12px rgba(0,0,0,0.3);
    }

    [data-testid="stSidebar"] > div {
        background: transparent;
    }

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #E0E0E0;
    }

    [data-testid="stSidebar"] h3 {
        color: #FFB500 !important;
        font-weight: 600;
    }

    [data-testid="stSidebar"] label {
        color: #E0E0E0 !important;
        font-weight: 500;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div {
        background-color: #2A2A2A;
        color: #E0E0E0;
        border: 1px solid #444;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .stSelectbox > div > div:hover {
        border-color: var(--accent-color);
        box-shadow: 0 0 8px rgba(255, 181, 0, 0.2);
    }

    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: #2A2A2A;
        border: 1px solid #444;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .stMultiSelect > div > div:hover {
        border-color: var(--accent-color);
        box-shadow: 0 0 8px rgba(255, 181, 0, 0.2);
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #2A2A2A;
        color: #E0E0E0;
        border: 1px solid #444;
        transition: all 0.3s ease;
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input:focus {
        border-color: var(--accent-color);
        box-shadow: 0 0 12px rgba(255, 181, 0, 0.3);
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input::placeholder {
        color: #888;
    }

    /* Info box dans sidebar */
    [data-testid="stSidebar"] .element-container .stAlert {
        background-color: #2A2A2A;
        color: #E0E0E0;
        border: 1px solid #444;
    }

    /* Boutons avec animations */
    .stButton > button {
        width: 100%;
        border-radius: 8px;
        border: 1px solid var(--border-color);
        font-weight: 500;
        transition: all 0.3s ease;
        background-color: transparent;
        position: relative;
        overflow: hidden;
    }

    .stButton > button::before {
        content: '';
        position: absolute;
        top: 50%;
        left: 50%;
        width: 0;
        height: 0;
        border-radius: 50%;
        background: rgba(255, 181, 0, 0.2);
        transform: translate(-50%, -50%);
        transition: width 0.6s, height 0.6s;
    }

    .stButton > button:hover::before {
        width: 300px;
        height: 300px;
    }

    .stButton > button:hover {
        border-color: var(--accent-color);
        color: var(--accent-color);
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(255, 181, 0, 0.3);
    }

    /* Bouton dans sidebar */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #2A2A2A;
        color: #E0E0E0;
        border: 1px solid #444;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #FFB500;
        color: #1E1E1E;
        border-color: #FFB500;
    }

    /* Tags multiselect (années) */
    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] {
        background-color: #FFB500 !important;
        color: #1E1E1E !important;
    }

    [data-testid="stSidebar"] .stMultiSelect span[data-baseweb="tag"] svg {
        fill: #1E1E1E !important;
    }

    /* Sections avec animations */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--primary-color);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
        position: relative;
        animation: slideInRight 0.6s ease-out;
    }

    .section-title::after {
        content: '';
        position: absolute;
        bottom: -2px;
        left: 0;
        width: 80px;
        height: 2px;
        background: linear-gradient(90deg, var(--accent-color), transparent);
        animation: shimmer 3s infinite;
    }

    /* Graphiques avec animations */
    .plotly-graph-div {
        border-radius: 12px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.4s ease;
        animation: fadeInUp 1s ease-out;
        background: white;
    }

    .plotly-graph-div:hover {
        box-shadow: 0 8px 20px rgba(0,0,0,0.12);
        transform: translateY(-4px);
    }

    /* Colonnes avec stagger animation */
    .element-container {
        animation: fadeInUp 0.8s ease-out;
    }

    .element-container:nth-child(1) { animation-delay: 0.1s; }
    .element-container:nth-child(2) { animation-delay: 0.2s; }
    .element-container:nth-child(3) { animation-delay: 0.3s; }
    .element-container:nth-child(4) { animation-delay: 0.4s; }
    .element-container:nth-child(5) { animation-delay: 0.5s; }

    /* Dataframes avec animations */
    [data-testid="stDataFrame"] {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: 0 2px 8px rgba(0,0,0,0.06);
        transition: all 0.3s ease;
        animation: fadeInUp 1s ease-out;
    }

    [data-testid="stDataFrame"]:hover {
        box-shadow: 0 6px 16px rgba(0,0,0,0.1);
    }

    /* Loading spinner personnalisé */
    .stSpinner > div {
        border-color: var(--accent-color) !important;
        border-right-color: transparent !important;
    }

    /* Smooth scroll */
    html {
        scroll-behavior: smooth;
    }

    /* Logo animations */
    [data-testid="stSidebar"] [data-testid="stImage"] {
        transition: all 0.3s ease;
        filter: brightness(0.95);
    }

    [data-testid="stSidebar"] [data-testid="stImage"]:hover {
        filter: brightness(1.1);
        transform: scale(1.05);
    }

    /* Progress bar si présent */
    .stProgress > div > div {
        background: linear-gradient(90deg, var(--primary-color), var(--accent-color));
        animation: pulse 2s infinite;
    }

    /* Responsive - Mobile First */
    @media (max-width: 1200px) {
        /* Écrans moyens et tablettes */
        .block-container {
            padding: 1.5rem 1rem;
            max-width: 100%;
        }

        .custom-header {
            padding: 1rem;
        }

        .custom-header h1 {
            font-size: 1.5rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.6rem;
        }

        /* Graphiques plus compacts */
        .plotly-graph-div {
            margin-bottom: 1rem;
        }

        /* Réduire les gaps entre colonnes */
        [data-testid="column"] {
            padding: 0 0.5rem;
        }
    }

    @media (max-width: 768px) {
        /* Tablettes et grands mobiles */
        .block-container {
            padding: 0.75rem 0.5rem;
        }

        .custom-header {
            padding: 0.75rem;
            margin-bottom: 1rem;
        }

        .custom-header h1 {
            font-size: 1.2rem;
            line-height: 1.3;
        }

        .custom-header p {
            font-size: 0.75rem;
        }

        /* Réduire la taille de l'icône sur tablette */
        .hospital-icon {
            width: 40px !important;
            height: 40px !important;
        }

        /* KPIs en 2 colonnes sur tablette pour meilleure lisibilité */
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
            display: grid !important;
            grid-template-columns: repeat(2, 1fr) !important;
            gap: 0.5rem !important;
        }

        [data-testid="stMetric"] {
            padding: 0.75rem;
            margin-bottom: 0.5rem;
            min-height: 80px;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.5rem;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.8rem;
            font-weight: 600;
        }

        /* Tabs plus compacts avec indicateur de scroll */
        .stTabs [data-baseweb="tab-list"] {
            gap: 0.5rem;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            padding-bottom: 0.5rem;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 6px;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 3px;
        }

        .stTabs [data-baseweb="tab"] {
            padding: 0.6rem 1rem;
            font-size: 0.9rem;
            flex-shrink: 0;
            white-space: nowrap;
        }

        /* Titres de section plus petits */
        .section-title {
            font-size: 1.1rem;
            margin: 1.5rem 0 1rem 0;
        }

        /* Sidebar responsive */
        [data-testid="stSidebar"] {
            min-width: 250px !important;
        }

        /* Selectbox et filtres plus grands pour mobile */
        .stSelectbox label, .stMultiSelect label {
            font-size: 0.9rem;
            font-weight: 600;
        }

        .stSelectbox > div > div, .stMultiSelect > div > div {
            font-size: 0.95rem;
            min-height: 44px;
        }

        /* Graphiques responsive avec hauteur adaptée */
        .plotly-graph-div {
            margin: 1rem 0;
            min-height: 350px !important;
            border-radius: 8px;
        }

        /* Tableaux scrollables avec indicateur visible */
        [data-testid="stDataFrame"] {
            font-size: 0.85rem;
            max-width: 100%;
            overflow-x: auto;
            -webkit-overflow-scrolling: touch;
            border-radius: 8px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        }

        [data-testid="stDataFrame"]::-webkit-scrollbar {
            height: 8px;
        }

        [data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 4px;
        }

        /* Colonnes empilées sur tablette */
        [data-testid="column"] {
            min-width: 100% !important;
            padding: 0.5rem 0;
        }

        /* Réduire animations sur mobile pour performance */
        * {
            animation-duration: 0.3s !important;
        }

        /* Boutons pleine largeur plus grands */
        .stButton > button {
            font-size: 1rem;
            padding: 0.75rem;
            width: 100%;
            min-height: 44px;
        }

        /* Améliorer les zones de clic */
        .stSelectbox, .stMultiSelect, .stButton {
            margin-bottom: 1rem;
        }

        /* Filtres de la carte en colonne */
        [data-testid="stHorizontalBlock"] > div {
            width: 100% !important;
            margin-bottom: 0.75rem;
        }

        /* Info boxes plus lisibles */
        .stAlert {
            font-size: 0.9rem;
            padding: 1rem;
            line-height: 1.5;
        }
    }

    @media (max-width: 480px) {
        /* Mobiles compacts */
        .block-container {
            padding: 0.75rem 0.5rem;
        }

        .custom-header {
            padding: 0.75rem;
        }

        .custom-header h1 {
            font-size: 1.1rem;
        }

        .custom-header p {
            font-size: 0.75rem;
            line-height: 1.5;
        }

        /* Cacher l'icône sur très petit écran */
        .header-icon {
            display: none !important;
        }

        /* KPIs en 1 colonne sur mobile pour meilleure lisibilité */
        [data-testid="stHorizontalBlock"]:has([data-testid="stMetric"]) {
            display: flex !important;
            flex-direction: column !important;
            gap: 0.75rem !important;
        }

        [data-testid="stMetric"] {
            padding: 1rem;
            min-height: 70px;
            border-radius: 8px;
            background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
            box-shadow: 0 2px 8px rgba(0,0,0,0.08);
        }

        [data-testid="stMetricValue"] {
            font-size: 1.6rem;
            font-weight: 700;
        }

        [data-testid="stMetricLabel"] {
            font-size: 0.85rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.5px;
        }

        .section-title {
            font-size: 1.1rem;
            margin: 1.25rem 0 0.75rem 0;
        }

        /* Tabs en scroll horizontal avec indicateur visible */
        .stTabs [data-baseweb="tab-list"] {
            overflow-x: auto;
            flex-wrap: nowrap;
            gap: 0.5rem;
            -webkit-overflow-scrolling: touch;
            scrollbar-width: thin;
            padding-bottom: 0.75rem;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar {
            height: 6px;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 3px;
        }

        .stTabs [data-baseweb="tab-list"]::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 3px;
        }

        .stTabs [data-baseweb="tab"] {
            font-size: 0.85rem;
            padding: 0.6rem 1rem;
            white-space: nowrap;
        }

        /* Graphiques optimisés pour mobile */
        .plotly-graph-div {
            min-height: 300px !important;
            margin: 1rem 0;
            border-radius: 8px;
        }

        /* Sidebar pleine largeur quand ouverte */
        [data-testid="stSidebar"] {
            width: 100% !important;
            max-width: 100% !important;
        }

        /* Tableaux avec scroll visible et lisible */
        [data-testid="stDataFrame"] {
            font-size: 0.8rem;
            border-radius: 8px;
        }

        [data-testid="stDataFrame"]::-webkit-scrollbar {
            height: 10px;
        }

        [data-testid="stDataFrame"]::-webkit-scrollbar-track {
            background: #f1f1f1;
            border-radius: 5px;
        }

        [data-testid="stDataFrame"]::-webkit-scrollbar-thumb {
            background: var(--accent-color);
            border-radius: 5px;
        }

        /* Info boxes lisibles */
        .stAlert {
            font-size: 0.85rem;
            padding: 0.85rem;
            line-height: 1.6;
        }

        /* Filtres et selectbox avec zones de clic optimales */
        .stSelectbox, .stMultiSelect {
            margin-bottom: 0.75rem;
        }

        .stSelectbox > div > div, .stMultiSelect > div > div {
            min-height: 48px;
            font-size: 1rem;
        }

        /* Boutons optimisés pour tactile */
        .stButton > button {
            min-height: 48px;
            font-size: 1rem;
        }

        /* Tout en pleine largeur */
        [data-testid="column"] {
            width: 100% !important;
            min-width: 100% !important;
            padding: 0.5rem 0;
        }

        /* Espacement entre les éléments */
        .element-container {
            margin-bottom: 0.75rem;
        }
    }

    @media (max-width: 360px) {
        /* Très petits mobiles */
        .custom-header h1 {
            font-size: 0.9rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1rem;
        }

        .section-title {
            font-size: 0.9rem;
        }

        .plotly-graph-div {
            min-height: 200px;
        }
    }

    /* Disable animations for reduced motion preference */
    @media (prefers-reduced-motion: reduce) {
        * {
            animation: none !important;
            transition: none !important;
        }
    }
</style>
""", unsafe_allow_html=True)

# Palette de couleurs Stryker - Charte officielle
COLORS = {
    'primary': '#823B8A',      # Violet
    'secondary': '#307E84',    # Bleu-vert
    'tertiary': '#BB7702',     # Orange
    'quaternary': '#075289',   # Bleu foncé
    'palette': ['#823B8A', '#307E84', '#BB7702', '#075289']  # Palette principale
}

# ========================================
# CHARGEMENT DES DONNÉES
# ========================================

@st.cache_data(ttl=3600, show_spinner="Chargement initial des donnees...")
def load_data():
    """Charge les donnees depuis le fichier Parquet optimise (7x plus rapide!)"""
    data_file = Path("data_casemix_2022_2024.parquet")

    if not data_file.exists():
        st.error("Fichier data_casemix_2022_2024.parquet introuvable")
        st.info("Verifiez que Git LFS est correctement configure")
        st.stop()

    # Verifier si c'est un pointer Git LFS
    file_size = data_file.stat().st_size
    if file_size < 1000:
        st.error(f"Le fichier Parquet semble etre un pointer Git LFS ({file_size} bytes)")
        st.info("Git LFS n'a pas telecharge le fichier. Verifiez packages.txt et la configuration LFS.")
        st.stop()

    # Lecture du fichier Parquet (beaucoup plus rapide que CSV!)
    try:
        df = pd.read_parquet(data_file)
        # Pas d'index - le filtrage direct est plus rapide pour des MultiIndex non-unique
    except Exception as e:
        st.error(f"Erreur lors de la lecture du Parquet : {str(e)}")
        st.stop()

    # Les donnees sont deja nettoyees et typees dans le Parquet
    return df

@st.cache_data
def load_finess_mapping():
    """Charge le mapping FINESS"""
    try:
        df_mapping = pd.read_csv('etablissements_finess.csv', sep=',', encoding='utf-8-sig', dtype=str)
        return dict(zip(df_mapping['Finess'], df_mapping['Raison sociale']))
    except Exception as e:
        st.warning(f"Impossible de charger le mapping FINESS: {str(e)}")
        return {}

# Chargement des données
with st.spinner('Chargement des données...'):
    df = load_data()
    finess_mapping = load_finess_mapping()

# ========================================
# SIDEBAR - FILTRES (AVEC CACHE POUR LES LISTES)
# ========================================

# OPTIMISATION CRITIQUE: Calculer les listes de filtres UNE SEULE FOIS
@st.cache_data
def get_filter_options():
    """Calcule les options de filtres une seule fois au lieu de à chaque rerun"""
    try:
        return {
            'annees': sorted(df['Annee'].unique()),
            'finess': sorted(df['Finess'].unique()),
            'da': ['Tous'] + sorted([x for x in df['DA'].unique() if x != 'Non renseigné']) if 'DA' in df.columns else ['Tous'],
            'classif': ['Tous'] + sorted([x for x in df['Classif PKCS'].unique() if x != 'Non renseigné']) if 'Classif PKCS' in df.columns else ['Tous']
        }
    except Exception as e:
        st.error(f"Erreur lors du calcul des options de filtres: {str(e)}")
        st.stop()

filter_opts = get_filter_options()

with st.sidebar:
    # Logo
    logo_path = Path("assets/logostrykerscansante.png")
    if logo_path.exists():
        st.image(str(logo_path), width="stretch")

    st.markdown("---")
    st.markdown("### Filtres")

    # Filtre années
    annees_selectionnees = st.multiselect(
        "Années",
        options=filter_opts['annees'],
        default=filter_opts['annees'],
        help="Sélectionnez les années à analyser"
    )

    # Filtre établissement avec option "Tous les établissements"
    def format_etablissement(finess):
        if finess == "Tous les établissements":
            return finess
        nom = finess_mapping.get(finess, 'Inconnu')  # FIX CRITIQUE: Ne JAMAIS filtrer df ici!
        return f"{finess} - {nom}"

    etablissement_options = ['Tous les établissements'] + filter_opts['finess']

    # Définir l'index par défaut : CLINIQUE AMBULATOIRE CENDANEG (010007300)
    default_finess = '010007300'
    default_index = etablissement_options.index(default_finess) if default_finess in etablissement_options else 1

    etablissement_selectionne = st.selectbox(
        "Établissement",
        options=etablissement_options,
        format_func=format_etablissement,
        index=default_index,
        help="Choisissez un établissement ou 'Tous' pour voir l'ensemble"
    )

    st.markdown("---")

    # Statistiques
    st.info(f"**Données chargées**\n\n{len(df):,} lignes\n\n{df['Finess'].nunique()} établissements")

    # Bouton reset
    if st.button("Réinitialiser", width="stretch"):
        st.cache_data.clear()
        st.rerun()

# ========================================
# FILTRAGE ULTRA-OPTIMISE AVEC SESSION STATE
# ========================================

def filter_data_ultra_fast(finess, annees):
    """Filtrage ultra-rapide avec masque booleen"""
    # Si "Tous les établissements" est sélectionné, ne pas filtrer par Finess
    if finess == "Tous les établissements":
        if annees:
            mask = df['Annee'].isin(annees)
            return df[mask].copy()
        else:
            return df.copy()

    # Filtrage direct par Finess avec masque booleen
    mask = (df['Finess'] == finess)

    # Filtrer par années
    if annees:
        mask &= df['Annee'].isin(annees)

    # Un seul filtrage à la fin - beaucoup plus rapide
    return df[mask].copy()

# Utilisation de session_state pour garder le dernier filtrage en memoire
# Sécurité: s'assurer que les variables sont bien définies
if not annees_selectionnees:
    annees_selectionnees = []

cache_key = f"{etablissement_selectionne}_{tuple(annees_selectionnees)}"

if 'last_cache_key' not in st.session_state or st.session_state.last_cache_key != cache_key:
    try:
        st.session_state.df_filtered = filter_data_ultra_fast(
            etablissement_selectionne,
            tuple(annees_selectionnees)
        )
        st.session_state.last_cache_key = cache_key
    except Exception as e:
        st.error(f"Erreur lors du filtrage des données: {str(e)}")
        st.exception(e)
        st.stop()

df_filtered = st.session_state.df_filtered

# ========================================
# VÉRIFICATION DE LA TAILLE DES DONNÉES
# ========================================

# Avertissement si trop de données (risque de dépassement mémoire sur Streamlit Cloud)
if etablissement_selectionne == "Tous les établissements":
    nb_lignes = len(df_filtered)
    if nb_lignes > 500000:  # Plus de 500k lignes
        st.warning(f"""
        ⚠️ **Volume de données important** : {nb_lignes:,} lignes à traiter

        L'affichage de tous les établissements peut être lent et consommer beaucoup de mémoire.

        **Recommandations :**
        - Utilisez les filtres par année pour réduire le volume
        - Privilégiez la vue "Carte de France" pour l'analyse multi-établissements
        - Sélectionnez un établissement spécifique pour des analyses détaillées
        """)

# ========================================
# EN-TÊTE
# ========================================

# Déterminer le nom de l'établissement pour l'en-tête
if etablissement_selectionne == "Tous les établissements":
    nom_etab = "Tous les établissements"
    # Sécurité: vérifier que df_filtered n'est pas vide avant de compter
    nb_etab = df_filtered['Finess'].nunique() if not df_filtered.empty else 0
    finess_display = f"{nb_etab} établissements"
else:
    nom_etab = finess_mapping.get(etablissement_selectionne, 'Inconnu')
    finess_display = f"FINESS: {etablissement_selectionne}"

# Lire et encoder le SVG de l'hôpital
hospital_svg_path = Path("assets/hospital.svg")
if hospital_svg_path.exists():
    with open(hospital_svg_path, 'r', encoding='utf-8') as f:
        svg_content = f.read()
        # Encoder en base64 pour éviter les problèmes d'échappement
        svg_b64 = base64.b64encode(svg_content.encode('utf-8')).decode('utf-8')
        hospital_svg = f'<img src="data:image/svg+xml;base64,{svg_b64}" class="hospital-icon" style="width: 48px; height: 48px; display: block;" />'
else:
    hospital_svg = ""

# En-tête avec informations de l'établissement
st.markdown(f"""
<div class="custom-header">
    <div style="display: flex; align-items: center; gap: 1rem; flex-wrap: wrap;">
        <div class="header-icon" style="flex-shrink: 0;">
            {hospital_svg}
        </div>
        <div class="header-content" style="flex: 1; min-width: 250px;">
            <h1>{nom_etab}</h1>
            <p>{finess_display} • Période: {', '.join(map(str, annees_selectionnees)) if annees_selectionnees else 'Toutes années'}</p>
        </div>
    </div>
</div>
""", unsafe_allow_html=True)

# Vérifier si données disponibles
if df_filtered.empty:
    st.warning("Aucune donnée disponible pour cette sélection")
    st.stop()

# ========================================
# KPIS PRINCIPAUX OPTIMISES
# ========================================

# Calcul direct des KPIs sur les donnees filtrees (deja en session_state)
total_effectif = df_filtered['Effectif'].sum()
dms_moyenne = (df_filtered['DMS'] * df_filtered['Effectif']).sum() / total_effectif if total_effectif > 0 else 0
age_moyen = (df_filtered['Age_Moyen'] * df_filtered['Effectif']).sum() / total_effectif if total_effectif > 0 else 0
taux_deces = (df_filtered['Taux_Deces'] * df_filtered['Effectif']).sum() / total_effectif if total_effectif > 0 else 0
nb_ghm = df_filtered['Code_GHM'].nunique()

st.markdown('<div class="section-title">Indicateurs Clés</div>', unsafe_allow_html=True)

col1, col2, col3, col4, col5 = st.columns(5)

with col1:
    st.metric("Effectif Total", f"{int(total_effectif):,}")

with col2:
    st.metric("GHM Distincts", f"{nb_ghm}")

with col3:
    st.metric("DMS Moyenne", f"{dms_moyenne:.1f} j")

with col4:
    st.metric("Âge Moyen", f"{age_moyen:.0f} ans")

with col5:
    st.metric("Taux Décès", f"{taux_deces:.2f}%")

st.markdown("---")

# ========================================
# FONCTIONS DE CALCUL CACHEES AVEC SESSION STATE (CRUCIAL!)
# ========================================
# PROBLEME: @st.cache_data hash le DataFrame (lent sur 2.2M lignes)
# SOLUTION: Utiliser session_state avec une clé légère

def compute_cached(cache_key_suffix, compute_func):
    """Wrapper générique pour cache en session_state"""
    full_key = f"computed_{cache_key}_{cache_key_suffix}"

    if full_key not in st.session_state:
        st.session_state[full_key] = compute_func()

    return st.session_state[full_key]

def compute_top_libelles(df_filtered, top_n=10):
    """Cache le top N des libellés"""
    def calc():
        # Optimisation : si trop de lignes, échantillonner d'abord
        df_work = df_filtered
        if len(df_filtered) > 1000000:
            # Garder seulement les lignes avec les effectifs les plus élevés
            df_work = df_filtered.nlargest(500000, 'Effectif')
        return df_work.groupby('Libelle', as_index=False, sort=False).agg({
            'Effectif': 'sum'
        }).nlargest(top_n, 'Effectif')
    return compute_cached(f"top{top_n}", calc)

def compute_detailed_table(df_filtered):
    """Cache le tableau détaillé avec weighted averages"""
    def calc():
        df_temp = df_filtered.reset_index(drop=True)
        return df_temp.groupby('Libelle', as_index=False).agg({
            'Effectif': 'sum',
            'DMS': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Age_Moyen': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Taux_Deces': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0
        }).sort_values('Effectif', ascending=False).head(20)
    return compute_cached("detailed", calc)

def compute_evolution_data(df_filtered):
    """Cache les données d'évolution temporelle"""
    def calc():
        df_temp = df_filtered.reset_index(drop=True)
        return df_temp.groupby('Annee', as_index=False).agg({
            'Effectif': 'sum',
            'DMS': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Age_Moyen': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Taux_Deces': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0
        })
    return compute_cached("evol", calc)

def compute_classification_data(df_filtered, column_name):
    """Cache les données de classification (DA ou PKCS)"""
    def calc():
        if column_name not in df_filtered.columns:
            return pd.DataFrame()
        return df_filtered[df_filtered[column_name] != 'Non renseigné'].groupby(column_name)['Effectif'].sum().reset_index().sort_values('Effectif', ascending=False).head(10)
    return compute_cached(f"class_{column_name}", calc)

# ========================================
# ONGLETS
# ========================================

tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "Vue d'ensemble",
    "Sélection Filtrée",
    "Analyse Financière",
    "Carte de France",
    "Classifications",
    "Évolution temporelle",
    "Export données"
])

# TAB 1: VUE D'ENSEMBLE (FUSION DES 2 ANCIENS ONGLETS)
with tab1:
    st.markdown('<div class="section-title">Vue d\'ensemble de l\'activité</div>', unsafe_allow_html=True)

    # Première ligne: Top 10 + Distributions
    col1, col2 = st.columns(2)

    with col1:
        # Top 10 Libellés
        df_top = compute_top_libelles(df_filtered, 10)

        fig = px.bar(
            df_top,
            y='Libelle',
            x='Effectif',
            orientation='h',
            title="Top 10 Libellés par Effectif",
            color='Effectif',
            color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['tertiary']]],
            text='Effectif'
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(
            height=450,
            showlegend=False,
            font=dict(size=11),
            yaxis=dict(title=''),
            xaxis=dict(title='Effectif'),
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        # Distribution de l'âge
        fig = go.Figure()
        fig.add_trace(go.Histogram(
            x=df_filtered['Age_Moyen'],
            nbinsx=30,
            marker_color=COLORS['primary'],
            opacity=0.7,
            name='Distribution'
        ))
        mediane_age = df_filtered['Age_Moyen'].median()
        fig.add_vline(
            x=mediane_age,
            line_dash="dash",
            line_color=COLORS['tertiary'],
            annotation_text=f"Médiane: {mediane_age:.0f} ans",
            annotation_position="top"
        )
        fig.update_layout(
            title="Distribution de l'Âge Moyen",
            xaxis_title="Âge (années)",
            yaxis_title="Fréquence",
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

        # Répartition DMS
        fig = go.Figure()
        df_filtered_copy = df_filtered[df_filtered['DMS'].notna()].copy()
        fig.add_trace(go.Histogram(
            x=df_filtered_copy['DMS'],
            nbinsx=30,
            marker_color=COLORS['quaternary'],
            opacity=0.7,
            name='Distribution'
        ))
        mediane_dms = df_filtered_copy['DMS'].median()
        fig.add_vline(
            x=mediane_dms,
            line_dash="dash",
            line_color=COLORS['tertiary'],
            annotation_text=f"Médiane: {mediane_dms:.1f} j",
            annotation_position="top"
        )
        fig.update_layout(
            title="Distribution de la Durée Moyenne de Séjour",
            xaxis_title="DMS (jours)",
            yaxis_title="Fréquence",
            height=300,
            showlegend=False,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

    # Analyses détaillées
    st.markdown('<div class="section-title">Analyses Détaillées</div>', unsafe_allow_html=True)

    df_detail = compute_detailed_table(df_filtered)
    col1, col2 = st.columns(2)

    with col1:
        # Info discrète pour guider l'utilisateur
        st.markdown("""
        <div style="background: linear-gradient(135deg, #F0F8FF, #FFF9E6); padding: 8px 12px; border-radius: 6px; margin-bottom: 10px; border-left: 3px solid #FFB500; font-size: 0.8rem;">
            💡 <strong>Comment lire ce graphique :</strong> Taille du cercle = volume d'activité • Position = DMS vs âge moyen
        </div>
        """, unsafe_allow_html=True)

        # Scatter: DMS vs Age
        fig = px.scatter(
            df_detail,
            x='DMS',
            y='Age_Moyen',
            size='Effectif',
            hover_name='Libelle',
            title="Relation DMS × Âge × Effectif (Top 20)",
            color='Effectif',
            color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['tertiary']]],
            labels={'DMS': 'DMS (jours)', 'Age_Moyen': 'Âge moyen (années)'}
        )
        fig.update_layout(
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

    with col2:
        # Taux de décès
        df_deces = df_detail[df_detail['Taux_Deces'] > 0].sort_values('Taux_Deces', ascending=False).head(10)

        if len(df_deces) > 0:
            fig = px.bar(
                df_deces,
                x='Taux_Deces',
                y='Libelle',
                orientation='h',
                title="Top 10 Taux de Décès",
                color='Taux_Deces',
                color_continuous_scale=[[0, COLORS['tertiary']], [0.5, COLORS['secondary']], [1, COLORS['primary']]],
                text='Taux_Deces'
            )
            fig.update_traces(texttemplate='%{text:.2f}%', textposition='outside')
            fig.update_layout(
                height=400,
                showlegend=False,
                yaxis=dict(title=''),
                xaxis=dict(title='Taux de décès (%)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")
        else:
            st.info("Pas de données de mortalité disponibles")

    # Heatmap de corrélation
    st.markdown('<div class="section-title">Matrice de Corrélation</div>', unsafe_allow_html=True)
    df_corr = df_filtered[['Effectif', 'DMS', 'Age_Moyen', 'Sexe_Ratio', 'Taux_Deces']].dropna()

    if len(df_corr) > 10:
        correlation = df_corr.corr()
        fig = go.Figure(data=go.Heatmap(
            z=correlation.values,
            x=['Effectif', 'DMS', 'Âge', 'Sexe Ratio', 'Taux Décès'],
            y=['Effectif', 'DMS', 'Âge', 'Sexe Ratio', 'Taux Décès'],
            colorscale=[[0, '#307E84'], [0.5, 'white'], [1, '#BB7702']],
            zmid=0,
            text=np.round(correlation.values, 2),
            texttemplate='%{text}',
            textfont={"size": 12},
            colorbar=dict(title="Corrélation")
        ))
        fig.update_layout(
            title="Corrélation entre les Indicateurs",
            height=400,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

    # Tableau détaillé
    st.markdown('<div class="section-title">Tableau Détaillé (Top 20)</div>', unsafe_allow_html=True)
    df_display = df_detail.copy()
    df_display['% du Total'] = (df_display['Effectif'] / total_effectif * 100).round(1)
    df_display = df_display[['Libelle', 'Effectif', '% du Total', 'DMS', 'Age_Moyen', 'Taux_Deces']]
    df_display.columns = ['Libellé GHM', 'Effectif', '% Total', 'DMS (j)', 'Âge', 'Décès (%)']
    df_display['DMS (j)'] = df_display['DMS (j)'].round(1)
    df_display['Âge'] = df_display['Âge'].round(0)
    df_display['Décès (%)'] = df_display['Décès (%)'].round(2)
    st.dataframe(
        df_display,
        width="stretch",
        hide_index=True,
        height=400
    )

# TAB 2: SÉLECTION FILTRÉE (NOUVEAU!)
with tab2:
    st.markdown('<div class="section-title">Sélection Filtrée - Analyse Approfondie</div>', unsafe_allow_html=True)

    # Message différent selon si "Tous les établissements" est sélectionné
    if etablissement_selectionne == "Tous les établissements":
        st.info("🌍 **Vue d'ensemble multi-établissements** : Vous visualisez actuellement les données de tous les établissements. Utilisez les filtres de la barre latérale pour sélectionner un établissement spécifique, ou affinez votre analyse avec les filtres ci-dessous.")
    else:
        st.info("🎯 **Filtrez vos données** : Sélectionnez les critères ci-dessous pour affiner votre analyse. Le graphique se mettra à jour automatiquement.")

    # Créer les filtres dynamiques sur 3 colonnes
    col1, col2, col3 = st.columns(3)

    with col1:
        # Récupérer les valeurs uniques présentes dans df_filtered
        ghm_options = ['Tous'] + sorted([x for x in df_filtered['Code_GHM'].unique() if pd.notna(x)])
        ghm_filter = st.selectbox("GHM", options=ghm_options)

        mco_options = ['Tous'] + sorted([x for x in df_filtered['MCO'].unique() if pd.notna(x) and x != 'Non renseigné'])
        mco_filter = st.selectbox("MCO", options=mco_options)

        cas_options = ['Tous'] + sorted([x for x in df_filtered['CAS'].unique() if pd.notna(x) and x != 'Non renseigné'])
        cas_filter = st.selectbox("CAS", options=cas_options)

    with col2:
        da_options = ['Tous'] + sorted([x for x in df_filtered['DA'].unique() if pd.notna(x) and x != 'Non renseigné'])
        da_filter = st.selectbox("Domaine d'Activité (DA)", options=da_options)

        gp_options = ['Tous'] + sorted([x for x in df_filtered['GP'].unique() if pd.notna(x) and x != 'Non renseigné'])
        gp_filter = st.selectbox("GP", options=gp_options)

        ga_options = ['Tous'] + sorted([x for x in df_filtered['GA'].unique() if pd.notna(x) and x != 'Non renseigné'])
        ga_filter = st.selectbox("GA", options=ga_options)

    with col3:
        classif_options = ['Tous'] + sorted([x for x in df_filtered['Classif PKCS'].unique() if pd.notna(x) and x != 'Non renseigné'])
        classif_filter = st.selectbox("Classification PKCS", options=classif_options)

        libracine_options = ['Tous'] + sorted([x for x in df_filtered['Libracine'].unique() if pd.notna(x) and x != 'Non renseigné'])
        libracine_filter = st.selectbox("Libracine", options=libracine_options)

        regroup_options = ['Tous'] + sorted([x for x in df_filtered['Regroupement GHM PH'].unique() if pd.notna(x) and x != 'Non renseigné'])
        regroup_filter = st.selectbox("Regroupement GHM PH", options=regroup_options)

    # Appliquer les filtres
    df_selection_filtree = df_filtered.copy()

    if ghm_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['Code_GHM'] == ghm_filter]
    if mco_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['MCO'] == mco_filter]
    if cas_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['CAS'] == cas_filter]
    if da_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['DA'] == da_filter]
    if gp_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['GP'] == gp_filter]
    if ga_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['GA'] == ga_filter]
    if classif_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['Classif PKCS'] == classif_filter]
    if libracine_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['Libracine'] == libracine_filter]
    if regroup_filter != 'Tous':
        df_selection_filtree = df_selection_filtree[df_selection_filtree['Regroupement GHM PH'] == regroup_filter]

    # Afficher le graphique "Effectif par Année"
    st.markdown("---")
    st.markdown('<div class="section-title">Effectif par Année (Données Filtrées)</div>', unsafe_allow_html=True)

    if not df_selection_filtree.empty:
        df_annee_filtered = df_selection_filtree.groupby('Annee')['Effectif'].sum().reset_index()

        fig = px.bar(
            df_annee_filtered,
            x='Annee',
            y='Effectif',
            title=f"Effectif par Année ({len(df_selection_filtree):,} lignes sélectionnées)",
            color='Effectif',
            color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['tertiary']]],
            text='Effectif'
        )
        fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
        fig.update_layout(
            height=450,
            showlegend=False,
            xaxis=dict(title='Année'),
            yaxis=dict(title='Effectif'),
            margin=dict(l=20, r=20, t=40, b=40)
        )
        st.plotly_chart(fig, width="stretch")

        # Statistiques de la sélection
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Lignes sélectionnées", f"{len(df_selection_filtree):,}")
        with col2:
            st.metric("Effectif total", f"{df_selection_filtree['Effectif'].sum():,}")
        with col3:
            st.metric("DMS moyenne", f"{(df_selection_filtree['DMS'] * df_selection_filtree['Effectif']).sum() / df_selection_filtree['Effectif'].sum():.1f} j" if df_selection_filtree['Effectif'].sum() > 0 else "N/A")
        with col4:
            st.metric("Âge moyen", f"{(df_selection_filtree['Age_Moyen'] * df_selection_filtree['Effectif']).sum() / df_selection_filtree['Effectif'].sum():.0f} ans" if df_selection_filtree['Effectif'].sum() > 0 else "N/A")
    else:
        st.warning("⚠️ Aucune donnée ne correspond à cette sélection de filtres.")

# TAB 3: ANALYSE FINANCIÈRE
with tab3:
    st.markdown('<div class="section-title">💰 Analyse Financière et Valorisation</div>', unsafe_allow_html=True)

    # Vérifier si les colonnes de tarifs et statut existent
    if 'Tarif_Public' not in df_filtered.columns or 'CA_Public_Estime' not in df_filtered.columns:
        st.error("⚠️ Les données tarifaires ne sont pas disponibles. Veuillez exécuter le script d'intégration des tarifs.")
        st.info("Exécutez `python integrate_tarifs.py` pour ajouter les tarifs GHS au fichier de données.")
        st.stop()

    if 'Statut_Etablissement' not in df_filtered.columns:
        st.error("⚠️ La colonne Statut_Etablissement n'est pas disponible. Veuillez exécuter le script add_statut_etablissement.py")
        st.info("Exécutez `python add_statut_etablissement.py` pour ajouter le statut Public/Privé aux établissements.")
        st.stop()

    # Déterminer le statut de l'établissement sélectionné
    if etablissement_selectionne == "Tous les établissements":
        statut_etablissement = "Mixte"
        st.info("🌍 **Vue d'ensemble multi-établissements** : Les analyses sont séparées par statut (Public / Privé).")
    else:
        # Récupérer le statut de l'établissement sélectionné
        statut_etablissement = df_filtered['Statut_Etablissement'].iloc[0] if len(df_filtered) > 0 else "Inconnu"

        if statut_etablissement == "Public":
            st.info(f"🏥 **Établissement PUBLIC** : {etablissement_selectionne} - Valorisation basée sur les tarifs GHS Public")
        elif statut_etablissement == "Privé":
            st.info(f"🏥 **Établissement PRIVÉ** : {etablissement_selectionne} - Valorisation basée sur les tarifs GHS Privé")
        else:
            st.warning(f"⚠️ Statut inconnu pour {etablissement_selectionne}")

    # ========== SECTION ÉTABLISSEMENT PUBLIC ==========
    if statut_etablissement in ["Public", "Mixte"]:
        st.markdown('<div class="section-title">🏥 Analyse Établissement Public</div>', unsafe_allow_html=True)

        # Filtrer uniquement les données publiques
        if statut_etablissement == "Mixte":
            df_public = df_filtered[df_filtered['Statut_Etablissement'] == 'Public'].copy()
        else:
            df_public = df_filtered.copy()

        if len(df_public) == 0:
            st.info("Aucune donnée disponible pour les établissements publics.")
        else:
            # KPIs Publics
            ca_public_total = df_public['CA_Public_Estime'].sum()
            tarif_moyen_public = df_public['Tarif_Public'].mean()
            effectif_total_public = df_public['Effectif'].sum()
            nb_ghm_public = df_public['Code_GHM'].nunique()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("CA Public Total", f"{ca_public_total/1e6:.1f} M€")
            with col2:
                st.metric("Tarif Moyen Public", f"{tarif_moyen_public:,.0f} €")
            with col3:
                st.metric("Effectif Total", f"{int(effectif_total_public):,}".replace(',', ' '))
            with col4:
                st.metric("Nombre de GHM", f"{nb_ghm_public}")

            st.markdown("---")

            # Top 15 GHM par CA Public
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💰 Top 15 GHM par CA Public")

                top_ca_public = df_public.groupby(['Code_GHM', 'Libelle']).agg({
                    'CA_Public_Estime': 'sum',
                    'Effectif': 'sum',
                    'Tarif_Public': 'mean'
                }).reset_index().sort_values('CA_Public_Estime', ascending=False).head(15)

                fig = px.bar(
                    top_ca_public,
                    y='Libelle',
                    x='CA_Public_Estime',
                    orientation='h',
                    title="",
                    color='CA_Public_Estime',
                    color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['primary']]],
                    hover_data={'Effectif': ':,', 'Tarif_Public': ':,.0f'},
                    labels={'CA_Public_Estime': 'CA (€)', 'Effectif': 'Effectif', 'Tarif_Public': 'Tarif (€)'}
                )
                fig.update_traces(texttemplate='%{x:,.0f}€', textposition='outside')
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    yaxis=dict(title=''),
                    xaxis=dict(title='Chiffre d\'Affaires (€)'),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 📊 Volume vs Valorisation (Public)")

                # Agréger par GHM
                ghm_public = df_public.groupby(['Code_GHM', 'Libelle']).agg({
                    'Effectif': 'sum',
                    'CA_Public_Estime': 'sum',
                    'Tarif_Public': 'mean',
                    'DMS': 'mean'
                }).reset_index().nlargest(30, 'CA_Public_Estime')

                fig = px.scatter(
                    ghm_public,
                    x='Effectif',
                    y='CA_Public_Estime',
                    size='Tarif_Public',
                    hover_name='Libelle',
                    hover_data={'Effectif': ':,', 'CA_Public_Estime': ':,.0f', 'Tarif_Public': ':,.0f', 'DMS': ':.1f'},
                    title="",
                    color='Tarif_Public',
                    color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['primary']]],
                    labels={
                        'Effectif': 'Volume',
                        'CA_Public_Estime': 'CA Public (€)',
                        'Tarif_Public': 'Tarif (€)',
                        'DMS': 'DMS (j)'
                    }
                )
                fig.update_layout(
                    height=600,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            # Tableau récapitulatif Public
            st.markdown("### 📋 Tableau Récapitulatif GHM Public (Top 20 par CA)")

            recap_public = df_public.groupby(['Code_GHM', 'Libelle']).agg({
                'Effectif': 'sum',
                'CA_Public_Estime': 'sum',
                'Tarif_Public': 'mean',
                'DMS': 'mean'
            }).reset_index().sort_values('CA_Public_Estime', ascending=False).head(20)

            recap_public['% CA'] = (recap_public['CA_Public_Estime'] / ca_public_total * 100).round(1)

            # Formater
            recap_public['Effectif'] = recap_public['Effectif'].apply(lambda x: f"{int(x):,}".replace(',', ' '))
            recap_public['CA Public'] = recap_public['CA_Public_Estime'].apply(lambda x: f"{x:,.0f} €".replace(',', ' '))
            recap_public['Tarif'] = recap_public['Tarif_Public'].apply(lambda x: f"{x:,.0f} €".replace(',', ' '))
            recap_public['DMS'] = recap_public['DMS'].apply(lambda x: f"{x:.1f}j")
            recap_public['% CA'] = recap_public['% CA'].apply(lambda x: f"{x:.1f}%")

            recap_public = recap_public[['Code_GHM', 'Libelle', 'Effectif', 'CA Public', 'Tarif', 'DMS', '% CA']]
            recap_public.columns = ['Code GHM', 'Libellé', 'Effectif', 'CA Public', 'Tarif Public', 'DMS', '% CA']

            st.dataframe(recap_public, use_container_width=True, hide_index=True, height=400)

            st.markdown("---")

    # ========== SECTION ÉTABLISSEMENT PRIVÉ ==========
    if statut_etablissement in ["Privé", "Mixte"]:
        st.markdown('<div class="section-title">🏥 Analyse Établissement Privé</div>', unsafe_allow_html=True)

        # Filtrer uniquement les données privées
        if statut_etablissement == "Mixte":
            df_prive = df_filtered[df_filtered['Statut_Etablissement'] == 'Privé'].copy()
        else:
            df_prive = df_filtered.copy()

        if len(df_prive) == 0:
            st.info("Aucune donnée disponible pour les établissements privés.")
        else:
            # KPIs Privés
            ca_prive_total = df_prive['CA_Prive_Estime'].sum()
            tarif_moyen_prive = df_prive['Tarif_Prive'].mean()
            effectif_total_prive = df_prive['Effectif'].sum()
            nb_ghm_prive = df_prive['Code_GHM'].nunique()

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                st.metric("CA Privé Total", f"{ca_prive_total/1e6:.1f} M€")
            with col2:
                st.metric("Tarif Moyen Privé", f"{tarif_moyen_prive:,.0f} €")
            with col3:
                st.metric("Effectif Total", f"{int(effectif_total_prive):,}".replace(',', ' '))
            with col4:
                st.metric("Nombre de GHM", f"{nb_ghm_prive}")

            st.markdown("---")

            # Top 15 GHM par CA Privé
            col1, col2 = st.columns(2)

            with col1:
                st.markdown("### 💳 Top 15 GHM par CA Privé")

                top_ca_prive = df_prive.groupby(['Code_GHM', 'Libelle']).agg({
                    'CA_Prive_Estime': 'sum',
                    'Effectif': 'sum',
                    'Tarif_Prive': 'mean'
                }).reset_index().sort_values('CA_Prive_Estime', ascending=False).head(15)

                fig = px.bar(
                    top_ca_prive,
                    y='Libelle',
                    x='CA_Prive_Estime',
                    orientation='h',
                    title="",
                    color='CA_Prive_Estime',
                    color_continuous_scale=[[0, COLORS['quaternary']], [1, COLORS['tertiary']]],
                    hover_data={'Effectif': ':,', 'Tarif_Prive': ':,.0f'},
                    labels={'CA_Prive_Estime': 'CA (€)', 'Effectif': 'Effectif', 'Tarif_Prive': 'Tarif (€)'}
                )
                fig.update_traces(texttemplate='%{x:,.0f}€', textposition='outside')
                fig.update_layout(
                    height=600,
                    showlegend=False,
                    yaxis=dict(title=''),
                    xaxis=dict(title='Chiffre d\'Affaires (€)'),
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            with col2:
                st.markdown("### 📊 Volume vs Valorisation (Privé)")

                # Agréger par GHM
                ghm_prive = df_prive.groupby(['Code_GHM', 'Libelle']).agg({
                    'Effectif': 'sum',
                    'CA_Prive_Estime': 'sum',
                    'Tarif_Prive': 'mean',
                    'DMS': 'mean'
                }).reset_index().nlargest(30, 'CA_Prive_Estime')

                fig = px.scatter(
                    ghm_prive,
                    x='Effectif',
                    y='CA_Prive_Estime',
                    size='Tarif_Prive',
                    hover_name='Libelle',
                    hover_data={'Effectif': ':,', 'CA_Prive_Estime': ':,.0f', 'Tarif_Prive': ':,.0f', 'DMS': ':.1f'},
                    title="",
                    color='Tarif_Prive',
                    color_continuous_scale=[[0, COLORS['quaternary']], [1, COLORS['tertiary']]],
                    labels={
                        'Effectif': 'Volume',
                        'CA_Prive_Estime': 'CA Privé (€)',
                        'Tarif_Prive': 'Tarif (€)',
                        'DMS': 'DMS (j)'
                    }
                )
                fig.update_layout(
                    height=600,
                    margin=dict(l=20, r=20, t=20, b=20)
                )
                st.plotly_chart(fig, use_container_width=True)

            # Tableau récapitulatif Privé
            st.markdown("### 📋 Tableau Récapitulatif GHM Privé (Top 20 par CA)")

            recap_prive = df_prive.groupby(['Code_GHM', 'Libelle']).agg({
                'Effectif': 'sum',
                'CA_Prive_Estime': 'sum',
                'Tarif_Prive': 'mean',
                'DMS': 'mean'
            }).reset_index().sort_values('CA_Prive_Estime', ascending=False).head(20)

            recap_prive['% CA'] = (recap_prive['CA_Prive_Estime'] / ca_prive_total * 100).round(1)

            # Formater
            recap_prive['Effectif'] = recap_prive['Effectif'].apply(lambda x: f"{int(x):,}".replace(',', ' '))
            recap_prive['CA Privé'] = recap_prive['CA_Prive_Estime'].apply(lambda x: f"{x:,.0f} €".replace(',', ' '))
            recap_prive['Tarif'] = recap_prive['Tarif_Prive'].apply(lambda x: f"{x:,.0f} €".replace(',', ' '))
            recap_prive['DMS'] = recap_prive['DMS'].apply(lambda x: f"{x:.1f}j")
            recap_prive['% CA'] = recap_prive['% CA'].apply(lambda x: f"{x:.1f}%")

            recap_prive = recap_prive[['Code_GHM', 'Libelle', 'Effectif', 'CA Privé', 'Tarif', 'DMS', '% CA']]
            recap_prive.columns = ['Code GHM', 'Libellé', 'Effectif', 'CA Privé', 'Tarif Privé', 'DMS', '% CA']

            st.dataframe(recap_prive, use_container_width=True, hide_index=True, height=400)

# TAB 4: CARTE DE FRANCE INTERACTIVE
with tab4:
    st.markdown('<div class="section-title">Répartition Géographique de l\'Activité Hospitalière</div>', unsafe_allow_html=True)

    st.info("🌍 **Vue d'ensemble nationale** : Cette carte affiche l'activité de tous les établissements. Utilisez les filtres ci-dessous pour affiner votre analyse.")

    # Filtres dédiés pour la carte
    col_filter1, col_filter2, col_filter3 = st.columns(3)

    with col_filter1:
        # Filtre par établissement
        etab_options_map = ['Tous les établissements'] + sorted(df['Finess'].unique().tolist())
        etab_filter_map = st.selectbox(
            "Filtrer par établissement",
            options=etab_options_map,
            key="map_etab_filter"
        )

    with col_filter2:
        # Filtre par département
        dept_options_map = ['Tous les départements'] + sorted(df['Nom_Departement'].dropna().unique().tolist())
        dept_filter_map = st.selectbox(
            "Filtrer par département",
            options=dept_options_map,
            key="map_dept_filter"
        )

    with col_filter3:
        # Filtre par année
        annee_options_map = ['Toutes les années'] + sorted(df['Annee'].unique().tolist())
        annee_filter_map = st.selectbox(
            "Filtrer par année",
            options=annee_options_map,
            key="map_annee_filter"
        )

    # Appliquer les filtres
    df_map = df.copy()

    if etab_filter_map != 'Tous les établissements':
        df_map = df_map[df_map['Finess'] == etab_filter_map]

    if dept_filter_map != 'Tous les départements':
        df_map = df_map[df_map['Nom_Departement'] == dept_filter_map]

    if annee_filter_map != 'Toutes les années':
        df_map = df_map[df_map['Annee'] == annee_filter_map]

    # Charger le GeoJSON des départements
    geojson_path = Path("departements.geojson")
    if not geojson_path.exists():
        st.error("Le fichier departements.geojson est introuvable. Veuillez le placer à la racine du projet.")
    else:
        with open(geojson_path, 'r', encoding='utf-8') as f:
            departements_geojson = json.load(f)

        # Agréger les données par département
        if 'Departement_Number' in df_map.columns and 'Nom_Departement' in df_map.columns:
            df_dept = df_map.groupby(['Departement_Number', 'Nom_Departement'], as_index=False).agg({
                'Effectif': 'sum',
                'DMS': lambda x: np.average(x, weights=df_map.loc[x.index, 'Effectif']) if df_map.loc[x.index, 'Effectif'].sum() > 0 else 0,
                'Age_Moyen': lambda x: np.average(x, weights=df_map.loc[x.index, 'Effectif']) if df_map.loc[x.index, 'Effectif'].sum() > 0 else 0,
                'Taux_Deces': lambda x: np.average(x, weights=df_map.loc[x.index, 'Effectif']) if df_map.loc[x.index, 'Effectif'].sum() > 0 else 0
            })

            # Calculer le nombre d'établissements par département
            df_nb_etab = df_map.groupby('Departement_Number')['Finess'].nunique().reset_index()
            df_nb_etab.columns = ['Departement_Number', 'Nb_Etablissements']
            df_dept = df_dept.merge(df_nb_etab, on='Departement_Number', how='left')

            # Titre dynamique selon les filtres
            titre_filtre = []
            if etab_filter_map != 'Tous les établissements':
                titre_filtre.append(f"Établissement: {finess_mapping.get(etab_filter_map, etab_filter_map)}")
            if dept_filter_map != 'Tous les départements':
                titre_filtre.append(f"Département: {dept_filter_map}")
            if annee_filter_map != 'Toutes les années':
                titre_filtre.append(f"Année: {annee_filter_map}")

            titre_carte = "Répartition de l'activité par département"
            if titre_filtre:
                titre_carte += f" - {' | '.join(titre_filtre)}"

            # Créer la carte choropleth
            fig_map = px.choropleth(
                df_dept,
                geojson=departements_geojson,
                locations='Departement_Number',
                featureidkey="properties.code",
                color='Effectif',
                hover_name='Nom_Departement',
                hover_data={
                    'Departement_Number': True,
                    'Effectif': ':,',
                    'Nb_Etablissements': True,
                    'DMS': ':.1f',
                    'Age_Moyen': ':.0f',
                    'Taux_Deces': ':.2f'
                },
                color_continuous_scale='YlOrRd',
                labels={
                    'Effectif': 'Effectif total',
                    'Nb_Etablissements': 'Nb établissements',
                    'DMS': 'DMS moyenne (jours)',
                    'Age_Moyen': 'Âge moyen (ans)',
                    'Taux_Deces': 'Taux de décès (%)',
                    'Departement_Number': 'Département'
                },
                title=titre_carte
            )

            # Ajuster la vue sur la France
            fig_map.update_geos(
                fitbounds="locations",
                visible=False
            )

            fig_map.update_layout(
                height=700,
                margin={"r": 0, "t": 50, "l": 0, "b": 0},
                coloraxis_colorbar={
                    'title': 'Effectif total',
                    'thickness': 20,
                    'len': 0.7
                }
            )

            st.plotly_chart(fig_map, use_container_width=True)

            # Tableau récapitulatif des départements
            st.markdown("### 📊 Top 10 Départements par Effectif")

            df_dept_sorted = df_dept.sort_values('Effectif', ascending=False).head(10)

            # Formater le tableau
            df_dept_display = df_dept_sorted.copy()
            df_dept_display['Effectif'] = df_dept_display['Effectif'].apply(lambda x: f"{x:,.0f}".replace(',', ' '))
            df_dept_display['Nb_Etablissements'] = df_dept_display['Nb_Etablissements'].astype(int)
            df_dept_display['DMS'] = df_dept_display['DMS'].apply(lambda x: f"{x:.1f}")
            df_dept_display['Age_Moyen'] = df_dept_display['Age_Moyen'].apply(lambda x: f"{x:.0f}")
            df_dept_display['Taux_Deces'] = df_dept_display['Taux_Deces'].apply(lambda x: f"{x:.2f}%")

            df_dept_display = df_dept_display.rename(columns={
                'Departement_Number': 'N° Dept',
                'Nom_Departement': 'Département',
                'Nb_Etablissements': 'Nb étab.',
                'DMS': 'DMS moy.',
                'Age_Moyen': 'Âge moy.',
                'Taux_Deces': 'Taux décès'
            })

            st.dataframe(df_dept_display, use_container_width=True, hide_index=True)

            # KPIs géographiques
            st.markdown("### 🎯 Indicateurs Géographiques")
            col1, col2, col3, col4 = st.columns(4)

            with col1:
                st.metric("Départements couverts", f"{len(df_dept)}")

            with col2:
                dept_max = df_dept.loc[df_dept['Effectif'].idxmax()]
                st.metric("Département principal", f"{dept_max['Nom_Departement']}", f"{dept_max['Effectif']:,.0f}".replace(',', ' '))

            with col3:
                concentration = (df_dept.nlargest(3, 'Effectif')['Effectif'].sum() / df_dept['Effectif'].sum() * 100) if len(df_dept) >= 3 else 100
                st.metric("Concentration Top 3", f"{concentration:.1f}%")

            with col4:
                nb_etab_total = df_map['Finess'].nunique()
                st.metric("Établissements", f"{nb_etab_total}")

        else:
            st.error("Les colonnes 'Departement_Number' et 'Nom_Departement' sont manquantes dans les données.")

# TAB 5: CLASSIFICATIONS
with tab5:
    st.markdown('<div class="section-title">Analyses par Classification</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Analyse par DA (Domaine d'Activité)
    with col1:
        if 'DA' in df_filtered.columns:
            df_da = compute_classification_data(df_filtered, 'DA')

            fig = px.bar(
                df_da,
                x='Effectif',
                y='DA',
                orientation='h',
                title="Top 10 Domaines d'Activité",
                color='Effectif',
                color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['tertiary']]],
                text='Effectif'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=500,
                showlegend=False,
                yaxis=dict(title=''),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

    # Analyse par Classification PKCS
    with col2:
        if 'Classif PKCS' in df_filtered.columns:
            df_pkcs = compute_classification_data(df_filtered, 'Classif PKCS')

            fig = px.bar(
                df_pkcs,
                x='Effectif',
                y='Classif PKCS',
                orientation='h',
                title="Top 10 Classifications PKCS",
                color='Effectif',
                color_continuous_scale=[[0, COLORS['secondary']], [1, COLORS['tertiary']]],
                text='Effectif'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=500,
                showlegend=False,
                yaxis=dict(title=''),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

    # Treemap hiérarchique
    if 'DA' in df_filtered.columns and 'GP' in df_filtered.columns:
        st.markdown('<div class="section-title">Vue Hiérarchique</div>', unsafe_allow_html=True)

        df_tree = df_filtered[
            (df_filtered['DA'] != 'Non renseigné') &
            (df_filtered['GP'] != 'Non renseigné')
        ].groupby(['DA', 'GP'])['Effectif'].sum().reset_index()

        df_tree = df_tree.sort_values('Effectif', ascending=False).head(50)

        fig = px.treemap(
            df_tree,
            path=['DA', 'GP'],
            values='Effectif',
            title="Hiérarchie DA > GP (Top 50)",
            color='Effectif',
            color_continuous_scale=[[0, COLORS['secondary']], [0.5, COLORS['primary']], [1, COLORS['tertiary']]]
        )
        fig.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

    # Sunburst
    if 'MCO' in df_filtered.columns and 'CAS' in df_filtered.columns:
        st.markdown('<div class="section-title">Répartition MCO / CAS</div>', unsafe_allow_html=True)

        df_sun = df_filtered[
            (df_filtered['MCO'] != 'Non renseigné') &
            (df_filtered['CAS'] != 'Non renseigné')
        ].groupby(['MCO', 'CAS'])['Effectif'].sum().reset_index()

        fig = px.sunburst(
            df_sun,
            path=['MCO', 'CAS'],
            values='Effectif',
            title="Répartition MCO / CAS",
            color='Effectif',
            color_continuous_scale=[[0, COLORS['quaternary']], [1, COLORS['tertiary']]]
        )
        fig.update_layout(
            height=600,
            margin=dict(l=20, r=20, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

# TAB 6: ÉVOLUTION TEMPORELLE
with tab6:
    st.markdown('<div class="section-title">Évolution Temporelle</div>', unsafe_allow_html=True)

    if len(annees_selectionnees) > 1:
        # Évolution globale (CACHE - évite recalcul weighted averages!)
        df_evol = compute_evolution_data(df_filtered)

        # Graphiques sur 2 colonnes
        col1, col2 = st.columns(2)

        with col1:
            fig = px.line(
                df_evol,
                x='Annee',
                y='Effectif',
                markers=True,
                title="Évolution de l'Effectif Total",
                color_discrete_sequence=[COLORS['primary']]
            )
            fig.update_traces(marker=dict(size=10), line=dict(width=3))
            fig.update_layout(
                height=350,
                xaxis=dict(title=''),
                yaxis=dict(title='Effectif'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        with col2:
            fig = px.line(
                df_evol,
                x='Annee',
                y='DMS',
                markers=True,
                title="Évolution de la DMS Moyenne",
                color_discrete_sequence=[COLORS['secondary']]
            )
            fig.update_traces(marker=dict(size=10), line=dict(width=3))
            fig.update_layout(
                height=350,
                xaxis=dict(title=''),
                yaxis=dict(title='DMS (jours)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        col3, col4 = st.columns(2)

        with col3:
            fig = px.line(
                df_evol,
                x='Annee',
                y='Age_Moyen',
                markers=True,
                title="Évolution de l'Âge Moyen",
                color_discrete_sequence=[COLORS['tertiary']]
            )
            fig.update_traces(marker=dict(size=10), line=dict(width=3))
            fig.update_layout(
                height=350,
                xaxis=dict(title=''),
                yaxis=dict(title='Âge (années)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        with col4:
            fig = px.line(
                df_evol,
                x='Annee',
                y='Taux_Deces',
                markers=True,
                title="Évolution du Taux de Décès",
                color_discrete_sequence=[COLORS['quaternary']]
            )
            fig.update_traces(marker=dict(size=10), line=dict(width=3))
            fig.update_layout(
                height=350,
                xaxis=dict(title=''),
                yaxis=dict(title='Taux de décès (%)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        # Top 5 libellés évolution
        st.markdown('<div class="section-title">Évolution des Principaux Libellés</div>', unsafe_allow_html=True)

        top5_libelles = df_filtered.groupby('Libelle')['Effectif'].sum().nlargest(5).index
        df_top5_evol = df_filtered[df_filtered['Libelle'].isin(top5_libelles)]
        df_top5_evol = df_top5_evol.groupby(['Annee', 'Libelle'])['Effectif'].sum().reset_index()

        fig = px.line(
            df_top5_evol,
            x='Annee',
            y='Effectif',
            color='Libelle',
            markers=True,
            title="Évolution des 5 Libellés Principaux",
            color_discrete_sequence=COLORS['palette']
        )
        fig.update_traces(marker=dict(size=8), line=dict(width=2))
        fig.update_layout(
            height=450,
            xaxis=dict(title=''),
            yaxis=dict(title='Effectif'),
            legend=dict(orientation="v", yanchor="top", y=1, xanchor="left", x=1.02),
            margin=dict(l=20, r=150, t=40, b=20)
        )
        st.plotly_chart(fig, width="stretch")

        # Analyse des plus fortes progressions/régressions
        st.markdown('<div class="section-title">Plus Fortes Variations</div>', unsafe_allow_html=True)

        # Calculer les variations entre première et dernière année
        annee_debut = min(annees_selectionnees)
        annee_fin = max(annees_selectionnees)

        df_debut = df_filtered[df_filtered['Annee'] == annee_debut].groupby('Libelle')['Effectif'].sum()
        df_fin = df_filtered[df_filtered['Annee'] == annee_fin].groupby('Libelle')['Effectif'].sum()

        df_variation = pd.DataFrame({
            'Effectif_debut': df_debut,
            'Effectif_fin': df_fin
        }).dropna()

        df_variation = df_variation[df_variation['Effectif_debut'] >= 5]  # Filtrer les petits effectifs
        df_variation['Variation_abs'] = df_variation['Effectif_fin'] - df_variation['Effectif_debut']
        df_variation['Variation_pct'] = (df_variation['Variation_abs'] / df_variation['Effectif_debut'] * 100)
        df_variation = df_variation.reset_index()

        col1, col2 = st.columns(2)

        with col1:
            # Top progressions
            df_prog = df_variation.sort_values('Variation_abs', ascending=False).head(10)

            fig = px.bar(
                df_prog,
                x='Variation_abs',
                y='Libelle',
                orientation='h',
                title=f"Top 10 Progressions ({annee_debut} → {annee_fin})",
                color='Variation_abs',
                color_continuous_scale=[[0, COLORS['tertiary']], [1, COLORS['secondary']]],
                text='Variation_abs'
            )
            fig.update_traces(texttemplate='%{text:+.0f}', textposition='outside')
            fig.update_layout(
                height=450,
                showlegend=False,
                yaxis=dict(title=''),
                xaxis=dict(title='Variation effectif'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        with col2:
            # Top régressions
            df_regr = df_variation.sort_values('Variation_abs', ascending=True).head(10)

            fig = px.bar(
                df_regr,
                x='Variation_abs',
                y='Libelle',
                orientation='h',
                title=f"Top 10 Régressions ({annee_debut} → {annee_fin})",
                color='Variation_abs',
                color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['quaternary']]],
                text='Variation_abs'
            )
            fig.update_traces(texttemplate='%{text:+.0f}', textposition='outside')
            fig.update_layout(
                height=450,
                showlegend=False,
                yaxis=dict(title=''),
                xaxis=dict(title='Variation effectif'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

    else:
        st.info("Sélectionnez plusieurs années pour voir l'évolution temporelle")

# TAB 7: EXPORT DONNÉES
with tab7:
    st.markdown('<div class="section-title">Export des Données</div>', unsafe_allow_html=True)

    # Options d'affichage
    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        recherche_table = st.text_input("Rechercher dans le tableau", "")

    with col2:
        nb_lignes = st.selectbox("Nombre de lignes", [100, 500, 1000, "Toutes"], index=0)

    with col3:
        tri_colonne = st.selectbox("Trier par", ['Effectif', 'DMS', 'Age_Moyen', 'Taux_Deces'], index=0)

    # Filtrer par recherche
    df_export = df_filtered.copy()
    if recherche_table:
        df_export = df_export[
            df_export['Libelle'].str.contains(recherche_table, case=False, na=False)
        ]

    # Trier
    df_export = df_export.sort_values(tri_colonne, ascending=False)

    # Limiter lignes
    if nb_lignes != "Toutes":
        df_export = df_export.head(nb_lignes)

    # Préparer pour affichage
    colonnes_export = ['Annee', 'Code_GHM', 'Libelle', 'Effectif', 'DMS', 'Age_Moyen', 'Sexe_Ratio', 'Taux_Deces']

    # Ajouter colonnes supplémentaires si disponibles
    if 'DA' in df_export.columns:
        colonnes_export.append('DA')
    if 'Classif PKCS' in df_export.columns:
        colonnes_export.append('Classif PKCS')

    df_export_display = df_export[colonnes_export].copy()

    # Renommer les colonnes
    rename_cols = {
        'Annee': 'Année',
        'Code_GHM': 'Code GHM',
        'Libelle': 'Libellé',
        'Effectif': 'Effectif',
        'DMS': 'DMS (j)',
        'Age_Moyen': 'Âge',
        'Sexe_Ratio': 'Sexe (%H)',
        'Taux_Deces': 'Décès (%)',
        'DA': 'Domaine Activité',
        'Classif PKCS': 'Classification'
    }
    df_export_display = df_export_display.rename(columns=rename_cols)

    # Arrondir
    if 'DMS (j)' in df_export_display.columns:
        df_export_display['DMS (j)'] = df_export_display['DMS (j)'].round(1)
    if 'Âge' in df_export_display.columns:
        df_export_display['Âge'] = df_export_display['Âge'].round(0)
    if 'Décès (%)' in df_export_display.columns:
        df_export_display['Décès (%)'] = df_export_display['Décès (%)'].round(2)

    st.dataframe(df_export_display, width="stretch", height=500)

    # Statistiques et boutons d'export
    col1, col2, col3 = st.columns([1, 1, 2])

    with col1:
        csv = df_export_display.to_csv(index=False, sep=';').encode('utf-8-sig')
        st.download_button(
            label="Télécharger CSV",
            data=csv,
            file_name=f"casemix_{etablissement_selectionne}_{pd.Timestamp.now().strftime('%Y%m%d')}.csv",
            mime="text/csv",
            width="stretch"
        )

    with col2:
        st.metric("Lignes exportées", f"{len(df_export_display):,}")

    with col3:
        st.info(f"Total disponible: {len(df_filtered):,} lignes")

# ========================================
# FOOTER
# ========================================

st.markdown("---")
st.markdown(f"""
<div style="text-align: center; padding: 20px; color: #999; font-size: 0.85rem;">
    <p style="margin: 0;">Dashboard Casemix GHM v5.0 | {len(df):,} lignes | {df['Finess'].nunique()} établissements</p>
    <p style="margin: 5px 0 0 0;">Enterprise Accounts - Jérémy Indelicato</p>
</div>
""", unsafe_allow_html=True)
