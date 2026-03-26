"""
Script d'extraction — Fichier: 23. Environnement_AS 2024.xlsx
Données extraites:
  - Bilan ressources eau 2022-2023 (sheet ENV 9-10)
  - Apport eau par bassin versant 2022-2023 (sheet ENV 9-10)
  - Nombre de plages par région 2022-2023 (sheet ENV32-33-34)
"""
import pandas as pd
SRC = "data_raw/hcp/23. Environnement_AS 2024.xlsx"
OUT = "data_processed"

# === Bilan eau ===
df = pd.read_excel(SRC, sheet_name="ENV 9-10", header=None)
bilan, bassins, in_b = [], [], False
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if "bassin" in cell.lower(): in_b = True
    if not in_b and cell and cell!="nan" and pd.notna(row[3]):
        try: bilan.append({"Indicateur": cell, "Annee_Hydro": "2022-2023", "Valeur_Mm3": float(str(row[3]).strip())})
        except: pass
    if in_b and cell and cell not in ["nan","Total","Bassin versant","Millions de m3/ an","année2022-2023"]:
        try:
            ap = float(row[1]) if pd.notna(row[1]) else None
            su = float(row[3]) if pd.notna(row[3]) else None
            if ap: bassins.append({"Bassin_Versant": cell, "Annee_Hydro": "2022-2023", "Apport_Surface_Mm3": ap, "Superficie_km2": su})
        except: pass
pd.DataFrame(bilan).to_csv(f"{OUT}/09a_env_ressources_eau_bilan.csv", index=False, encoding="utf-8-sig")
pd.DataFrame(bassins).to_csv(f"{OUT}/09b_env_ressources_eau_par_bassin.csv", index=False, encoding="utf-8-sig")
print(f" Bilan eau: {len(bilan)} lignes; Bassins: {len(bassins)} lignes")

# === Plages ===
df = pd.read_excel(SRC, sheet_name="ENV32-33-34", header=None)
plages = []
for i in range(5, 18):
    row = df.iloc[i]
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if not cell or cell in ["nan","Total","المجمــوع","Région"]: continue
    try:
        v23 = int(float(row[3])) if pd.notna(row[3]) else None
        v22 = int(float(row[4])) if pd.notna(row[4]) else None
        if v23 is not None: plages.append({"Region": cell, "Annee": 2023, "Nb_Plages": v23})
        if v22 is not None: plages.append({"Region": cell, "Annee": 2022, "Nb_Plages": v22})
    except: pass
pd.DataFrame(plages).to_csv(f"{OUT}/10_env_plages_par_region.csv", index=False, encoding="utf-8-sig")
print(f" Plages: {len(plages)} lignes → 10_env_plages_par_region.csv")
