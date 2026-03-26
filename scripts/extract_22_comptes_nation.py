"""
Script d'extraction — Fichier: 22.Comptes de la nation_AS 2024.xlsx
Données extraites: PIB régional 2022 (sheet 16) et 2021 (sheet 17)
"""
import pandas as pd
SRC = "data_raw/hcp/22.Comptes de la nation_AS 2024.xlsx"
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
sectors = ["A00_Agriculture","A05_Peche","B00_Extraction","C00_Industrie_Manuf",
           "DE0_Elec_Eau","F00_Construction","G00_Commerce","H00_Transport",
           "I00_Hebergement","J00_InfoComm","K00_Finance","L68_Immobilier",
           "MN0_Recherche","O84_AdminPublique","PQ8_Education","RS0_Autres",
           "IS_Pt_Impots_Nets","PIB_Regional_MDH"]
results = []
for sheet, year in [(" 16", 2022), ("17", 2021)]:
    df = pd.read_excel(SRC, sheet_name=sheet, header=None)
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        r = get_region(cell)
        if r:
            try:
                vals = [float(row[j]) if pd.notna(row[j]) else 0 for j in range(1,19)]
                rec = {"Region": r, "Annee": year}
                for k, v in zip(sectors, vals): rec[k] = v
                results.append(rec)
            except: pass
result = pd.DataFrame(results)
result.to_csv(f"{OUT}/04_pib_regional_par_secteur.csv", index=False, encoding="utf-8-sig")
print(f"PIB régional: {len(result)} lignes → 04_pib_regional_par_secteur.csv")
