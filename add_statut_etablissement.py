"""
Script pour ajouter le statut Public/Privé aux établissements du casemix.

Méthode fiable : utilise le fichier FINESS etalab (ET) pour obtenir le FINESS EJ,
puis le fichier statutjuridique (EJ) pour obtenir le code statut juridique.

Classification :
  01-52 : Public (État, Commune, Département, EPH, CCAS...)
  60-66 : Privé Non Lucratif (Association Loi 1901, Fondation, Congrégation...)
  70-95 : Privé Commercial (SA, SARL, SAS, Personne Physique/Libéral...)
"""

import pandas as pd
import sys

sys.stdout.reconfigure(encoding='utf-8')

print("=== Ajout du Statut Établissement (Public/Privé) - V2 FIABLE ===\n")

# 1. Charger le fichier casemix
print("1. Chargement du fichier casemix...")
df_casemix = pd.read_parquet('data_casemix_2022_2024.parquet')
# Supprimer l'ancienne colonne si elle existe
if 'Statut_Etablissement' in df_casemix.columns:
    df_casemix = df_casemix.drop(columns=['Statut_Etablissement'])
if 'Statut_Detail' in df_casemix.columns:
    df_casemix = df_casemix.drop(columns=['Statut_Detail'])
# S'assurer que Finess est en string
df_casemix['Finess'] = df_casemix['Finess'].astype(str).str.strip()
print(f"   {len(df_casemix):,} lignes chargees")
print(f"   {df_casemix['Finess'].nunique():,} etablissements uniques")

# 2. Charger le fichier etalab (FINESS ET) — contient la correspondance ET → EJ
print("\n2. Chargement du referentiel etalab FINESS ET...")
df_etalab = pd.read_csv(
    'etalab-cs1100507-stock-20260107-0342 (2).csv',
    sep=';', skiprows=1, header=None, encoding='utf-8', low_memory=False, dtype=str
)
# Garder uniquement les lignes structureet
df_etalab = df_etalab[df_etalab[0] == 'structureet'].copy()
# Colonnes utiles : 1=FINESS_ET, 2=FINESS_EJ
df_etalab = df_etalab[[1, 2]].rename(columns={1: 'finess_et', 2: 'finess_ej'})
df_etalab['finess_et'] = df_etalab['finess_et'].str.strip()
df_etalab['finess_ej'] = df_etalab['finess_ej'].str.strip()
# Dédupliquer (un ET n'a qu'un seul EJ)
df_etalab = df_etalab.drop_duplicates(subset='finess_et')
print(f"   {len(df_etalab):,} etablissements ET avec correspondance EJ")

# 3. Charger le référentiel statut juridique (FINESS EJ)
print("\n3. Chargement du referentiel statut juridique (EJ)...")
df_statut = pd.read_csv(
    'statutjuridique-finessET.csv', sep=';', skiprows=1,
    header=None, encoding='utf-8', low_memory=False, dtype=str
)
df_statut = df_statut[df_statut[0] == 'structureej'].copy()
# Colonne 1 = FINESS EJ, colonne 16 = code statut juridique
df_statut = df_statut[[1, 16]].rename(columns={1: 'finess_ej', 16: 'code_statut'})
df_statut['finess_ej'] = df_statut['finess_ej'].str.strip()
df_statut['code_statut'] = pd.to_numeric(df_statut['code_statut'], errors='coerce')
# Dédupliquer
df_statut = df_statut.drop_duplicates(subset='finess_ej')
print(f"   {len(df_statut):,} entites juridiques avec code statut")

# 4. Construire la table de référence ET → statut
print("\n4. Construction de la table FINESS ET -> Statut...")
df_ref = df_etalab.merge(df_statut, on='finess_ej', how='left')

def classify_statut(code):
    if pd.isna(code):
        return None, None
    code = int(code)
    if 1 <= code <= 52:
        return 'Public', 'Public'
    elif 60 <= code <= 66:
        return 'Privé', 'Privé Non Lucratif'
    elif 67 <= code <= 95:
        return 'Privé', 'Privé Commercial'
    return None, None

df_ref[['Statut_Etablissement', 'Statut_Detail']] = df_ref['code_statut'].apply(
    lambda x: pd.Series(classify_statut(x))
)

ref_final = df_ref[['finess_et', 'Statut_Etablissement', 'Statut_Detail']].dropna()
print(f"   {len(ref_final):,} ET avec statut determine")
print(f"   Public : {(ref_final['Statut_Etablissement']=='Public').sum():,}")
print(f"   Prive  : {(ref_final['Statut_Etablissement']=='Privé').sum():,}")
print(f"     dont Non Lucratif : {(ref_final['Statut_Detail']=='Privé Non Lucratif').sum():,}")
print(f"     dont Commercial   : {(ref_final['Statut_Detail']=='Privé Commercial').sum():,}")

