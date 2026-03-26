"""
Script d'extraction — Fichier: 5. Energie et Eau_AS_2024.xlsx
Données extraites: 2022 et 2023 (avec données régionales)
"""
import pandas as pd, os
SRC = "data_raw/hcp/5. Energie et Eau_AS 2024.xlsx"
OUT = "data_processed"

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

# === DATASET 1: Ventes électricité par province (sheet 7-7suite) ===
df = pd.read_excel(SRC, sheet_name="7-7suite", header=None)
data, current_region = [], None
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    r = get_region(cell)
    if r: current_region = r
    if pd.notna(row[1]) and current_region and "source" not in cell.lower() and cell not in ["Total","المجموع"]:
        try:
            data += [{"Region": current_region, "Province_Prefecture": cell, "Annee": 2023, "Ventes_Electricite_Mm_KWh": round(float(row[1]),4)},
                     {"Region": current_region, "Province_Prefecture": cell, "Annee": 2022, "Ventes_Electricite_Mm_KWh": round(float(row[2]),4)}]
        except: pass
df1 = pd.DataFrame(data)
df1.to_csv(f"{OUT}/02_energie_ventes_electricite_par_province.csv", index=False, encoding="utf-8-sig")
print(f"Ventes electricite: {len(df1)} lignes → 02_energie_ventes_electricite_par_province.csv")

# === DATASET 2: Production eau superficielle par centre (sheet 19) ===
df = pd.read_excel(SRC, sheet_name="19", header=None)
data, current_region, current_province = [], None, None
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    r = get_region(cell)
    if r and pd.isna(row[3]) and pd.isna(row[4]): current_region = r; continue
    if r: current_province = cell; continue
    if pd.notna(row[1]) and current_region and "source" not in cell.lower():
        try:
            for yr, v in [(2023, row[3]), (2022, row[4])]:
                if pd.notna(v) and str(v).strip() not in ['-']:
                    data.append({"Region": current_region, "Province": current_province or cell,
                                 "Centre": str(row[1]).strip(), "Barrage_Oued": str(row[2]).strip() if pd.notna(row[2]) else "",
                                 "Annee": yr, "Production_Eau_m3": float(v)})
        except: pass
df2 = pd.DataFrame(data)
df2.to_csv(f"{OUT}/03a_eau_production_superficielle_par_centre.csv", index=False, encoding="utf-8-sig")
print(f"Production eau: {len(df2)} lignes → 03a_eau_production_superficielle_par_centre.csv")

# === DATASET 3: Activite ONEE eau par province 2023 (sheet 20-20suite) ===
df = pd.read_excel(SRC, sheet_name="20-20suite", header=None)
data, current_region = [], None
for _, row in df.iterrows():
    cell = str(row[0]).strip() if pd.notna(row[0]) else ""
    if not cell or cell=="nan" or "source" in cell.lower() or "compris" in cell.lower(): continue
    r = get_region(cell)
    if r: current_region = r
    if current_region and pd.notna(row[1]) and cell not in ["Ensemble","المجموع"]:
        try:
            nb = float(str(row[1]).replace(' ','').replace('-','0').replace('…','0'))
            va = float(str(row[2]).strip()) if pd.notna(row[2]) and str(row[2]).strip() not in ['-','…',''] else 0.0
            vr = float(str(row[3]).strip()) if pd.notna(row[3]) and str(row[3]).strip() not in ['-','…',''] else 0.0
            pr = float(str(row[4]).strip()) if pd.notna(row[4]) and str(row[4]).strip() not in ['-','…',''] else 0.0
            if pr > 0 or nb > 0:
                data.append({"Region": current_region, "Province_Prefecture": cell, "Annee": 2023,
                             "Nb_Abonnes": nb, "Ventes_Abonnes_m3k": va,
                             "Ventes_Regies_m3k": vr, "Production_Eau_m3k": pr})
        except: pass
df3 = pd.DataFrame(data)
df3.to_csv(f"{OUT}/03b_eau_onee_par_province_2023.csv", index=False, encoding="utf-8-sig")
print(f"ONEE eau 2023: {len(df3)} lignes → 03b_eau_onee_par_province_2023.csv")
