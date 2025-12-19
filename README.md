---
title: Dashboard Casemix GHM
emoji: 📊
colorFrom: purple
colorTo: blue
sdk: streamlit
sdk_version: "1.52.1"
app_file: app_analyse_casemix.py
pinned: false
license: mit
---

# Dashboard Casemix GHM - Analyse Hospitalière 2022-2024

Application d'analyse de données hospitalières sur 3 ans (2022-2024) avec 2.2M lignes de données.

## 🎯 Fonctionnalités

### 1. Système de filtrage multi-critères avancé
- **Établissement** : Sélection par FINESS avec affichage du nom complet
- **Période temporelle** : Multi-sélection des années 2022, 2023, 2024
- **Domaine d'activité (DA)** : Filtrage par classification médicale
- **Classification PKCS** : Segmentation par type de prise en charge
- **Recherche textuelle** : Filtrage instantané dans les libellés GHM
- **Combinaison intelligente** : Tous les filtres s'appliquent simultanément

### 2. Analyses et visualisations interactives
- **KPIs en temps réel** : effectif total, GHM distincts, DMS moyenne, âge moyen, taux de décès
- **5 onglets d'analyse** : vue d'ensemble, analyses détaillées, classifications, évolution temporelle, export Excel
- **Graphiques dynamiques** : top 10/20, distributions, scatter plots, évolutions, treemaps

### 3. Performances optimisées
- **Format Parquet** : 40 MB (95% compression), chargement 7x plus rapide
- **2.2M lignes** de données pré-traitées et optimisées
- **Navigation ultra-rapide** : Index Finess + Session State

## 🛠️ Technologies

- **Streamlit** : Framework d'interface
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **PyArrow** : Format Parquet optimisé

## 🔐 Authentification

L'application est protégée par mot de passe. Le mot de passe doit être configuré dans les Secrets de Hugging Face Spaces.

## 📊 Données

- **2.2M lignes** de données hospitalières 2022-2024
- **Format Parquet** optimisé pour les performances
- Données anonymisées et agrégées
