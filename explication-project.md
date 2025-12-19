# PROJET DASHBOARD CASEMIX GHM - DOCUMENTATION COMPLÈTE

## CONTEXTE GÉNÉRAL

### Objectif du projet
Créer un dashboard d'analyse des données de séjours hospitaliers (GHM - Groupes Homogènes de Malades) extraites du site Scansanté pour les établissements de santé français.

### Données source
- **Source**: Site web Scansanté (données publiques)
- **Période**: 2022, 2023, 2024
- **Format**: Fichiers CSV par établissement et par année
- **Contenu**: Statistiques de séjours hospitaliers (effectifs, durée moyenne de séjour, âge moyen, etc.)

### Établissements
- Liste complète dans `etablissements_finess.csv`
- Identifiés par leur numéro FINESS (identifiant unique des établissements de santé)
- Mapping FINESS -> Nom de l'établissement

## HISTORIQUE DU PROJET

### Phase 1: Extraction des données (Scripts Python)
Plusieurs scripts de scraping ont été créés pour extraire les données de Scansanté:
- `scraper_casemix_2022.py`
- `scraper_casemix_2023.py`
- `scraper_casemix_2024.py`
- `rerun_2023_missing.py` (pour réextraire les données manquantes)

Ces scripts génèrent des fichiers CSV dans les dossiers `data/2022/`, `data/2023/`, `data/2024/`.

### Phase 2: Version Streamlit (Première version du dashboard)
Création de `app_analyse_casemix.py` - un dashboard interactif avec Streamlit.

**Fonctionnalités:**
- Filtrage par établissement (FINESS)
- Filtrage par années (checkboxes)
- Affichage de 4 KPIs principaux
- 4 onglets d'analyse avec graphiques Plotly
- Export CSV des données

**Optimisations effectuées:**
- Cache TTL (1h pour load_all_data, 30min pour aggregate_data_cached)
- Normalisation des colonnes Finess en string dès le chargement
- Conversion en types category pour Annee et CMD (économie mémoire)
- Tri des données par Finess et Annee (amélioration performance)
- Désactivation des animations Plotly (rendu instantané)

**Problèmes rencontrés et résolus:**
1. **Encodage CSV**: Double encodage UTF-8 lors de l'export -> Résolu en utilisant `to_csv()` sans encoding puis `.encode('utf-8-sig')` une seule fois
2. **Boutons sidebar**: Texte "keyboard_double_arrow_right" s'affichait au lieu des flèches -> Résolu en cachant complètement les boutons collapse avec `display: none`
3. **Animations de chargement**: Ajout de `st.spinner()` lors du changement d'établissement

### Phase 3: Version Web HTML/CSS/JS (Version actuelle)

**Motivation:**
- Meilleur contrôle du design (charte graphique Stryker)
- Performance améliorée (updates partiels vs reload complet)
- Vraie responsive mobile
- Architecture séparée Frontend/Backend

**Technologies:**
- **Backend**: FastAPI (Python)
- **Frontend**: HTML5, CSS3, JavaScript vanilla
- **Graphiques**: Plotly.js (équivalent JavaScript de Plotly Python)

## STRUCTURE DU PROJET

