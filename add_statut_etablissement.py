"""
Script pour ajouter la colonne Statut_Etablissement (Public/Privé) au fichier casemix
Utilise:
1. Correspondance directe FINESS ET = FINESS EJ depuis statutjuridique-finessET.csv (45%)
2. Heuristique sur le nom d'établissement pour le reste (55%)
"""

import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Ajout du Statut Établissement (Public/Privé) ===\n")

# 1. Charger le fichier casemix
print("1️⃣ Chargement du fichier casemix...")
df_casemix = pd.read_parquet('data_casemix_2022_2024.parquet')
print(f"   ✓ {len(df_casemix):,} lignes chargées")
print(f"   ✓ {df_casemix['Finess'].nunique():,} établissements uniques")

# 2. Charger le référentiel statut juridique
print("\n2️⃣ Chargement du référentiel statut juridique...")
df_statut = pd.read_csv('statutjuridique-finessET.csv', sep=';', skiprows=1,
                        encoding='utf-8', header=None, low_memory=False)
df_statut = df_statut[df_statut[0] == 'structureej'].copy()
df_statut.columns = [f'col{i}' for i in range(len(df_statut.columns))]
df_statut = df_statut.rename(columns={
    'col1': 'finess_ej',
    'col2': 'nom',
    'col16': 'code_statut'
})

# Convertir code statut en numérique et classifier
df_statut['code_statut_num'] = pd.to_numeric(df_statut['code_statut'], errors='coerce')
df_statut['Statut_EJ'] = df_statut['code_statut_num'].apply(
    lambda x: 'Public' if pd.notna(x) and 1 <= x <= 52 else
              ('Privé' if pd.notna(x) and 60 <= x <= 95 else None)
)

# Garder uniquement les colonnes nécessaires
ref_statut = df_statut[['finess_ej', 'Statut_EJ']].dropna()
print(f"   ✓ {len(ref_statut):,} entités juridiques avec statut")
print(f"   ✓ Public: {(ref_statut['Statut_EJ']=='Public').sum():,}")
print(f"   ✓ Privé: {(ref_statut['Statut_EJ']=='Privé').sum():,}")

# 3. Merge avec correspondance directe FINESS ET = FINESS EJ
print("\n3️⃣ Tentative de correspondance directe FINESS ET = FINESS EJ...")
df_casemix = df_casemix.merge(
    ref_statut.rename(columns={'finess_ej': 'Finess', 'Statut_EJ': 'Statut_Etablissement'}),
    on='Finess',
    how='left'
)

nb_matches = df_casemix['Statut_Etablissement'].notna().sum()
print(f"   ✓ {nb_matches:,} lignes avec correspondance directe ({nb_matches/len(df_casemix)*100:.1f}%)")

# 4. Heuristique pour les non-matchés
print("\n4️⃣ Application de l'heuristique sur les noms pour les non-matchés...")

def classify_by_name(row):
    """Classifier selon le nom de l'établissement si pas de statut"""
    if pd.notna(row['Statut_Etablissement']):
        return row['Statut_Etablissement']

    nom = str(row['Nom_Etablissement']).upper()

    # Indicateurs de PRIVÉ
    private_keywords = [
        'CLINIQUE', 'POLYCLINIQUE', 'CENTRE DE SANTE', 'CABINET',
        'SOCIETE', 'S.A.', 'SAS', 'SARL', 'SELARL', 'ASSOCIATION',
        'FONDATION', 'CROIX ROUGE', 'MUTUALISTE'
    ]

    # Indicateurs de PUBLIC
    public_keywords = [
        'CHU', 'CH ', ' CH ', 'CENTRE HOSPITALIER', 'HOPITAL', 'HÔPITAL',
        'AP-HP', 'APHP', 'ASSISTANCE PUBLIQUE', 'HCL', 'HOSPICES CIVILS',
        'ETABLISSEMENT PUBLIC', 'CHIC', 'EPSM', 'EHPAD PUBLIC'
    ]

    # Vérifier privé en premier (plus spécifique)
    for keyword in private_keywords:
        if keyword in nom:
            return 'Privé'

    # Vérifier public
    for keyword in public_keywords:
        if keyword in nom:
            return 'Public'

    # Par défaut: si contient "ETABLISSEMENT" ou "ETABL." → Public
    # Sinon → Privé (principe de précaution, les privés sont majoritaires)
    if 'ETABL' in nom or 'ETAB' in nom:
        return 'Public'
    else:
        return 'Privé'  # Default

df_casemix['Statut_Etablissement'] = df_casemix.apply(classify_by_name, axis=1)

# 5. Statistiques finales
print("\n5️⃣ Statistiques de classification:")
print(f"   Total lignes: {len(df_casemix):,}")
print(f"   Public: {(df_casemix['Statut_Etablissement']=='Public').sum():,} lignes")
print(f"   Privé: {(df_casemix['Statut_Etablissement']=='Privé').sum():,} lignes")

# Par établissement
etab_stats = df_casemix.groupby(['Finess', 'Nom_Etablissement', 'Statut_Etablissement']).size().reset_index(name='count')
print(f"\n   Par établissement:")
print(f"   Public: {(etab_stats['Statut_Etablissement']=='Public').sum():,} établissements")
print(f"   Privé: {(etab_stats['Statut_Etablissement']=='Privé').sum():,} établissements")

# Exemples
print("\n6️⃣ Exemples de classification:")
print("\n   Établissements PUBLICS:")
publics = etab_stats[etab_stats['Statut_Etablissement']=='Public'].head(10)
for _, row in publics.iterrows():
    print(f"   {row['Finess']}: {row['Nom_Etablissement']}")

print("\n   Établissements PRIVÉS:")
prives = etab_stats[etab_stats['Statut_Etablissement']=='Privé'].head(10)
for _, row in prives.iterrows():
    print(f"   {row['Finess']}: {row['Nom_Etablissement']}")

# 6. Sauvegarder
print("\n7️⃣ Sauvegarde du fichier enrichi...")
df_casemix.to_parquet('data_casemix_2022_2024.parquet', index=False)
print(f"   ✓ Fichier sauvegardé: data_casemix_2022_2024.parquet")
print(f"   ✓ Nouvelle colonne: Statut_Etablissement")

print("\n✅ Traitement terminé avec succès!")