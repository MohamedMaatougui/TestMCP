# -*- coding: utf-8 -*-
import os
import pandas as pd
import re

print("=== Début de l'analyse Pandas (version propre & corrigée) ===")

# Dossier contenant les fichiers téléchargés
downloads_dir = r"c:\Users\Admin\Desktop\fac\3eme\3eme - 1ere sem\Python Framework for the Web\DJango\djangotesting\firstProject\INSEE_INJEP_downloads"

if not os.path.exists(downloads_dir):
    print("Erreur : le dossier de téléchargement n'existe pas.")
    exit(1)

# Trouver tous les fichiers .xlsx (sauf fichiers temporaires Excel commençant par ~$)
all_files = [
    os.path.join(downloads_dir, f)
    for f in os.listdir(downloads_dir)
    if f.endswith(".xlsx") and not f.startswith("~$")
]

print(f"[INFO] {len(all_files)} fichiers trouvés pour analyse dans {downloads_dir}")

combined_data = []

# Expression régulière pour repérer les nombres et années
numeric_pattern = re.compile(r"\b(?:\d+[.,]?\d*|(?:19|20)\d{2})\b")

for file in all_files:
    try:
        sheets = pd.read_excel(file, sheet_name=None)
        for sheet_name, df in sheets.items():
            df = df.dropna(how="all").dropna(axis=1, how="all")
            df.columns = [str(c).strip() for c in df.columns]

            # Ne garder que les colonnes texte / numériques
            df = df.select_dtypes(include=["object", "float", "int"])

            # Garder uniquement les lignes contenant au moins un nombre
            mask = df.astype(str).apply(lambda row: row.apply(lambda x: bool(numeric_pattern.search(x))).any(), axis=1)
            df = df[mask]

            if df.empty:
                continue

            combined_data.append(df)
            print(f"[OK] {os.path.basename(file)} - {sheet_name} ({len(df)} lignes conservées)")

    except Exception as e:
        print(f"[ERREUR] {os.path.basename(file)} : {e}")

if not combined_data:
    print("Aucune donnée utile trouvée.")
    exit(0)

# Fusion de toutes les données
full_df = pd.concat(combined_data, ignore_index=True).dropna(how="all").dropna(axis=1, how="all")

# Sauvegarde (ferme Excel avant de lancer le script)
output_path = os.path.join(downloads_dir, "consolidated_cleaned.xlsx")

try:
    full_df.to_excel(output_path, index=False)
    print(f"[SAUVEGARDÉ] Données nettoyées dans : {output_path}")
except PermissionError:
    print(f"[ERREUR] Impossible d'écrire dans {output_path}. Ferme le fichier Excel s'il est ouvert.")

print("=== Analyse terminée ===")