```
Casemix extraction/
│
├── data/                                # Données CSV
│   ├── 2022/
│   │   ├── 010007300_*.csv
│   │   ├── 010007987_*.csv
│   │   └── ... (environ 1500 fichiers)
│   ├── 2023/
│   │   └── ... (environ 1500 fichiers)
│   └── 2024/
│       └── ... (environ 1500 fichiers)
│
├── backend/                             # Backend FastAPI
│   ├── api.py                           # API REST (9 endpoints)
│   └── requirements.txt                 # Dépendances Python
│
├── frontend/                            # Frontend Web
│   ├── templates/
│   │   └── index.html                   # Page HTML principale
│   └── static/
│       ├── css/
│       │   └── style.css                # Styles CSS (charte Stryker)
│       └── js/
│           └── app.js                   # JavaScript + Plotly.js
│
├── assets/                              # Assets graphiques
│   ├── logostryker.png
│   ├── ROCK.TTF (police Rockwell)
│   └── ...
│
├── logs/                                # Logs des scrapers
│
├── __pycache__/                         # Cache Python
│
├── .venv/                               # Environnement virtuel Python
│
├── .claude/                             # Configuration Claude Code
│   └── settings.local.json
│
├── etablissements_finess.csv            # Mapping FINESS -> Nom
│
├── app_analyse_casemix.py               # VERSION STREAMLIT (conservée)
│
├── scraper_casemix_2022.py              # Scripts d'extraction
├── scraper_casemix_2023.py
├── scraper_casemix_2024.py
├── rerun_2023_missing.py
│
├── rapport_extraction.csv               # Rapports d'extraction
├── rapport_extraction_2022.csv
├── rapport_extraction_2023.csv
│
├── start_server.bat                     # Lancement serveur (Windows)
│
├── requirements.txt                     # Dépendances Streamlit
│
├── README_WEB_VERSION.md                # Doc complète version web
├── README_TOUTES_ANNEES.md              # Doc extraction données
├── LANCEMENT_WEB.txt                    # Guide rapide version web
├── LANCEMENT_RAPIDE.txt                 # Guide rapide Streamlit
├── RESUME_VERSION_WEB.md                # Résumé version web
├── GUIDE_COMPLET.txt                    # Guide complet Streamlit
│
└── explication-project.md               # CE FICHIER
```

## ARCHITECTURE TECHNIQUE

### Version Streamlit (app_analyse_casemix.py)

**Architecture monolithique:**
```
app_analyse_casemix.py
    ├── CSS inline (st.markdown)
    ├── Fonctions de chargement données
    ├── Fonctions de nettoyage
    ├── Fonctions d'agrégation
    ├── Interface utilisateur (st.sidebar, st.tabs, etc.)
    └── Graphiques Plotly
```

**Fonctions principales:**
- `load_finess_mapping()`: Charge le mapping FINESS -> Nom
- `load_all_data()`: Charge tous les CSV des 3 années (avec cache 1h)
- `clean_data(df)`: Nettoie et standardise les données
- `aggregate_data_cached()`: Agrège les données par établissement/année (cache 30min)
- `get_cmd_name(cmd_code)`: Retourne le nom d'une CMD

**Structure des données:**
```python
DataFrame colonnes:
- Code_GHM: Code du GHM (ex: "05M09T")
- Libelle: Libellé du GHM
- Effectif: Nombre de séjours
- Duree_Moyenne_Sejour: DMS en jours
- Age_Moyen: Âge moyen des patients
- Sexe_Ratio: Pourcentage d'hommes
- Taux_Deces: Pourcentage de décès
- CMD: Catégorie Majeure de Diagnostic (2 premiers caractères du GHM)
- Annee: Année (2022, 2023, 2024)
- Finess: Code FINESS de l'établissement
- Etablissement: Nom de l'établissement
```

**CMD (Catégories Majeures de Diagnostic):**
- 01: Affections du système nerveux
- 02: Affections de l'œil
- 03: Affections ORL
- 04: Affections de l'appareil respiratoire
- 05: Affections de l'appareil circulatoire
- 06: Affections du système digestif
- 07: Affections du système hépatobiliaire
- 08: Affections de l'appareil musculosquelettique
- 09: Affections de la peau
- 10: Affections endocriniennes
- 11: Affections du rein et des voies urinaires
- 12: Affections de l'appareil génital masculin
- 13: Affections de l'appareil génital féminin
- 14: Grossesses pathologiques
- 15: Nouveau-nés, prématurés
- 16: Affections du sang
- 17: Affections myéloprolifératives
- 18: Maladies infectieuses
- 19: Maladies mentales
- 20: Toxicomanies et troubles mentaux organiques
- 21: Traumatismes multiples graves
- 22: Brûlures
- 23: Facteurs influant sur l'état de santé
- 24: Séances
- 25: Maladies dues à une infection par le VIH
- 26: Traumatismes, allergies et empoisonnements
- 27: Transplantations d'organes
- 28: Séjours de moins de 2 jours