# 4b. Table de référence EJ → statut (pour les FINESS du casemix qui sont des EJ)
print("\n4b. Table FINESS EJ -> Statut (fallback)...")
ref_ej = df_statut.copy()
ref_ej[['Statut_Etablissement', 'Statut_Detail']] = ref_ej['code_statut'].apply(
    lambda x: pd.Series(classify_statut(x))
)
ref_ej = ref_ej[['finess_ej', 'Statut_Etablissement', 'Statut_Detail']].dropna()
print(f"   {len(ref_ej):,} EJ avec statut determine")

# 5. Merge avec le casemix — d'abord via FINESS ET, puis fallback via FINESS EJ
print("\n5. Merge avec le casemix...")
# Étape 1 : merge via FINESS ET
df_casemix = df_casemix.merge(
    ref_final.rename(columns={'finess_et': 'Finess'}),
    on='Finess',
    how='left'
)
nb_via_et = df_casemix['Statut_Etablissement'].notna().sum()
print(f"   Via FINESS ET : {nb_via_et:,} lignes ({nb_via_et/len(df_casemix)*100:.1f}%)")

# Étape 2 : fallback via FINESS EJ pour les non-matchés
mask_missing = df_casemix['Statut_Etablissement'].isna()
finess_missing = df_casemix.loc[mask_missing, 'Finess'].unique()
# Chercher ces FINESS dans la table EJ
ref_ej_match = ref_ej[ref_ej['finess_ej'].isin(finess_missing)].rename(
    columns={'finess_ej': 'Finess', 'Statut_Etablissement': 'Statut_EJ', 'Statut_Detail': 'Detail_EJ'}
)
df_casemix = df_casemix.merge(ref_ej_match, on='Finess', how='left')
# Remplir les manquants avec le fallback EJ
mask_fill = df_casemix['Statut_Etablissement'].isna() & df_casemix['Statut_EJ'].notna()
df_casemix.loc[mask_fill, 'Statut_Etablissement'] = df_casemix.loc[mask_fill, 'Statut_EJ']
df_casemix.loc[mask_fill, 'Statut_Detail'] = df_casemix.loc[mask_fill, 'Detail_EJ']
df_casemix = df_casemix.drop(columns=['Statut_EJ', 'Detail_EJ'])
nb_via_ej = mask_fill.sum()
print(f"   Via FINESS EJ : {nb_via_ej:,} lignes ({nb_via_ej/len(df_casemix)*100:.1f}%)")

nb_matches = df_casemix['Statut_Etablissement'].notna().sum()
nb_missing = df_casemix['Statut_Etablissement'].isna().sum()
print(f"   Matches : {nb_matches:,} lignes ({nb_matches/len(df_casemix)*100:.1f}%)")
print(f"   Manquants : {nb_missing:,} lignes ({nb_missing/len(df_casemix)*100:.1f}%)")

# 6. Traiter les non-matchés
if nb_missing > 0:
    finess_manquants = df_casemix[df_casemix['Statut_Etablissement'].isna()]['Finess'].unique()
    print(f"\n6. {len(finess_manquants)} etablissements sans statut :")
    for f in finess_manquants[:20]:
        nom = df_casemix[df_casemix['Finess'] == f]['Nom_Etablissement'].iloc[0] if 'Nom_Etablissement' in df_casemix.columns else '?'
        print(f"   {f} : {nom}")

    # Remplir les manquants par 'Inconnu'
    df_casemix['Statut_Etablissement'] = df_casemix['Statut_Etablissement'].fillna('Inconnu')
    df_casemix['Statut_Detail'] = df_casemix['Statut_Detail'].fillna('Inconnu')
    print(f"   -> Marques comme 'Inconnu'")

# 7. Statistiques finales
print("\n7. Statistiques finales :")
print(f"   Total lignes : {len(df_casemix):,}")
for statut in ['Public', 'Privé', 'Inconnu']:
    n = (df_casemix['Statut_Etablissement'] == statut).sum()
    print(f"   {statut:20s} : {n:>10,} lignes")

# Par établissement
etab_stats = df_casemix.groupby(['Finess', 'Statut_Etablissement']).size().reset_index(name='count')
etab_unique = etab_stats.drop_duplicates('Finess')
print(f"\n   Par etablissement :")
for statut in ['Public', 'Privé', 'Inconnu']:
    n = (etab_unique['Statut_Etablissement'] == statut).sum()
    print(f"   {statut:20s} : {n:>6,} etablissements")

# 8. Sauvegarder
print("\n8. Sauvegarde du fichier enrichi...")
df_casemix.to_parquet('data_casemix_2022_2024.parquet', index=False)
print(f"   Fichier sauvegarde : data_casemix_2022_2024.parquet")
print(f"   Colonnes ajoutees : Statut_Etablissement, Statut_Detail")

print("\nTermine avec succes !")
