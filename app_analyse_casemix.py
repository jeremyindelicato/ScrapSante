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
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS personnalisé - Design épuré et responsive
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

    /* Réduire les marges globales */
    .block-container {
        padding-top: 2rem;
        padding-bottom: 1rem;
        max-width: 100%;
    }

    /* Header personnalisé */
    .custom-header {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 8px;
        padding: 1.5rem;
        margin-bottom: 1.5rem;
        border-left: 4px solid var(--accent-color);
    }

    .custom-header h1 {
        color: var(--primary-color);
        font-size: 1.8rem;
        font-weight: 600;
        margin: 0;
    }

    .custom-header p {
        color: #666;
        font-size: 0.9rem;
        margin: 0.5rem 0 0 0;
    }

    /* Cards KPI */
    [data-testid="stMetricValue"] {
        font-size: 1.8rem;
        font-weight: 600;
        color: var(--primary-color);
    }

    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        font-weight: 500;
        color: #666;
    }

    /* Tabs styling */
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
    }

    .stTabs [aria-selected="true"] {
        color: var(--accent-color);
        border-bottom: 3px solid var(--accent-color);
        background-color: transparent;
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #1E1E1E;
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
    }

    [data-testid="stSidebar"] .stMultiSelect > div > div {
        background-color: #2A2A2A;
        border: 1px solid #444;
    }

    [data-testid="stSidebar"] .stTextInput > div > div > input {
        background-color: #2A2A2A;
        color: #E0E0E0;
        border: 1px solid #444;
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

    /* Boutons */
    .stButton > button {
        width: 100%;
        border-radius: 6px;
        border: 1px solid var(--border-color);
        font-weight: 500;
        transition: all 0.3s ease;
        background-color: transparent;
    }

    .stButton > button:hover {
        border-color: var(--accent-color);
        color: var(--accent-color);
        background-color: rgba(255, 181, 0, 0.1);
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

    /* Sections */
    .section-title {
        font-size: 1.3rem;
        font-weight: 600;
        color: var(--primary-color);
        margin: 2rem 0 1rem 0;
        padding-bottom: 0.5rem;
        border-bottom: 2px solid var(--border-color);
    }

    /* Graphiques */
    .plotly-graph-div {
        border-radius: 8px;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05);
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

        # OPTIMISATION CRITIQUE: Pre-indexer par Finess pour filtrage ultra-rapide
        df = df.set_index('Finess', drop=False)

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
# SIDEBAR - FILTRES
# ========================================

with st.sidebar:
    # Logo
    logo_path = Path("assets/logostrykerscansante.png")
    if logo_path.exists():
        st.image(str(logo_path), width="stretch")

    st.markdown("---")
    st.markdown("### Filtres")

    # Filtre années
    annees_disponibles = sorted(df['Annee'].unique())
    annees_selectionnees = st.multiselect(
        "Années",
        options=annees_disponibles,
        default=annees_disponibles,
        help="Sélectionnez les années à analyser"
    )

    # Filtre établissement
    etablissements_finess = sorted(df['Finess'].unique())

    def format_etablissement(finess):
        nom = finess_mapping.get(finess, df[df['Finess']==finess]['Nom_Etablissement'].iloc[0] if len(df[df['Finess']==finess]) > 0 else 'Inconnu')
        return f"{finess} - {nom}"

    etablissement_selectionne = st.selectbox(
        "Établissement",
        options=etablissements_finess,
        format_func=format_etablissement,
        help="Choisissez un établissement"
    )

    st.markdown("---")
    st.markdown("### Filtres avancés")

    # Filtre par classification
    if 'DA' in df.columns:
        da_disponibles = ['Tous'] + sorted([x for x in df['DA'].unique() if x != 'Non renseigné'])
        da_selectionne = st.selectbox("Domaine d'activité (DA)", options=da_disponibles)
    else:
        da_selectionne = 'Tous'

    if 'Classif PKCS' in df.columns:
        classif_disponibles = ['Tous'] + sorted([x for x in df['Classif PKCS'].unique() if x != 'Non renseigné'])
        classif_selectionne = st.selectbox("Classification PKCS", options=classif_disponibles)
    else:
        classif_selectionne = 'Tous'

    # Recherche par libellé
    st.markdown("---")
    recherche_libelle = st.text_input(
        "Recherche",
        placeholder="Rechercher un libellé GHM...",
        help="Ex: arthroplastie, coronaire..."
    )

    st.markdown("---")

    # Statistiques
    st.info(f"**Données chargées**\n\n{len(df):,} lignes\n\n{df['Finess'].nunique()} établissements")

    # Bouton reset
    if st.button("Réinitialiser", width="stretch"):
        st.cache_data.clear()
        st.rerun()

# ========================================
# FILTRAGE ULTRA-OPTIMISE AVEC INDEX ET SESSION STATE
# ========================================

def filter_data_ultra_fast(finess, annees, da, classif, recherche):
    """Filtrage ultra-rapide utilisant l'index Finess"""
    # Utilisation de l'index pour filtrage instantané par Finess
    df_filtered = df.loc[finess].copy() if finess in df.index else df[df['Finess'] == finess].copy()

    # Filtres additionnels
    if annees:
        df_filtered = df_filtered[df_filtered['Annee'].isin(annees)]

    if da != 'Tous':
        df_filtered = df_filtered[df_filtered['DA'] == da]

    if classif != 'Tous':
        df_filtered = df_filtered[df_filtered['Classif PKCS'] == classif]

    # Recherche dans les libelles (seulement si necessaire)
    if recherche:
        df_filtered = df_filtered[
            df_filtered['Libelle'].str.contains(recherche, case=False, na=False)
        ]

    return df_filtered

# Utilisation de session_state pour garder le dernier filtrage en memoire
cache_key = f"{etablissement_selectionne}_{tuple(annees_selectionnees) if annees_selectionnees else ()}_{da_selectionne}_{classif_selectionne}_{recherche_libelle}"

if 'last_cache_key' not in st.session_state or st.session_state.last_cache_key != cache_key:
    st.session_state.df_filtered = filter_data_ultra_fast(
        etablissement_selectionne,
        tuple(annees_selectionnees) if annees_selectionnees else (),
        da_selectionne,
        classif_selectionne,
        recherche_libelle
    )
    st.session_state.last_cache_key = cache_key

df_filtered = st.session_state.df_filtered

# ========================================
# EN-TÊTE
# ========================================

nom_etab = finess_mapping.get(
    etablissement_selectionne,
    df[df['Finess']==etablissement_selectionne]['Nom_Etablissement'].iloc[0] if len(df[df['Finess']==etablissement_selectionne]) > 0 else 'Inconnu'
)

st.markdown(f"""
<div class="custom-header">
    <h1>{nom_etab}</h1>
    <p>FINESS: {etablissement_selectionne} • Période: {', '.join(map(str, annees_selectionnees)) if annees_selectionnees else 'Toutes années'}</p>
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
# ONGLETS
# ========================================

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "Vue d'ensemble",
    "Analyses détaillées",
    "Classifications",
    "Évolution temporelle",
    "Export données"
])

# TAB 1: VUE D'ENSEMBLE
with tab1:
    st.markdown('<div class="section-title">Vue d\'ensemble de l\'activité</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        # Top 10 Libellés (optimisé avec groupby sort=False)
        with st.spinner('Chargement...'):
            df_top = df_filtered.groupby('Libelle', as_index=False, sort=False).agg({
                'Effectif': 'sum'
            }).nlargest(10, 'Effectif')

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

        # Ajouter ligne médiane
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

        # Créer des bins pour la DMS
        df_filtered_copy = df_filtered[df_filtered['DMS'].notna()].copy()

        fig.add_trace(go.Histogram(
            x=df_filtered_copy['DMS'],
            nbinsx=30,
            marker_color=COLORS['quaternary'],
            opacity=0.7,
            name='Distribution'
        ))

        # Ajouter ligne médiane
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

    # Répartition par année (si plusieurs années)
    if len(annees_selectionnees) > 1:
        st.markdown('<div class="section-title">Répartition temporelle</div>', unsafe_allow_html=True)

        col1, col2 = st.columns(2)

        with col1:
            df_annee = df_filtered.groupby('Annee')['Effectif'].sum().reset_index()

            fig = px.bar(
                df_annee,
                x='Annee',
                y='Effectif',
                title="Effectif par Année",
                color='Effectif',
                color_continuous_scale=[[0, COLORS['primary']], [1, COLORS['tertiary']]],
                text='Effectif'
            )
            fig.update_traces(texttemplate='%{text:,.0f}', textposition='outside')
            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis=dict(title=''),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

        with col2:
            # Variation annuelle
            df_annee['Variation'] = df_annee['Effectif'].pct_change() * 100

            fig = px.bar(
                df_annee[df_annee['Variation'].notna()],
                x='Annee',
                y='Variation',
                title="Variation Annuelle (%)",
                color='Variation',
                color_continuous_scale=['#823B8A', '#BB7702', '#307E84'],
                text='Variation'
            )
            fig.update_traces(texttemplate='%{text:+.1f}%', textposition='outside')
            fig.update_layout(
                height=350,
                showlegend=False,
                xaxis=dict(title=''),
                yaxis=dict(title='Variation (%)'),
                margin=dict(l=20, r=20, t=40, b=20)
            )
            st.plotly_chart(fig, width="stretch")

# TAB 2: ANALYSES DÉTAILLÉES
with tab2:
    st.markdown('<div class="section-title">Analyses Détaillées</div>', unsafe_allow_html=True)

    # Top 20 avec métriques complètes
    # Reset index pour que les lambdas avec weights fonctionnent correctement
    df_temp = df_filtered.reset_index(drop=True)
    df_detail = df_temp.groupby('Libelle', as_index=False).agg({
        'Effectif': 'sum',
        'DMS': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
        'Age_Moyen': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0,
        'Taux_Deces': lambda x: np.average(x, weights=df_temp.loc[x.index, 'Effectif']) if df_temp.loc[x.index, 'Effectif'].sum() > 0 else 0
    }).sort_values('Effectif', ascending=False).head(20)

    col1, col2 = st.columns(2)

    with col1:
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

# TAB 3: CLASSIFICATIONS
with tab3:
    st.markdown('<div class="section-title">Analyses par Classification</div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    # Analyse par DA (Domaine d'Activité)
    with col1:
        if 'DA' in df_filtered.columns:
            df_da = df_filtered[df_filtered['DA'] != 'Non renseigné'].groupby('DA')['Effectif'].sum().reset_index()
            df_da = df_da.sort_values('Effectif', ascending=False).head(10)

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
            df_pkcs = df_filtered[df_filtered['Classif PKCS'] != 'Non renseigné'].groupby('Classif PKCS')['Effectif'].sum().reset_index()
            df_pkcs = df_pkcs.sort_values('Effectif', ascending=False).head(10)

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
        # Évolution globale - Reset index pour weighted average
        df_temp_evol = df_filtered.reset_index(drop=True)
        df_evol = df_temp_evol.groupby('Annee', as_index=False).agg({
            'Effectif': 'sum',
            'DMS': lambda x: np.average(x, weights=df_temp_evol.loc[x.index, 'Effectif']) if df_temp_evol.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Age_Moyen': lambda x: np.average(x, weights=df_temp_evol.loc[x.index, 'Effectif']) if df_temp_evol.loc[x.index, 'Effectif'].sum() > 0 else 0,
            'Taux_Deces': lambda x: np.average(x, weights=df_temp_evol.loc[x.index, 'Effectif']) if df_temp_evol.loc[x.index, 'Effectif'].sum() > 0 else 0
        })

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