### Version Web (Backend FastAPI + Frontend HTML/CSS/JS)

**Architecture séparée:**
```
Frontend (Browser)
    ↓ HTTP Requests
Backend (FastAPI API REST)
    ↓ Pandas operations
Données (CSV files)
```

#### Backend (backend/api.py)

**API REST avec 9 endpoints:**

1. `GET /`
   - Sert la page HTML principale
   - Retourne: FileResponse(index.html)

2. `GET /api/etablissements`
   - Liste tous les établissements
   - Retourne: `{"etablissements": [{finess, nom, display}, ...]}`

3. `GET /api/annees`
   - Liste les années disponibles
   - Retourne: `{"annees": ["2022", "2023", "2024"]}`

4. `GET /api/kpis?finess={finess}&annees={annees}`
   - Calcule les KPIs pour un établissement
   - Params: finess (required), annees (optional, comma-separated)
   - Retourne: `{sejours_total, dms_moyenne, age_moyen, nb_ghm}`

5. `GET /api/top-ghm?finess={finess}&annees={annees}&limit={limit}`
   - Top N GHM les plus fréquents
   - Params: finess (required), annees (optional), limit (default: 10)
   - Retourne: `{ghm: [], libelle: [], effectif: []}`

6. `GET /api/evolution-temporelle?finess={finess}&annees={annees}`
   - Évolution temporelle des séjours
   - Retourne: `{annees: [], effectifs: []}`

7. `GET /api/distribution-cmd?finess={finess}&annees={annees}`
   - Distribution des séjours par CMD
   - Retourne: `{cmd: [], nom_cmd: [], effectif: []}`

8. `GET /api/comparaison?finess_list={finess1,finess2,...}&annees={annees}`
   - Compare plusieurs établissements
   - Params: finess_list (comma-separated, required)
   - Retourne: `{etablissements: [], cmd: [], data: [[]]}`

9. `GET /api/donnees-brutes?finess={finess}&annees={annees}&limit={limit}`
   - Données brutes pour tableau
   - Params: limit (default: 1000)
   - Retourne: `{columns: [], data: [{...}, ...]}`

**Fonctions réutilisées du Streamlit:**
Le backend réutilise 100% des fonctions de `app_analyse_casemix.py`:
- `load_finess_mapping()`
- `load_all_data()`
- `clean_data()`
- `get_cmd_name()`

**Cache:**
Utilise `@lru_cache(maxsize=1)` au lieu de `@st.cache_data`

**CORS:**
Configuré pour autoriser tous les origins en développement (`allow_origins=["*"]`)

#### Frontend (frontend/)

**Structure HTML (index.html):**
```html
<header>  <!-- Titre principal -->
<aside class="sidebar">  <!-- Filtres -->
    - Select établissement
    - Checkboxes années
    - Bouton Filtrer
    - Spinner de chargement
</aside>
<main>
    <section class="kpis">  <!-- 4 cartes KPI -->
    <section class="tabs">  <!-- 4 onglets -->
        <div id="tab1">  <!-- Top GHM + Évolution -->
        <div id="tab2">  <!-- Distribution CMD -->
        <div id="tab3">  <!-- Comparaison -->
        <div id="tab4">  <!-- Données brutes -->
</main>
<footer>
```

**CSS (style.css):**
- Variables CSS pour couleurs Stryker
- Layout avec sidebar fixe (desktop) ou en haut (mobile)
- Responsive breakpoints: 768px (tablet), 480px (mobile)
- Zones tactiles 44px minimum sur mobile
- Animations et transitions

