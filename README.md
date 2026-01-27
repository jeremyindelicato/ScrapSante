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

## Fonctionnalités

- **7 onglets** : Vue d'ensemble, Sélection Filtrée, Analyse Financière (Public/Privé), Carte de France, Comparaison Multi-Établissements, Évolution temporelle, Export données
- **KPIs avec delta** : effectif total, GHM distincts, DMS moyenne, âge moyen, taux de décès (vs année précédente)
- **Analyse financière** : CA estimé basé sur les tarifs GHS 2022-2024, séparé Public/Privé
- **Comparaison multi-établissements** : bar chart groupé par année sur un GHM sélectionné
- **Export** : CSV et Excel avec formatage

## Technologies

- **Streamlit** : Framework d'interface
- **Pandas / NumPy** : Manipulation de données
- **Plotly** : Visualisations interactives
- **PyArrow** : Format Parquet optimisé
- **openpyxl** : Export Excel formaté

## Données

- **2,222,698 lignes** de données hospitalières 2022-2024
- **1,252 établissements** (589 Public, 631 Privé, 32 Inconnu)
- **Format Parquet** optimisé (~43 MB, compression gzip)
- Classification Public/Privé fiable via référentiel FINESS officiel (99.2% de couverture)

## Classification Public/Privé

Source : référentiel FINESS etalab (ET) + statut juridique (EJ).

- Codes 01-52 : **Public** (État, Commune, Département, EPH, CCAS...)
- Codes 60-66 : **Privé Non Lucratif** (Association, Fondation, Congrégation...)
- Codes 67-95 : **Privé Commercial** (SA, SARL, SAS, Libéral...)

### 32 établissements sans statut connu

Ces établissements n'ont pas été retrouvés dans le référentiel FINESS (fermetures, fusions, erreurs de code...) :

| FINESS | Nom | Effectif total |
|--------|-----|---------------|
| 070004742 | CH DE LARGENTIERE | 31 |
| 170780167 | CH DE SAINT-JEAN-D'ANGELY | 9 176 |
| 200200145 | POLYCLINIQUE LA RESIDENCE | 24 427 |
| 220000046 | CH RENE PLEVEN DINAN | 31 749 |
| 220005045 | CH TREGUIER | 1 473 |
| 270000862 | CLINIQUE BERGOUIGNAN | 6 448 |
| 290000207 | CLINIQUE ST MICHEL ET STE ANNE | 4 499 |
| 290000215 | POLYCLINIQUE QUIMPER SUD | 6 243 |
| 300781465 | CLINIQUE KENNEDY | 2 574 |
| 320780067 | POLYCLINIQUE DE GASCOGNE | 8 021 |
| 410004998 | CLINIQUE DU SAINT COEUR | 15 157 |
| 460006075 | CLINIQUE FONT REDONDE | 78 |
| 500000138 | HL VILLEDIEU | 232 |
| 500000203 | POLYCLINIQUE DE LA MANCHE - SAINT-LO | 11 577 |
| 500000401 | CLINIQUE DR. H. GUILLARD | 9 093 |
| 500021944 | UNITE RADIOTHERAPIE EXTERNE CHERBOURG | 1 373 |
| 540000445 | ESPACE CHIRURGICAL AMBROISE PARE NANCY | 2 826 |
| 540000486 | POLYCLINIQUE DE GENTILLY | 16 723 |
| 650780158 | CH LOURDES | 7 308 |
| 690042080 | HOPITAL PRIVE NATECIA - GYNECOLOGIE | 367 |
| 690782248 | CH DE BEAUJEU | 436 |
| 750300410 | CLINIQUE JEANNE D'ARC | 2 073 |
| 760780825 | CLINIQUE DE L'ABBAYE | 7 517 |
| 770300192 | CLINIQUE ST BRICE | 1 549 |
| 830100103 | CLINIQUE STE MARGUERITE | 27 129 |
| 920300365 | CLINIQUE LA MONTAGNE | 14 117 |
| 920300712 | CENTRE CHIRURGICAL P. CHEREST | 9 383 |
| 920300761 | CLINIQUE HARTMANN | 8 495 |
| 930300298 | POLYCLINIQUE VAUBAN | 9 383 |
| 950001370 | GH CARNELLE-PORTES DE L'OISE | 8 201 |
| 950015289 | GH INTERCOMMUNAL DU VEXIN | 858 |
| 970462024 | CLINIQUE JEANNE D'ARC | 4 021 |
