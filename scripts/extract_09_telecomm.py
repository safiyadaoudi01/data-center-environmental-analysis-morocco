"""
Script d'extraction — Fichier: 9. Post-télécomm_AS 2024.xlsx
Données extraites: Indicateurs nationaux télécom 2022-2023 (sheet 7)
Note: Données à l'échelle nationale uniquement (pas de découpage régional dans ce fichier)
"""
import pandas as pd
SRC = "data_raw/hcp/9. Post-télécomm_AS 2024.xlsx"
OUT = "data_processed"
df = pd.read_excel(SRC, sheet_name="7", header=None)
data = []
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if not cell or cell=="nan": continue
    try:
        v23 = float(str(row[1]).strip().replace(',','')) if pd.notna(row[1]) and str(row[1]).strip() not in ['-','nan'] else None
        v22 = float(str(row[2]).strip().replace(',','').replace('R','').replace('م','').strip()) if pd.notna(row[2]) and str(row[2]).strip() not in ['-','nan'] else None
        if v23 is not None: data.append({"Indicateur": cell, "Annee": 2023, "Valeur": v23})
        if v22 is not None: data.append({"Indicateur": cell, "Annee": 2022, "Valeur": v22})
    except: pass
result = pd.DataFrame(data).dropna(subset=["Valeur"])
result.to_csv(f"{OUT}/08_telecomm_indicateurs_nationaux.csv", index=False, encoding="utf-8-sig")
print(f"Telecomm: {len(result)} lignes → 08_telecomm_indicateurs_nationaux.csv")