**JavaScript (app.js):**

**État global:**
```javascript
state = {
    etablissements: [],
    anneesDisponibles: [],
    finessSelectionne: null,
    anneesSelectionnees: [],
    currentTab: 'tab1'
}
```

**Fonctions principales:**
- `loadEtablissements()`: Charge la liste via API
- `loadAnnees()`: Charge les années via API
- `handleFiltrer()`: Déclenché au clic sur "Filtrer"
- `loadKPIs()`: Charge et affiche les KPIs
- `loadTopGHM()`: Crée le graphique Top GHM (Plotly.js)
- `loadEvolutionTemporelle()`: Graphique évolution
- `loadDistributionCMD()`: Graphique camembert CMD
- `loadComparaison()`: Heatmap de comparaison
- `loadDonneesBrutes()`: Remplit le tableau
- `switchTab()`: Gestion des onglets
- `handleExportCSV()`: Export CSV avec BOM UTF-8

**Graphiques Plotly.js:**
Même configuration que Plotly Python:
- Type bar (horizontal) pour Top GHM
- Type scatter (lines+markers) pour évolution
- Type pie pour distribution CMD
- Type heatmap pour comparaison

## CHARTE GRAPHIQUE STRYKER

### Couleurs
- **Jaune Stryker**: `#FFB500` (couleur principale - KPIs, titres, bordures)
- **Noir Stryker**: `#1E1E1E` (textes, boutons, fond header)
- **Gris**: `#6C757D` (textes secondaires)
- **Gris clair**: `#F8F9FA` (fonds)

### Typographie
- **Titres H1**: Montserrat Extra Bold 900 (police Stryker)
- **Titres H2/H3**: Rockwell Bold 700
- **Texte courant**: Cambria (avec fallback Georgia, serif)
- **Données/KPIs**: Montserrat pour les chiffres

### Design
- Header avec dégradé gris foncé
- Sidebar jaune Stryker avec boutons noirs
- KPIs avec bordure jaune et dégradé blanc
- Graphiques avec couleurs basées sur le jaune Stryker
- Hover effects sur tous les éléments interactifs

## FONCTIONNALITÉS DÉTAILLÉES

### Filtrage
**Établissement:**
- Sélection unique via dropdown
- Format: "FINESS - Nom établissement"
- Liste triée par nom
- Environ 1500 établissements

**Années:**
- Checkboxes multiples
- 2022, 2023, 2024
- Toutes cochées par défaut
- Au moins une année doit être sélectionnée

### KPIs (4 indicateurs)
1. **Séjours Totaux**: Somme des effectifs
2. **DMS Moyenne**: Moyenne des durées moyennes de séjour (en jours, 1 décimale)
3. **Âge Moyen**: Moyenne des âges moyens (en ans, 1 décimale)
4. **Nombre GHM**: Nombre de GHM distincts

### Onglet 1: Top GHM & Évolution

**Graphique 1: Top 10 GHM**
- Type: Barre horizontale
- Données: 10 GHM les plus fréquents
- X: Effectif
- Y: Libellé GHM
- Couleur: Jaune Stryker
- Hauteur: 500px

**Graphique 2: Évolution temporelle**
- Type: Ligne avec marqueurs
- Données: Effectif total par année
- X: Année (catégorielle)
- Y: Nombre de séjours
- Couleur: Ligne jaune, marqueurs noirs
- Hauteur: 400px

### Onglet 2: Distribution CMD

**Graphique: Camembert**
- Données: Répartition des séjours par CMD
- Labels: Nom complet de la CMD
- Valeurs: Effectifs
- Couleurs: Palette générée autour du jaune Stryker
- Affichage: Label + pourcentage
- Hauteur: 600px

### Onglet 3: Comparaison

