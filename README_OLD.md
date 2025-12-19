# Dashboard Casemix GHM

Dashboard d'analyse des données hospitalières casemix 2022-2024.

## Installation locale

### Prérequis
- Python 3.8 ou supérieur
- pip

### Étapes d'installation

1. Clonez le repository
   ```bash
   git clone https://github.com/votre-username/casemix-dashboard.git
   cd casemix-dashboard
   ```

2. Installez les dépendances
   ```bash
   pip install -r requirements.txt
   ```

3. Configurez les variables d'environnement
   ```bash
   cp .env.example .env
   ```

   Puis modifiez `.env` avec votre mot de passe :
   ```
   DASHBOARD_PASSWORD=votre_mot_de_passe
   ```

4. Lancez l'application
   ```bash
   streamlit run app_analyse_casemix.py
   ```

5. Ouvrez votre navigateur à l'adresse : `http://localhost:8501`

## Déploiement sur Streamlit Cloud

Consultez le fichier [DEPLOYMENT.md](DEPLOYMENT.md) pour les instructions complètes de déploiement.

### Configuration rapide

1. Poussez votre code sur GitHub
2. Connectez-vous sur [share.streamlit.io](https://share.streamlit.io)
3. Créez une nouvelle app depuis votre repository
4. Configurez le secret `DASHBOARD_PASSWORD` dans les paramètres
5. Déployez !

## Fonctionnalités

- Authentification par mot de passe
- Vue d'ensemble de l'activité hospitalière
- Analyses détaillées avec corrélations
- Classifications par domaine d'activité et PKCS
- Évolution temporelle multi-années
- Export des données en CSV
- Design responsive et épuré
- Charte graphique Stryker

## Structure des données

Le dashboard utilise deux fichiers CSV :
- `data_casemix_2022_2024.csv` : Données d'activité casemix
- `etablissements_finess.csv` : Mapping des établissements FINESS

## Technologies

- **Streamlit** : Framework d'application web
- **Pandas** : Manipulation de données
- **Plotly** : Visualisations interactives
- **Python-dotenv** : Gestion des variables d'environnement

## Sécurité

- Mot de passe stocké dans variables d'environnement
- Fichier `.env` exclu de git via `.gitignore`
- Configuration des secrets pour Streamlit Cloud

## Auteur

Enterprise Accounts - Jérémy Indelicato

## Version

v5.0 - Dashboard optimisé avec design épuré et charte graphique Stryker
