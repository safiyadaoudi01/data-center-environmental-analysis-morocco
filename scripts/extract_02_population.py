"""
Script d'extraction — Fichier: 2. population_AS 2024.xlsx
Données extraites: 2022 et 2023 (avec données régionales)
"""
from pathlib import Path
import pandas as pd, os

DATA_RAW_PATH = Path("data_raw/hcp/2. population_AS 2024.xlsx")
DATA_PROCESSED_PATH = Path("data_processed")


REGIONS = {"tanger":"Tanger - Tétouan - Al Hoceima","oriental":"L'Oriental",
           "fès":"Fès - Meknès","meknès":"Fès - Meknès","rabat":"Rabat - Salé - Kénitra",
           "béni":"Béni Mellal - Khénifra","casablanca":"Casablanca - Settat",
           "marrakech":"Marrakech - Safi","drâa":"Drâa - Tafilalet","souss":"Souss - Massa",
           "guelmim":"Guelmim - Oued Noun","laâyoune":"Laâyoune - Sakia El Hamra",
           "dakhla":"Dakhla - Oued Ed-Dahab"}
def get_region(t):
    for k,v in REGIONS.items():
        if k in str(t).lower(): return v
    return None

df_src = pd.read_excel(DATA_RAW_PATH, sheet_name="2", header=None)
data, current_region = [], None
for _, row in df_src.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if not cell or cell=="nan": continue
    r = get_region(cell)
    if r and "urbain" not in cell.lower() and "rural" not in cell.lower():
        current_region = r
        for yr, col in [(2023,2),(2022,3)]:
            try:
                val = int(float(str(row[col]).replace(' ','')))
                data.append({"Region": current_region, "Annee": yr, "Milieu": "Total", "Population": val})
            except: pass
    elif cell.lower() in ["urbain","rural"] and current_region:
        for yr, col in [(2023,2),(2022,3)]:
            try:
                val = int(float(str(row[col]).replace(' ','')))
                data.append({"Region": current_region, "Annee": yr, "Milieu": cell.capitalize(), "Population": val})
            except: pass
result = pd.DataFrame(data)
result.to_csv(f"{DATA_PROCESSED_PATH}/01_population_par_region.csv", index=False, encoding="utf-8-sig")
print(f"Population: {len(result)} lignes → 01_population_par_region.csv")