**Sélection:**
- Dropdown multiple (select multiple)
- Minimum 2 établissements requis
- Bouton "Comparer" pour lancer

**Graphique: Heatmap**
- Type: Heatmap
- X: CMD (colonnes)
- Y: Établissements (lignes)
- Z: Effectifs
- Colorscale: Blanc -> Jaune -> Noir
- Hauteur: Dynamique selon nombre d'établissements (400px + 30px par établissement)

### Onglet 4: Données brutes

**Tableau:**
- Colonnes: Année, Code GHM, Libellé, Effectif, DMS, Âge Moyen, CMD
- Formatage: DMS et Âge arrondi à 1 décimale
- Limite: 1000 lignes
- Style: Lignes alternées, hover effect
- Responsive: Scroll horizontal sur mobile

**Export CSV:**
- Bouton "Télécharger CSV"
- Encodage: UTF-8 avec BOM (compatibilité Excel)
- Séparateur: Point-virgule (;)
- Nom fichier: `casemix_export_YYYYMMDD_HHMMSS.csv`

## RESPONSIVE DESIGN

### Desktop (> 768px)
- Sidebar fixe à gauche (300px)
- Main content décalé de 300px
- Header fixe en haut (120px)
- 4 KPIs en ligne (grid auto-fit)
- Tabs en ligne

### Tablet (≤ 768px)
- Sidebar en position static (en haut)
- Main content pleine largeur
- Header réduit (100px)
- 2 KPIs par ligne
- Tabs potentiellement sur 2 lignes

### Mobile (≤ 480px)
- Sidebar pleine largeur
- 1 KPI par ligne (stack vertical)
- Tabs sur 2 lignes (50% chacun)
- Tableau: scroll horizontal
- Taille texte réduite

### Zones tactiles
- Minimum 44px de hauteur sur tous les éléments interactifs
- Détection via `@media (hover: none) and (pointer: coarse)`
- Font-size minimum 16px pour éviter le zoom automatique sur iOS

## OPTIMISATIONS PERFORMANCES

### Backend
1. **Cache LRU**:
   - `load_finess_mapping()`: maxsize=1
   - `load_all_data()`: maxsize=1
   - Cache en mémoire, pas de TTL (redémarrage serveur pour vider)

2. **Pandas optimisations**:
   - Conversion en types `category` pour Annee et CMD
   - Tri des données par Finess et Annee
   - Utilisation de masques booléens pour filtrage

3. **Chargement CSV**:
   - `low_memory=False` pour éviter les avertissements dtype
   - Nettoyage des lignes "Total" automatique
   - Gestion des erreurs par fichier (continue si échec)

### Frontend
1. **Updates partiels**: Seules les données nécessaires sont rechargées
2. **Plotly config**: `displaylogo: false`, `responsive: true`
3. **Pas d'animations Plotly**: Rendu instantané
4. **Lazy loading**: Tabs non actifs ne sont pas affichés (display: none)

### Données
- Taille totale: environ 4500 fichiers CSV (1500 par année)
- Taille mémoire: environ 2 GB une fois chargé en cache
- Temps de chargement initial: 1-2 minutes
- Temps de filtrage: < 1 seconde (grâce au cache)

## PROBLÈMES CONNUS ET SOLUTIONS

### 1. Encodage CSV Export
**Problème**: "Durée" devenait "DurÃ©e" dans Excel
**Cause**: Double encodage UTF-8
**Solution**:
```python
csv = df.to_csv(index=False, sep=';')  # Sans encoding
data=csv.encode('utf-8-sig')  # Encode une seule fois avec BOM
```

### 2. Boutons sidebar Streamlit
**Problème**: Texte "keyboard_double_arrow_right" affiché au lieu de flèche
**Tentatives échouées**:
- Material Symbols font
- ::before et ::after CSS
- text-indent technique
- font-size: 0

