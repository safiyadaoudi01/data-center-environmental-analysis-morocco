"""
Script d'extraction — Fichier: 6. Industrie et Artisanat_AS_2024.xlsx
Données extraites: Grandeurs industrielles par région 2022 (sheet 1)
"""
import pandas as pd
SRC = "data_raw/hcp/6. Industrie et Artisanat_AS 2024.xlsx"
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
df = pd.read_excel(SRC, sheet_name="1", header=None)
data = []
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    r = get_region(cell)
    if r:
        try:
            data.append({"Region": r, "Annee": 2022,
                         "Chiffre_Affaires_kDH": float(row[1]) if pd.notna(row[1]) else 0,
                         "Production_kDH": float(row[2]) if pd.notna(row[2]) else 0,
                         "Valeur_Ajoutee_kDH": float(row[3]) if pd.notna(row[3]) else 0,
                         "Investissements_kDH": float(row[4]) if pd.notna(row[4]) else 0})
        except: pass
result = pd.DataFrame(data)
result.to_csv(f"{OUT}/05_industrie_par_region_2022.csv", index=False, encoding="utf-8-sig")
print(f"✅ Industrie: {len(result)} lignes → 05_industrie_par_region_2022.csv")
