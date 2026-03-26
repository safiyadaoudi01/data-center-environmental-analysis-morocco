"""
Script d'extraction — Fichier: 8. Transport_AS 2024.xlsx
Données extraites: Réseau routier par région au 31/12/2023 + réseau total 2022-2023 (sheet 1-2)
"""
import pandas as pd
SRC = "data_raw/hcp/8. Transport_AS 2024.xlsx"
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
df = pd.read_excel(SRC, sheet_name="1-2", header=None)
# Routes par région (rows 11-23)
reg_data = []
for i in range(11, 24):
    row = df.iloc[i]
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    r = get_region(cell)
    if r and "total" not in cell.lower():
        try:
            reg_data.append({"Region": r, "Annee": 2023,
                             "Routes_Provinciales_Total_km": float(row[2]) if pd.notna(row[2]) else 0,
                             "Routes_Provinciales_Revetues_km": float(row[1]) if pd.notna(row[1]) else 0,
                             "Routes_Regionales_Total_km": float(row[4]) if pd.notna(row[4]) else 0,
                             "Routes_Nationales_Total_km": float(row[6]) if pd.notna(row[6]) else 0})
        except: pass
pd.DataFrame(reg_data).to_csv(f"{OUT}/07_transport_routes_par_region_2023.csv", index=False, encoding="utf-8-sig")
print(f"Routes par région 2023: {len(reg_data)} lignes → 07_transport_routes_par_region_2023.csv")
# Réseau total 2022-2023 (rows 34-40)
tot = []
for i in range(34, 41):
    row = df.iloc[i]
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if pd.notna(row[1]) and pd.notna(row[2]) and cell and cell!="nan":
        try:
            tot.append({"Type_Route": cell, "2023": float(str(row[1]).replace('*','')), "2022": float(row[2])})
        except: pass
pd.DataFrame(tot).to_csv(f"{OUT}/07b_transport_reseau_total_2022_2023.csv", index=False, encoding="utf-8-sig")
print(f"Réseau total: {len(tot)} lignes → 07b_transport_reseau_total_2022_2023.csv")
