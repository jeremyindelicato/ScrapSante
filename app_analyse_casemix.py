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
from dotenv import load_dotenv
import os

# Charger les variables d'environnement
load_dotenv()

# Configuration de la page
st.set_page_config(
    page_title="Casemix Dashboard",
    page_icon="assets/3xS.svg",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Design épuré et responsive avec animations
st.markdown("""
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

    /* Responsive */
    @media (max-width: 768px) {
        .block-container {
            padding: 1rem;
        }

        .custom-header h1 {
            font-size: 1.4rem;
        }

        [data-testid="stMetricValue"] {
            font-size: 1.4rem;
        }

        /* Réduire animations sur mobile pour performance */
        * {
            animation-duration: 0.3s !important;
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
        df = pd.read_csv('etablissements_finess.csv', sep=',', encoding='utf-8-sig', dtype=str)
        return dict(zip(df['Finess'], df['Raison sociale']))
    except:
        return {}

# Chargement des données
with st.spinner('Chargement des données...'):
    df = load_data()
    finess_mapping = load_finess_mapping()

# ========================================
# AUTHENTIFICATION
# ========================================

# Récupérer le mot de passe depuis les variables d'environnement
# En local: fichier .env
# Sur Streamlit Cloud: configurez dans Settings > Secrets
PASSWORD = os.getenv("DASHBOARD_PASSWORD")

# Vérification que le mot de passe est configuré
if not PASSWORD:
    st.error("⚠️ Configuration manquante : DASHBOARD_PASSWORD non défini")
    st.info("**Configuration requise :**\n\n- **Local :** Créez un fichier `.env` avec `DASHBOARD_PASSWORD=votre_mot_de_passe`\n\n- **Streamlit Cloud :** Ajoutez `DASHBOARD_PASSWORD` dans Settings > Secrets")
    st.stop()

if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

if not st.session_state.authenticated:
    st.markdown("<div style='margin-top: 60px;'></div>", unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        logo_path = Path("assets/logomotdepasse.png")
        if logo_path.exists():
            st.image(str(logo_path), width="stretch")

        st.markdown("""
        <div style="text-align: center; margin: 30px 0;">
            <h2 style="color: #FFB500; font-size: 24px;">Accès Sécurisé</h2>
            <p style="color: #666666; font-size: 16px;">Dashboard Casemix GHM</p>
        </div>
        """, unsafe_allow_html=True)

        with st.form(key="login_form"):
            password_input = st.text_input("Mot de passe", type="password", placeholder="Entrez le mot de passe...")
            submit_button = st.form_submit_button("Se connecter", width="stretch")

            if submit_button:
                if password_input == PASSWORD:
                    st.session_state.authenticated = True
                    st.rerun()
                else:
                    st.error("Mot de passe incorrect")

    st.stop()

# ========================================
# SIDEBAR - FILTRES (AVEC CACHE POUR LES LISTES)
# ========================================

# OPTIMISATION CRITIQUE: Calculer les listes de filtres UNE SEULE FOIS
@st.cache_data
def get_filter_options():
    """Calcule les options de filtres une seule fois au lieu de à chaque rerun"""
    return {
        'annees': sorted(df['Annee'].unique()),
        'finess': sorted(df['Finess'].unique()),
        'da': ['Tous'] + sorted([x for x in df['DA'].unique() if x != 'Non renseigné']) if 'DA' in df.columns else ['Tous'],
        'classif': ['Tous'] + sorted([x for x in df['Classif PKCS'].unique() if x != 'Non renseigné']) if 'Classif PKCS' in df.columns else ['Tous']
    }

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

    # Filtre établissement
    def format_etablissement(finess):
        nom = finess_mapping.get(finess, 'Inconnu')  # FIX CRITIQUE: Ne JAMAIS filtrer df ici!
        return f"{finess} - {nom}"

    etablissement_selectionne = st.selectbox(
        "Établissement",
        options=filter_opts['finess'],
        format_func=format_etablissement,
        help="Choisissez un établissement"
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
    # Filtrage direct par Finess avec masque booleen
    mask = (df['Finess'] == finess)

    # Filtrer par années
    if annees:
        mask &= df['Annee'].isin(annees)

    # Un seul filtrage à la fin - beaucoup plus rapide
    return df[mask].copy()

# Utilisation de session_state pour garder le dernier filtrage en memoire
cache_key = f"{etablissement_selectionne}_{tuple(annees_selectionnees) if annees_selectionnees else ()}"

if 'last_cache_key' not in st.session_state or st.session_state.last_cache_key != cache_key:
    st.session_state.df_filtered = filter_data_ultra_fast(
        etablissement_selectionne,
        tuple(annees_selectionnees) if annees_selectionnees else ()
    )
    st.session_state.last_cache_key = cache_key

df_filtered = st.session_state.df_filtered

# ========================================
# EN-TÊTE
# ========================================

nom_etab = finess_mapping.get(etablissement_selectionne, 'Inconnu')  # FIX: Ne pas filtrer df ici!

# Lire le SVG de l'hôpital
hospital_svg_path = Path("assets/hospital.svg")
if hospital_svg_path.exists():
    with open(hospital_svg_path, 'r', encoding='utf-8') as f:
        hospital_svg = f.read()
        # Extraire juste le SVG sans la déclaration XML
        hospital_svg = hospital_svg.replace('<?xml version="1.0" encoding="UTF-8"?>', '').strip()
else:
    hospital_svg = ""

st.markdown(f"""
<div class="custom-header">
    <div style="display: flex; align-items: center; gap: 1rem;">
        <div style="flex-shrink: 0; opacity: 0.9; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.1));">
            {hospital_svg}
        </div>
        <div style="flex-grow: 1;">
            <h1>{nom_etab}</h1>
            <p>FINESS: {etablissement_selectionne} • Période: {', '.join(map(str, annees_selectionnees)) if annees_selectionnees else 'Toutes années'}</p>
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
        return df_filtered.groupby('Libelle', as_index=False, sort=False).agg({
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

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Vue d'ensemble",
    "Sélection Filtrée",
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

# TAB 3: CLASSIFICATIONS
with tab3:
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

# TAB 4: ÉVOLUTION TEMPORELLE
with tab4:
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

# TAB 5: EXPORT DONNÉES
with tab5:
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
