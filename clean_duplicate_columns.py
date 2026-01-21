"""
Script pour supprimer les colonnes doublons et optimiser le parquet
"""
import pandas as pd
import sys
import os

sys.stdout.reconfigure(encoding='utf-8')

print("=== Nettoyage des Colonnes Doublons ===\n")

# 1. Charger le fichier
print("1️⃣ Chargement du fichier...")
df = pd.read_parquet('data_casemix_2022_2024.parquet')
taille_avant = os.path.getsize('data_casemix_2022_2024.parquet') / 1024**2
print(f"   Lignes : {len(df):,}")
print(f"   Colonnes avant : {len(df.columns)}")
print(f"   Taille fichier avant : {taille_avant:.1f} MB")

# 2. Identifier les colonnes à supprimer
print("\n2️⃣ Identification des colonnes doublons...")

colonnes_a_supprimer = [
    'Libelle_Raw',  # Doublon de 'Libelle'
    'DMS_Raw',      # Doublon de 'DMS'
    'Age_Raw',      # Doublon de 'Age_Moyen'
    'Sexe_Raw',     # Non utilisé dans le dashboard
    'Deces_Raw'     # Doublon de 'Taux_Deces' (après calcul)
]

colonnes_presentes = [col for col in colonnes_a_supprimer if col in df.columns]

print(f"   Colonnes à supprimer : {len(colonnes_presentes)}")
for col in colonnes_presentes:
    nunique = df[col].nunique()
    print(f"      - {col:20s} ({nunique:,} valeurs uniques)")

# 3. Vérifier qu'on ne perd pas d'info
print("\n3️⃣ Vérification de l'intégrité...")
verifications = {
    'Libelle_Raw': 'Libelle',
    'DMS_Raw': 'DMS',
    'Age_Raw': 'Age_Moyen'
}

for old_col, new_col in verifications.items():
    if old_col in df.columns and new_col in df.columns:
        # Vérifier si les valeurs sont identiques (ou très proches pour les floats)
        if df[old_col].dtype in ['float32', 'float64']:
            diff = (df[old_col] - df[new_col]).abs().max()
            print(f"   {old_col} vs {new_col}: diff max = {diff:.6f} ({'✓' if diff < 0.01 else '✗'})")
        else:
            identical = (df[old_col] == df[new_col]).all()
            print(f"   {old_col} vs {new_col}: {'✓ Identiques' if identical else '✗ Différents'}")

# 4. Supprimer les colonnes
print("\n4️⃣ Suppression des colonnes...")
df_clean = df.drop(columns=colonnes_presentes, errors='ignore')
print(f"   Colonnes après : {len(df_clean.columns)}")
print(f"   Colonnes supprimées : {len(df.columns) - len(df_clean.columns)}")

# 5. Remplir valeurs manquantes Libracine
print("\n5️⃣ Remplissage des valeurs manquantes...")
missing_libracine_avant = df_clean['Libracine'].isna().sum()
if missing_libracine_avant > 0:
    # Convertir en string si categorical
    if df_clean['Libracine'].dtype.name == 'category':
        df_clean['Libracine'] = df_clean['Libracine'].cat.add_categories(['Non classé'])
    df_clean['Libracine'] = df_clean['Libracine'].fillna('Non classé')
    print(f"   Libracine: {missing_libracine_avant:,} valeurs manquantes remplies par 'Non classé'")

# 6. Backup et sauvegarde
print("\n6️⃣ Sauvegarde...")
import shutil
if not os.path.exists('data_casemix_2022_2024.parquet.before_clean'):
    shutil.copy('data_casemix_2022_2024.parquet', 'data_casemix_2022_2024.parquet.before_clean')
    print("   ✓ Backup créé")

df_clean.to_parquet('data_casemix_2022_2024.parquet', compression='gzip', index=False)
taille_apres = os.path.getsize('data_casemix_2022_2024.parquet') / 1024**2

print(f"   ✓ Fichier sauvegardé")
print(f"   Taille après : {taille_apres:.1f} MB")
print(f"   Gain : {taille_avant - taille_apres:.1f} MB ({(taille_avant - taille_apres)/taille_avant*100:.1f}%)")

# 7. Vérification finale
print("\n7️⃣ Vérification finale...")
df_verify = pd.read_parquet('data_casemix_2022_2024.parquet')
print(f"   Lignes : {len(df_verify):,} ({'✓' if len(df_verify) == len(df) else '✗'})")
print(f"   Colonnes : {len(df_verify.columns)}")
print(f"   CA Public total : {df_verify['CA_Public_Estime'].sum()/1e9:.2f} Mds€")

print("\n✅ Nettoyage terminé avec succès !")
