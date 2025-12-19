#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script de conversion CSV vers Parquet
Convertit le gros CSV en format Parquet pour des performances optimales
"""

import pandas as pd
from pathlib import Path
import time

print("Conversion CSV vers Parquet")
print("=" * 50)

# Fichiers
csv_file = Path("data_casemix_2022_2024.csv")
parquet_file = Path("data_casemix_2022_2024.parquet")

if not csv_file.exists():
    print(f"ERREUR: Fichier {csv_file} introuvable!")
    exit(1)

# Taille du CSV
csv_size = csv_file.stat().st_size / (1024**3)
print(f"Taille du CSV : {csv_size:.2f} GB")

# Lecture du CSV
print("\nLecture du CSV...")
start = time.time()
df = pd.read_csv(csv_file, sep=';', encoding='utf-8-sig', low_memory=False)
read_time = time.time() - start
print(f"CSV lu en {read_time:.1f}s")
print(f"   {len(df):,} lignes x {len(df.columns)} colonnes")

# Nettoyer les colonnes
print("\nNettoyage des donnees...")
df.columns = df.columns.str.strip()

# Renommer les colonnes principales
rename_dict = {
    'Code': 'Code_GHM',
    'Libellé': 'Libelle_Raw',
    'Durée moyennede séjour': 'DMS_Raw',
    'Age moyen': 'Age_Raw',
    'Sexe ratio(% homme)': 'Sexe_Raw',
    '% décès': 'Deces_Raw'
}
df = df.rename(columns=rename_dict)

# Convertir les colonnes numériques
numeric_cols_to_clean = {
    'Effectif': 'Effectif',
    'DMS_Raw': 'DMS',
    'Age_Raw': 'Age_Moyen',
    'Sexe_Raw': 'Sexe_Ratio',
    'Deces_Raw': 'Taux_Deces'
}

for raw_col, new_col in numeric_cols_to_clean.items():
    if raw_col in df.columns:
        if raw_col in ['Sexe_Raw', 'Deces_Raw']:
            df[new_col] = pd.to_numeric(
                df[raw_col].str.replace('%', '', regex=False).str.replace(',', '.', regex=False),
                errors='coerce'
            )
        else:
            df[new_col] = pd.to_numeric(
                df[raw_col].str.replace(',', '.', regex=False) if df[raw_col].dtype == 'object' else df[raw_col],
                errors='coerce'
            )

# Libellé
if 'Libelle_Raw' in df.columns:
    df['Libelle'] = df['Libelle_Raw'].fillna('')

# Filtrer les lignes invalides
if 'Effectif' in df.columns and 'Libelle' in df.columns:
    mask = (
        df['Effectif'].notna() &
        (df['Effectif'] > 0) &
        (df['Libelle'] != '') &
        ~df['Libelle'].str.contains('Total', case=False, na=False)
    )
    df = df[mask].copy()
    print(f"{len(df):,} lignes apres filtrage")

# Optimisations de types
if 'Finess' in df.columns:
    df['Finess'] = df['Finess'].astype(str).str.strip()
if 'Annee' in df.columns:
    df['Annee'] = df['Annee'].astype('category')

# Colonnes catégorielles
categorical_cols = ['MCO', 'CAS', 'DA', 'GP', 'GA', 'Classif PKCS', 'Regroupement GHM PH']
for col in categorical_cols:
    if col in df.columns:
        df[col] = df[col].fillna('Non renseigné').astype('category')

# Ecriture Parquet
print("\nEcriture du fichier Parquet...")
start = time.time()
df.to_parquet(
    parquet_file,
    engine='pyarrow',
    compression='snappy',
    index=False
)
write_time = time.time() - start
print(f"Parquet ecrit en {write_time:.1f}s")

# Statistiques
parquet_size = parquet_file.stat().st_size / (1024**3)
compression_ratio = (1 - parquet_size / csv_size) * 100

print("\n" + "=" * 50)
print("RESULTATS")
print("=" * 50)
print(f"CSV    : {csv_size:.2f} GB")
print(f"Parquet: {parquet_size:.2f} GB")
print(f"Gain   : {compression_ratio:.1f}% de compression")
print(f"\nTemps de lecture CSV    : {read_time:.1f}s")
print(f"Temps d'ecriture Parquet: {write_time:.1f}s")

# Test de lecture Parquet
print("\nTest de lecture Parquet...")
start = time.time()
df_test = pd.read_parquet(parquet_file)
parquet_read_time = time.time() - start
print(f"Parquet lu en {parquet_read_time:.1f}s")
print(f"Gain de vitesse: {read_time / parquet_read_time:.1f}x plus rapide!")

print("\nConversion terminee avec succes!")
print(f"Fichier cree: {parquet_file}")
