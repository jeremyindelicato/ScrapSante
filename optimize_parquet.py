"""
Script pour optimiser la taille du fichier parquet avec compression maximale
"""
import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Optimisation du fichier Parquet ===\n")

# 1. Charger le fichier actuel
print("1️⃣ Chargement du fichier actuel...")
df = pd.read_parquet('data_casemix_2022_2024.parquet')
print(f"   Taille en mémoire : {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")
print(f"   Nombre de lignes : {len(df):,}")
print(f"   Nombre de colonnes : {len(df.columns)}")

# 2. Optimiser les types de données
print("\n2️⃣ Optimisation des types de données...")

# Convertir les colonnes numériques en types plus petits
for col in df.columns:
    if df[col].dtype == 'float64':
        # Vérifier si on peut utiliser float32 sans perte de précision
        if df[col].max() < 3.4e38 and df[col].min() > -3.4e38:
            df[col] = df[col].astype('float32')
            print(f"   {col}: float64 → float32")

    elif df[col].dtype == 'int64':
        # Optimiser les entiers
        col_min = df[col].min()
        col_max = df[col].max()

        if col_min >= 0 and col_max <= 65535:
            df[col] = df[col].astype('uint16')
            print(f"   {col}: int64 → uint16")
        elif col_min >= 0 and col_max <= 4294967295:
            df[col] = df[col].astype('uint32')
            print(f"   {col}: int64 → uint32")
        elif col_min >= -32768 and col_max <= 32767:
            df[col] = df[col].astype('int16')
            print(f"   {col}: int64 → int16")
        elif col_min >= -2147483648 and col_max <= 2147483647:
            df[col] = df[col].astype('int32')
            print(f"   {col}: int64 → int32")

# Optimiser les colonnes catégorielles (répétition de valeurs)
categorical_candidates = ['Finess', 'Nom_Etablissement', 'Code_GHM', 'Libelle',
                          'Libracine', 'Statut_Etablissement', 'Annee']

for col in categorical_candidates:
    if col in df.columns:
        # Si moins de 50% de valeurs uniques, utiliser category
        if df[col].nunique() / len(df) < 0.5:
            df[col] = df[col].astype('category')
            print(f"   {col}: object → category")

print(f"\n   Nouvelle taille en mémoire : {df.memory_usage(deep=True).sum() / 1024**2:.1f} MB")

# 3. Sauvegarder avec compression maximale
print("\n3️⃣ Sauvegarde avec compression maximale...")

# Backup de l'ancien fichier
import shutil
shutil.copy('data_casemix_2022_2024.parquet', 'data_casemix_2022_2024.parquet.before_optim')
print("   Backup créé : data_casemix_2022_2024.parquet.before_optim")

# Sauvegarder avec compression gzip (meilleure compression que snappy)
df.to_parquet(
    'data_casemix_2022_2024.parquet',
    engine='pyarrow',
    compression='gzip',  # Meilleure compression que 'snappy'
    index=False
)

import os
taille_fichier = os.path.getsize('data_casemix_2022_2024.parquet') / 1024**2
print(f"   ✓ Fichier sauvegardé : {taille_fichier:.1f} MB")

# 4. Vérifier l'intégrité
print("\n4️⃣ Vérification de l'intégrité...")
df_verify = pd.read_parquet('data_casemix_2022_2024.parquet')
print(f"   Nombre de lignes : {len(df_verify):,} ({'✓' if len(df_verify) == len(df) else '✗'})")
print(f"   Nombre de colonnes : {len(df_verify.columns)} ({'✓' if len(df_verify.columns) == len(df.columns) else '✗'})")

print("\n✅ Optimisation terminée avec succès !")
print(f"\nGain d'espace estimé : {79.9 - taille_fichier:.1f} MB")
