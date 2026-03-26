"""
Script d'extraction — Fichier: 7. Construction et Foncier_AS 2024.xlsx
Données extraites: Autorisations de construire par province 2020 (sheet 11)
Note: Les données régionales disponibles sont pour 2020 uniquement dans ce fichier.
"""
import pandas as pd
SRC = "data_raw/hcp/7. Construction et Foncier_AS 2024.xlsx"
OUT = "data_processed"

REGIONS = {"tanger":"Tanger - Tétouan - Al Hoceima","oriental":"L'Oriental",
           "fès":"Fès - Meknès","rabat":"Rabat - Salé - Kénitra","béni":"Béni Mellal - Khénifra",
           "casablanca":"Casablanca - Settat","marrakech":"Marrakech - Safi","drâa":"Drâa - Tafilalet",
           "souss":"Souss - Massa","guelmim":"Guelmim - Oued Noun","laâyoune":"Laâyoune - Sakia El Hamra",
           "dakhla":"Dakhla - Oued Ed-Dahab"}
def get_region(t):
    for k,v in REGIONS.items():
        if k in str(t).lower(): return v
    return None
df = pd.read_excel(SRC, sheet_name="11", header=None)
data, current_region = [], None
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if not cell or cell=="nan" or "source" in cell.lower() or "année" in cell.lower(): continue
    r = get_region(cell)
    if r: current_region = r
    if current_region and pd.notna(row[1]):
        try:
            data.append({"Region": current_region, "Province_Prefecture": cell, "Annee": 2020,
                         "Nb_Autorisations": float(row[6]) if pd.notna(row[6]) else 0,
                         "Nb_Logements": float(row[2]) if pd.notna(row[2]) else 0,
                         "Nb_Pieces": float(row[1]) if pd.notna(row[1]) else 0,
                         "Valeur_Prevue_kDH": float(str(row[3]).replace(',','')) if pd.notna(row[3]) else 0,
                         "Surface_Batie_m2": float(row[4]) if pd.notna(row[4]) else 0,
                         "Surface_Planchers_m2": float(row[5]) if pd.notna(row[5]) else 0})
        except: pass
result = pd.DataFrame(data)
result.to_csv(f"{OUT}/06_construction_autorisations_par_province_2020.csv", index=False, encoding="utf-8-sig")
print(f"Construction (2020): {len(result)} lignes → 06_construction_autorisations_par_province_2020.csv")