**Solution finale**: Cacher complètement les boutons
```css
button[kind="header"],
button[data-testid="baseButton-header"],
[data-testid="collapsedControl"] {
    display: none !important;
}
```

### 3. Serveur FastAPI ne démarre pas
**Problème**: `reload=True` dans uvicorn.run() causait erreur
**Solution**: Retirer `reload=True`
```python
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)  # Sans reload
```

### 4. Port déjà utilisé
**Problème**: ERR_CONNECTION_REFUSED sur localhost:8000
**Causes possibles**:
- Un autre processus utilise le port 8000
- Le serveur n'a pas démarré correctement
- Firewall bloque le port

**Solutions**:
- Vérifier qu'aucun autre serveur ne tourne
- Changer de port dans api.py et app.js
- Vérifier les logs de démarrage dans la fenêtre CMD

## LANCEMENT ET UTILISATION

### Version Streamlit
```bash
streamlit run app_analyse_casemix.py
```
Ouvre automatiquement le navigateur sur http://localhost:8501

### Version Web
```bash
# Méthode 1: Fichier .bat (Windows)
Double-cliquer sur: start_server.bat

# Méthode 2: Ligne de commande
cd backend
python api.py
```
Ouvrir manuellement: http://localhost:8000

**IMPORTANT**: Ne pas fermer la fenêtre CMD pendant l'utilisation

### Arrêt du serveur
- CTRL+C dans la fenêtre CMD
- Ou fermer la fenêtre CMD

## DÉPENDANCES

### Version Streamlit (requirements.txt)
```
streamlit
pandas
plotly
```

### Version Web Backend (backend/requirements.txt)
```
fastapi
uvicorn[standard]
pandas
python-multipart
```

### Version Web Frontend
- Plotly.js (CDN): https://cdn.plotly.ly/plotly-2.27.0.min.js
- Google Fonts Montserrat (CDN)
- CSS/JS vanilla (pas de framework)

## ENVIRONNEMENT DÉVELOPPEMENT

### Python
- Version: 3.13
- Environnement virtuel: `.venv/`
- Gestionnaire: pip

### IDE
- Claude Code (VS Code extension)
- Configuration: `.claude/settings.local.json`

### Système
- OS: Windows
- Encodage: UTF-8 avec BOM pour CSV
- Séparateur CSV: Point-virgule (;) pour compatibilité Excel France

## DÉPLOIEMENT (FUTUR)

### Version Streamlit
- **Streamlit Cloud**: Déploiement gratuit direct
- **Heroku**: Avec Procfile
- **Docker**: Dockerfile avec streamlit run

### Version Web
- **Serveur Linux**: Ubuntu/Debian recommandé
- **Reverse Proxy**: Nginx devant FastAPI
- **SSL**: Let's Encrypt pour HTTPS
- **Process Manager**: Supervisor ou PM2
- **Domaine**: Configuration DNS
- **Base de données**: Optionnel (actuellement fichiers CSV)

### Améliorations production
1. Authentification utilisateur (JWT)
2. Rate limiting API
3. CORS restreint aux domaines autorisés
4. Logging structuré (JSON)
5. Monitoring (Prometheus + Grafana)
6. Healthcheck endpoint
7. Base de données PostgreSQL (au lieu de CSV)
8. Cache Redis (au lieu de LRU en mémoire)

## COMPARAISON DES DEUX VERSIONS

| Critère | Streamlit | Web (FastAPI + HTML/CSS/JS) |
|---------|-----------|------------------------------|
| **Ligne de code** | ~1800 (1 fichier) | ~1550 (6 fichiers) |
| **Setup** | Très simple | Moyen (séparation backend/frontend) |
| **Design** | Limité par Streamlit | 100% personnalisable |
| **Performance** | Reload complet | Updates partiels |
| **Mobile** | Basique, responsive limitée | Vraie responsive, zones tactiles |
| **Backend** | Intégré | Séparé, API REST réutilisable |
| **Cache** | st.cache_data (TTL) | lru_cache (mémoire) |
| **Graphiques** | Plotly Python | Plotly.js (identique) |
| **Déploiement** | Streamlit Cloud | N'importe quel serveur |
| **État** | Session state automatique | État géré manuellement |
| **Debugging** | Console Streamlit | Console JavaScript + logs Python |
| **Courbe apprentissage** | Facile | Moyen |

