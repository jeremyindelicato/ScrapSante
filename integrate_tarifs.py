#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Script d'intégration des tarifs GHS dans le fichier Parquet principal
Fusionne les tarifs 2022, 2023, 2024 et les ajoute aux données casemix
"""

import pandas as pd
import re
from pathlib import Path
import numpy as np
import sys

# Configurer l'encodage de sortie
if sys.platform == 'win32':
    sys.stdout.reconfigure(encoding='utf-8')

def clean_tarif(val):
    """Nettoie les valeurs de tarifs"""
    if pd.isna(val):
        return None
    # Retirer espaces, €, caractères spéciaux, remplacer virgule par point
    val = str(val).strip()
    val = re.sub(r'[^\d,.]', '', val)  # Garder seulement chiffres, virgule, point
    val = val.replace(',', '.')
    val = val.replace(' ', '')
    try:
        return float(val)
    except:
        return None

print("="*80)
print("INTÉGRATION DES TARIFS GHS AU FICHIER CASEMIX")
print("="*80)
print()

# 1. Charger les fichiers de tarifs
print("📊 Chargement des fichiers de tarifs...")

tarifs_2024 = pd.read_csv('2024GHMGHS.csv', encoding='latin1', sep=';')
tarifs_2023 = pd.read_csv('2023GHMGHS.csv', encoding='latin1', sep=';')
tarifs_2022 = pd.read_csv('2022GHMGHS.csv', encoding='latin1', sep=';')

print(f"  ✓ 2024: {len(tarifs_2024):,} GHM")
print(f"  ✓ 2023: {len(tarifs_2023):,} GHM")
print(f"  ✓ 2022: {len(tarifs_2022):,} GHM")
print()

# 2. Nettoyer et standardiser les colonnes
print("🧹 Nettoyage des données...")

# 2024
tarifs_2024.columns = ['Code_GHM', 'Libelle_GHS', 'Tarif_Public_2024', 'Tarif_Prive_2024']
tarifs_2024['Tarif_Public_2024'] = tarifs_2024['Tarif_Public_2024'].apply(clean_tarif)
tarifs_2024['Tarif_Prive_2024'] = tarifs_2024['Tarif_Prive_2024'].apply(clean_tarif)

# 2023
tarifs_2023.columns = ['Code_GHM', 'Libelle_GHS', 'Tarif_Public_2023', 'Tarif_Prive_2023']
tarifs_2023['Tarif_Public_2023'] = tarifs_2023['Tarif_Public_2023'].apply(clean_tarif)
tarifs_2023['Tarif_Prive_2023'] = tarifs_2023['Tarif_Prive_2023'].apply(clean_tarif)

# 2022
tarifs_2022.columns = ['Code_GHM', 'Libelle_GHS', 'Tarif_Public_2022', 'Tarif_Prive_2022']
tarifs_2022['Tarif_Public_2022'] = tarifs_2022['Tarif_Public_2022'].apply(clean_tarif)
tarifs_2022['Tarif_Prive_2022'] = tarifs_2022['Tarif_Prive_2022'].apply(clean_tarif)

print(f"  ✓ Tarifs nettoyés et convertis en float")
print()

# 3. Fusionner tous les tarifs en un seul référentiel
print("🔗 Fusion des tarifs...")

# IMPORTANT: Supprimer les doublons en gardant la première occurrence
tarifs_2024_unique = tarifs_2024.drop_duplicates(subset=['Code_GHM'], keep='first')
tarifs_2023_unique = tarifs_2023.drop_duplicates(subset=['Code_GHM'], keep='first')
tarifs_2022_unique = tarifs_2022.drop_duplicates(subset=['Code_GHM'], keep='first')

print(f"  ✓ Doublons supprimés:")
print(f"    2024: {len(tarifs_2024)} → {len(tarifs_2024_unique)} GHM")
print(f"    2023: {len(tarifs_2023)} → {len(tarifs_2023_unique)} GHM")
print(f"    2022: {len(tarifs_2022)} → {len(tarifs_2022_unique)} GHM")

# Commencer avec 2024 (référentiel le plus récent)
tarifs_ref = tarifs_2024_unique[['Code_GHM', 'Libelle_GHS', 'Tarif_Public_2024', 'Tarif_Prive_2024']].copy()

# Ajouter 2023
tarifs_ref = tarifs_ref.merge(
    tarifs_2023_unique[['Code_GHM', 'Tarif_Public_2023', 'Tarif_Prive_2023']],
    on='Code_GHM',
    how='outer'
)

# Ajouter 2022
tarifs_ref = tarifs_ref.merge(
    tarifs_2022_unique[['Code_GHM', 'Tarif_Public_2022', 'Tarif_Prive_2022']],
    on='Code_GHM',
    how='outer'
)

# Réorganiser les colonnes
tarifs_ref = tarifs_ref[[
    'Code_GHM', 'Libelle_GHS',
    'Tarif_Public_2022', 'Tarif_Prive_2022',
    'Tarif_Public_2023', 'Tarif_Prive_2023',
    'Tarif_Public_2024', 'Tarif_Prive_2024'
]]

print(f"  ✓ Référentiel créé: {len(tarifs_ref):,} GHM uniques")
print()

# 4. Sauvegarder le référentiel seul
print("💾 Sauvegarde du référentiel GHS...")
tarifs_ref.to_parquet('referentiel_ghs_2022_2024.parquet', index=False)
tarifs_ref.to_csv('referentiel_ghs_2022_2024.csv', index=False, encoding='utf-8-sig')
print(f"  ✓ Référentiel sauvegardé (Parquet + CSV)")
print()

# 5. Charger le fichier casemix principal
print("📂 Chargement du fichier casemix principal...")
df_casemix = pd.read_parquet('data_casemix_2022_2024.parquet')
print(f"  ✓ {len(df_casemix):,} lignes chargées")
print()

# 6. Merger avec les données casemix
print("🔀 Fusion avec les données casemix...")

# Créer une colonne de tarif selon l'année
df_merged = df_casemix.merge(
    tarifs_ref,
    on='Code_GHM',
    how='left'
)

# Ajouter les colonnes de tarif actif selon l'année
df_merged['Tarif_Public'] = df_merged.apply(
    lambda row: row[f'Tarif_Public_{int(row["Annee"])}'] if pd.notna(row['Annee']) else None,
    axis=1
)

df_merged['Tarif_Prive'] = df_merged.apply(
    lambda row: row[f'Tarif_Prive_{int(row["Annee"])}'] if pd.notna(row['Annee']) else None,
    axis=1
)

# Calculer le CA estimé (Effectif × Tarif)
df_merged['CA_Public_Estime'] = df_merged['Effectif'] * df_merged['Tarif_Public']
df_merged['CA_Prive_Estime'] = df_merged['Effectif'] * df_merged['Tarif_Prive']

print(f"  ✓ Fusion réussie")
print()

# 7. Statistiques de matching
print("📊 Statistiques de matching...")
total_lignes = len(df_merged)
avec_tarif_public = df_merged['Tarif_Public'].notna().sum()
avec_tarif_prive = df_merged['Tarif_Prive'].notna().sum()

print(f"  Total lignes: {total_lignes:,}")
print(f"  Avec tarif public: {avec_tarif_public:,} ({avec_tarif_public/total_lignes*100:.1f}%)")
print(f"  Avec tarif privé: {avec_tarif_prive:,} ({avec_tarif_prive/total_lignes*100:.1f}%)")
print()

# 8. Supprimer les colonnes redondantes de l'ancien fichier
print("🧹 Nettoyage des colonnes redondantes...")
colonnes_a_supprimer = [
    'Duree_moyenne_sejour', 'Age_moyen', 'Sexe_ratio_pct_homme', 'Pct_deces'
]
colonnes_existantes = [col for col in colonnes_a_supprimer if col in df_merged.columns]
if colonnes_existantes:
    df_merged = df_merged.drop(columns=colonnes_existantes)
    print(f"  ✓ Supprimées: {', '.join(colonnes_existantes)}")
else:
    print(f"  ℹ Aucune colonne redondante trouvée")
print()

# 9. Sauvegarder le nouveau fichier
print("💾 Sauvegarde du fichier enrichi...")

# Backup de l'ancien fichier
import shutil
backup_path = 'data_casemix_2022_2024.parquet.backup'
if not Path(backup_path).exists():
    shutil.copy('data_casemix_2022_2024.parquet', backup_path)
    print(f"  ✓ Backup créé: {backup_path}")

# Sauvegarder le nouveau
df_merged.to_parquet('data_casemix_2022_2024.parquet', index=False)
print(f"  ✓ Fichier principal mis à jour")
print()

# 10. Statistiques finales
print("="*80)
print("✅ INTÉGRATION TERMINÉE AVEC SUCCÈS")
print("="*80)
print()
print(f"📊 Nouvelles colonnes ajoutées:")
print(f"  - Libelle_GHS (libellé officiel complet)")
print(f"  - Tarif_Public_2022, Tarif_Prive_2022")
print(f"  - Tarif_Public_2023, Tarif_Prive_2023")
print(f"  - Tarif_Public_2024, Tarif_Prive_2024")
print(f"  - Tarif_Public (tarif actif selon l'année)")
print(f"  - Tarif_Prive (tarif actif selon l'année)")
print(f"  - CA_Public_Estime (Effectif × Tarif Public)")
print(f"  - CA_Prive_Estime (Effectif × Tarif Privé)")
print()

# Statistiques de CA
ca_public_total = df_merged['CA_Public_Estime'].sum()
ca_prive_total = df_merged['CA_Prive_Estime'].sum()
print(f"💰 Chiffres d'affaires estimés (2022-2024):")
print(f"  Public: {ca_public_total:,.0f} €")
print(f"  Privé:  {ca_prive_total:,.0f} €")
print(f"  Total:  {ca_public_total + ca_prive_total:,.0f} €")
print()

print(f"📁 Fichiers générés:")
print(f"  - data_casemix_2022_2024.parquet (enrichi avec tarifs)")
print(f"  - referentiel_ghs_2022_2024.parquet (référentiel seul)")
print(f"  - referentiel_ghs_2022_2024.csv (référentiel CSV)")
print()