## WORKFLOWS UTILISATEUR

### Workflow typique - Analyse établissement unique
1. Lancer le dashboard (Streamlit ou Web)
2. Sélectionner un établissement dans le dropdown
3. Cocher/décocher les années souhaitées
4. Cliquer sur "Filtrer"
5. Consulter les KPIs
6. **Tab 1**: Voir le Top 10 GHM et l'évolution temporelle
7. **Tab 2**: Analyser la distribution par CMD
8. **Tab 4**: Explorer les données brutes, exporter en CSV si besoin

### Workflow typique - Comparaison établissements
1. Lancer le dashboard
2. Aller dans **Tab 3**
3. Sélectionner 2+ établissements dans le dropdown multiple
4. Cliquer sur "Comparer"
5. Analyser la heatmap de comparaison

### Workflow typique - Export données
1. Filtrer sur un établissement et des années
2. Aller dans **Tab 4**
3. Vérifier les données dans le tableau
4. Cliquer sur "Télécharger CSV"
5. Ouvrir le CSV dans Excel (encodage UTF-8 avec BOM détecté automatiquement)

## MAINTENANCE ET ÉVOLUTION

### Ajout d'une nouvelle année (ex: 2025)
1. Créer le dossier `data/2025/`
2. Créer/adapter `scraper_casemix_2025.py`
3. Lancer l'extraction
4. Modifier le backend pour inclure 2025:
   - `load_all_data()`: Ajouter '2025' dans la boucle
   - Pas de modification frontend nécessaire (années chargées dynamiquement)

### Ajout d'un nouveau KPI
1. **Backend**: Ajouter le calcul dans `GET /api/kpis`
2. **Frontend HTML**: Ajouter une div.kpi-card
3. **Frontend JS**: Mettre à jour `loadKPIs()` pour afficher la valeur
4. **Streamlit**: Ajouter st.metric() dans la section KPIs

### Ajout d'un nouvel onglet
1. **Backend**: Créer un nouvel endpoint si besoin
2. **Frontend HTML**: Ajouter un bouton .tab-button et un div.tab-panel
3. **Frontend JS**: Créer la fonction de chargement des données
4. **Streamlit**: Ajouter un tab dans st.tabs()

### Modification du design
**Streamlit**: Modifier le CSS dans la string `css_content`
**Web**: Modifier `frontend/static/css/style.css`

## DONNÉES TECHNIQUES IMPORTANTES

### Format des fichiers CSV source
```
Séparateur: ;
Encodage: UTF-8 avec BOM
Colonnes (peuvent varier):
- Code GHM / Code
- Libellé / Libelle
- Effectif
- Durée moyenne de séjour / Durée moyennede séjour
- Age moyen
- Sexe ratio / Sexe ratio(% homme)
- % décès
```

### Nettoyage des données
1. Suppression des lignes vides
2. Suppression des lignes "Total"
3. Normalisation des noms de colonnes
4. Conversion des colonnes numériques (suppression %, espaces, virgule->point)
5. Extraction CMD depuis Code GHM (2 premiers caractères)
6. Filtrage CMD invalides (doit matcher `^\d{2}$`)
7. Suppression des lignes sans effectif ou effectif ≤ 0

### Performance - Temps de chargement
**Premier chargement (cache vide):**
- Streamlit: 60-90 secondes
- Web: 60-90 secondes

**Chargements suivants (cache actif):**
- Streamlit: < 1 seconde
- Web: < 1 seconde

**Filtrage établissement:**
- Streamlit: < 1 seconde (avec masques booléens)
- Web: < 1 seconde (backend filtré, frontend reçoit seulement les données nécessaires)

### Mémoire
- Données brutes en cache: ~2 GB
- Streamlit session state: ~50 MB par utilisateur
- Web backend: ~2 GB (partagé entre tous les utilisateurs)
- Web frontend: ~10 MB par utilisateur (JavaScript state)

## SÉCURITÉ

### Données sensibles
- **Aucune donnée patient individuelle**: Les données sont déjà agrégées
- **Données publiques**: Extraites de Scansanté (site public)
- **Pas d'authentification**: Actuellement pas de login requis

### Recommandations production
1. Ajouter authentification (JWT ou OAuth)
2. HTTPS obligatoire
3. Rate limiting sur l'API
4. Validation stricte des paramètres API
5. CORS restreint aux domaines autorisés
6. Pas de .env ou credentials.json dans Git
7. Logs d'accès et d'erreurs

### Fichiers à ne PAS commiter
- `.env`
- `credentials.json`
- `.venv/`
- `__pycache__/`
- `.DS_Store`
- `*.pyc`
- `.claude/settings.local.json` (contient des chemins locaux)

## TESTS

### Tests manuels effectués
- Chargement des données (3 années)
- Filtrage par établissement
- Filtrage par années
- Calcul des KPIs
- Génération des graphiques
- Export CSV
- Responsive mobile (Chrome DevTools)
- Compatibilité navigateurs (Chrome, Firefox, Edge)

### Tests à implémenter
- Tests unitaires backend (pytest)
- Tests API (pytest + httpx)
- Tests frontend (Jest + Testing Library)
- Tests d'intégration (Selenium)
- Tests de charge (Locust)
- Tests E2E (Playwright)

## LOGS ET DEBUGGING

### Streamlit
- Logs dans le terminal où streamlit run est lancé
- Erreurs affichées directement dans l'interface
- `st.write()` pour debug rapide

### Web Backend
- Logs dans le terminal où python api.py est lancé
- Format: `INFO:     127.0.0.1:xxxxx - "GET /api/endpoint HTTP/1.1" 200 OK`
- Ajouter `logging.basicConfig(level=logging.DEBUG)` pour plus de détails

### Web Frontend
- Console JavaScript (F12)
- Messages: "Initialisation...", "X établissements chargés", etc.
- Erreurs: Catchées et affichées via `alert()` ou console.error()

## CONTACT ET SUPPORT

### Documentation
- README_WEB_VERSION.md: Doc complète version web
- LANCEMENT_WEB.txt: Guide rapide version web
- GUIDE_COMPLET.txt: Guide Streamlit
- Ce fichier: Vue d'ensemble complète

### Support interne
- Développeur: Jérémy Indelicato
- Organisation: Stryker
- Usage: Interne uniquement

## NOTES FINALES

### Choix technologiques
- **Streamlit**: Choisi pour prototypage rapide
- **FastAPI**: Choisi pour performance et modernité (vs Flask)
- **Plotly**: Choisi pour interactivité et rendu identique Python/JS
- **Vanilla JS**: Choisi pour légèreté (vs React/Vue)

### Pérennité
- Code Python 3.13 compatible
- Pas de dépendances exotiques
- Architecture simple et maintenable
- Documentation complète

### Évolution possible
Le projet peut évoluer vers:
1. Dashboard temps réel (WebSocket)
2. Prédictions ML (tendances, anomalies)
3. Alertes automatiques (seuils dépassés)
4. Export PDF des rapports
5. Version mobile native (React Native)
6. Intégration avec d'autres sources de données

---

**DOCUMENT CRÉÉ LE**: 2024
**VERSION**: 1.0
**AUTEUR**: Jérémy Indelicato (avec assistance Claude Code)
**DERNIÈRE MISE À JOUR**: Session actuelle
