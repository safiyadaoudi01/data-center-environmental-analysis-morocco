"""
Scripts d'extraction définitifs — Annuaire Statistique Maroc 2024
Sources: 8 fichiers Excel fournis
Extraction des données régionales 2022 et 2023
"""
import pandas as pd
import os

SRC = "/mnt/user-data/uploads"
OUT = "/home/claude/csv_outputs"
os.makedirs(OUT, exist_ok=True)

REGIONS = {
    "tanger": "Tanger - Tétouan - Al Hoceima",
    "oriental": "L'Oriental",
    "fès": "Fès - Meknès",
    "meknès": "Fès - Meknès",
    "rabat": "Rabat - Salé - Kénitra",
    "béni": "Béni Mellal - Khénifra",
    "casablanca": "Casablanca - Settat",
    "marrakech": "Marrakech - Safi",
    "drâa": "Drâa - Tafilalet",
    "souss": "Souss - Massa",
    "guelmim": "Guelmim - Oued Noun",
    "laâyoune": "Laâyoune - Sakia El Hamra",
    "dakhla": "Dakhla - Oued Ed-Dahab"
}
def get_region(text):
    t = text.lower()
    for k, v in REGIONS.items():
        if k in t:
            return v
    return None

def is_region_header(cell, regions=REGIONS):
    return get_region(str(cell)) is not None

# =============================================================================
# 1. POPULATION par région (2-population sheet '2')
# =============================================================================
def extract_population():
    df = pd.read_excel(f"{SRC}/2__population_AS_2024.xlsx", sheet_name="2", header=None)
    data = []
    current_region = None
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan":
            continue
        r = get_region(cell)
        if r and "urbain" not in cell.lower() and "rural" not in cell.lower():
            current_region = r
            # col1=2024 col2=2023 col3=2022
            try:
                for yr, col in [(2023, 2), (2022, 3)]:
                    val = str(row[col]).replace(' ','').strip() if pd.notna(row[col]) else None
                    if val:
                        data.append({"Region": current_region, "Annee": yr,
                                     "Milieu": "Total", "Population": int(float(val))})
            except: pass
        elif cell.lower() in ["urbain", "rural"] and current_region:
            try:
                for yr, col in [(2023, 2), (2022, 3)]:
                    val = str(row[col]).replace(' ','').strip() if pd.notna(row[col]) else None
                    if val:
                        data.append({"Region": current_region, "Annee": yr,
                                     "Milieu": cell.capitalize(), "Population": int(float(val))})
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 2. ENERGIE — Ventes électricité par province/préfecture (sheet '7-7suite')
# =============================================================================
def extract_ventes_elec():
    df = pd.read_excel(f"{SRC}/5__Energie_et_Eau_AS_2024.xlsx", sheet_name="7-7suite", header=None)
    data = []
    current_region = None
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower():
            continue
        r = get_region(cell)
        if r:
            current_region = r
        if pd.notna(row[1]) and current_region and cell not in ["Total","المجموع"]:
            try:
                v23 = float(row[1])
                v22 = float(row[2])
                data.append({"Region": current_region, "Province_Prefecture": cell,
                              "Annee": 2023, "Ventes_Electricite_Mm_KWh": round(v23, 4)})
                data.append({"Region": current_region, "Province_Prefecture": cell,
                              "Annee": 2022, "Ventes_Electricite_Mm_KWh": round(v22, 4)})
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 3. EAU — Production eau superficielle par centre (sheet '19')
# =============================================================================
def extract_prod_eau():
    df = pd.read_excel(f"{SRC}/5__Energie_et_Eau_AS_2024.xlsx", sheet_name="19", header=None)
    data = []
    current_region = None
    current_province = None
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower():
            continue
        r = get_region(cell)
        # col3=2023, col4=2022R
        v23 = row[3]; v22 = row[4]
        if r and pd.isna(v23) and pd.isna(v22):
            current_region = r
            continue
        if r and current_region:
            current_province = cell
            continue
        if pd.notna(row[1]) and current_region:  # centre row
            centre = str(row[1]).strip() if pd.notna(row[1]) else ""
            barrage = str(row[2]).strip() if pd.notna(row[2]) else ""
            province = current_province or cell
            try:
                for yr, v in [(2023, v23), (2022, v22)]:
                    if pd.notna(v) and str(v).strip() not in ['-','']:
                        data.append({
                            "Region": current_region, "Province": province,
                            "Centre": centre, "Barrage_Oued": barrage,
                            "Annee": yr, "Production_Eau_m3": float(v)
                        })
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 4. EAU — Activité ONEE eau par province (sheet '20-20suite')  2023 seulement
# =============================================================================
def extract_onee_eau():
    df = pd.read_excel(f"{SRC}/5__Energie_et_Eau_AS_2024.xlsx", sheet_name="20-20suite", header=None)
    data = []
    current_region = None
    for i, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower() or "compris" in cell.lower():
            continue
        r = get_region(cell)
        if r and pd.isna(row[1]):
            current_region = r
            continue
        if current_region and (pd.notna(row[1]) or str(row[1]).strip() == ' -'):
            # col1=NbAbonnes, col2=VentesAbonnes, col3=VentesRegies, col4=Production
            try:
                nb = float(str(row[1]).replace(' ','').replace('-','0'))
                va = float(str(row[2]).strip()) if pd.notna(row[2]) and str(row[2]).strip() not in ['-','nan'] else 0.0
                vr = float(str(row[3]).strip()) if pd.notna(row[3]) and str(row[3]).strip() not in ['-','nan'] else 0.0
                pr = float(str(row[4]).strip()) if pd.notna(row[4]) and str(row[4]).strip() not in ['-','nan'] else 0.0
                if (pr > 0 or nb > 0) and cell not in ["Ensemble","المجموع"]:
                    data.append({
                        "Region": current_region, "Province_Prefecture": cell, "Annee": 2023,
                        "Nb_Abonnes": nb, "Ventes_Abonnes_m3k": va,
                        "Ventes_Regies_m3k": vr, "Production_Eau_m3k": pr
                    })
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 5. COMPTES RÉGIONAUX — PIB par secteur et région (sheets '16'=2022, '17'=2021)
# =============================================================================
def extract_pib():
    sectors = ["A00_Agriculture","A05_Peche","B00_Extraction","C00_Industrie_Manuf",
               "DE0_Elec_Eau","F00_Construction","G00_Commerce","H00_Transport",
               "I00_Hebergement","J00_InfoComm","K00_Finance","L68_Immobilier",
               "MN0_Recherche","O84_AdminPublique","PQ8_Education","RS0_Autres",
               "IS_Pt_Impots_Nets","PIB_Regional_MDH"]
    results = []
    for sheet, year in [(" 16", 2022), ("17", 2021)]:
        df = pd.read_excel(f"{SRC}/22_Comptes_de_la_nation_AS_2024.xlsx", sheet_name=sheet, header=None)
        for _, row in df.iterrows():
            cell = str(row[0]).strip() if pd.notna(row[0]) else ""
            r = get_region(cell)
            if r:
                try:
                    vals = [float(row[j]) if pd.notna(row[j]) else 0 for j in range(1, 19)]
                    rec = {"Region": r, "Annee": year}
                    for k, v in zip(sectors, vals):
                        rec[k] = v
                    results.append(rec)
                except: pass
    return pd.DataFrame(results)

# =============================================================================
# 6. INDUSTRIE — Grandeurs par région 2022 (sheet '1')
# =============================================================================
def extract_industrie():
    df = pd.read_excel(f"{SRC}/6__Industrie_et_artisanat_AS_2024.xlsx", sheet_name="1", header=None)
    data = []
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        r = get_region(cell)
        if r:
            try:
                data.append({
                    "Region": r, "Annee": 2022,
                    "Chiffre_Affaires_kDH": float(row[1]) if pd.notna(row[1]) else 0,
                    "Production_kDH": float(row[2]) if pd.notna(row[2]) else 0,
                    "Valeur_Ajoutee_kDH": float(row[3]) if pd.notna(row[3]) else 0,
                    "Investissements_kDH": float(row[4]) if pd.notna(row[4]) else 0
                })
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 7. CONSTRUCTION — Autorisations par province (sheet 11) — 2020 data (seule année dispo)
# =============================================================================
def extract_construction():
    df = pd.read_excel(f"{SRC}/7__Construction_et_Foncier_AS_2024.xlsx", sheet_name="11", header=None)
    data = []
    current_region = None
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower():
            continue
        r = get_region(cell)
        if r and pd.isna(row[1]):
            current_region = r
            continue
        if current_region and pd.notna(row[1]):
            try:
                # col1=Nb pièces, col2=Nb logements, col3=Valeur prévue kDH, col4=Surface bâtie, col5=Surface planchers, col6=Nb autorisations
                nb_auth = float(row[6]) if pd.notna(row[6]) else None
                nb_log = float(row[2]) if pd.notna(row[2]) else None
                val = float(str(row[3]).replace(',','')) if pd.notna(row[3]) else None
                surf = float(row[5]) if pd.notna(row[5]) else None
                data.append({
                    "Region": current_region, "Province_Prefecture": cell, "Annee": 2020,
                    "Nb_Autorisations": nb_auth, "Nb_Logements": nb_log,
                    "Valeur_Prevue_kDH": val, "Surface_Planchers_m2": surf
                })
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# 8. TRANSPORT — Routes par région au 31/12/2023 (sheet '1-2')
# =============================================================================
def extract_transport():
    df = pd.read_excel(f"{SRC}/8__Transport_AS_2024.xlsx", sheet_name="1-2", header=None)
    data = []
    # Routes régionales 2023 (rows 11-24)
    for i in range(11, 25):
        row = df.iloc[i]
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        r = get_region(cell)
        if r and "total" not in cell.lower():
            try:
                data.append({
                    "Region": r, "Annee": 2023,
                    "Routes_Provinciales_Total_km": float(row[2]) if pd.notna(row[2]) else 0,
                    "Routes_Provinciales_Revetues_km": float(row[1]) if pd.notna(row[1]) else 0,
                    "Routes_Regionales_Total_km": float(row[4]) if pd.notna(row[4]) else 0,
                    "Routes_Nationales_Total_km": float(row[6]) if pd.notna(row[6]) else 0,
                })
            except: pass
    # Réseau total national 2022 and 2023
    total_data = []
    for i in range(34, 42):
        row = df.iloc[i]
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if pd.notna(row[1]) and pd.notna(row[2]) and cell and cell != "nan":
            try:
                total_data.append({
                    "Type_Route": cell,
                    "2023": float(str(row[1]).replace('*','').strip()),
                    "2022": float(row[2])
                })
            except: pass
    return pd.DataFrame(data), pd.DataFrame(total_data)

# =============================================================================
# 9. TÉLÉCOMMUNICATIONS — Indicateurs nationaux 2022-2023 (sheet '7')
# =============================================================================
def extract_telecomm():
    df = pd.read_excel(f"{SRC}/9__Post-télécomm_AS_2024.xlsx", sheet_name="7", header=None)
    data = []
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan":
            continue
        try:
            v23_raw = str(row[1]).strip()
            v22_raw = str(row[2]).strip() if pd.notna(row[2]) else ""
            v23 = float(v23_raw.replace(',','')) if v23_raw not in ['-','nan','NaN',''] else None
            v22 = float(v22_raw.replace(',','').replace('R','').replace('م','').strip()) if v22_raw not in ['-','nan','NaN',''] else None
            if v23 is not None:
                data.append({"Indicateur": cell, "Annee": 2023, "Valeur": v23})
            if v22 is not None:
                data.append({"Indicateur": cell, "Annee": 2022, "Valeur": v22})
        except: pass
    return pd.DataFrame(data).dropna(subset=["Valeur"])

# =============================================================================
# 10. ENVIRONNEMENT — Ressources en eau 2022-2023 (sheet 'ENV 9-10')
# =============================================================================
def extract_env_eau():
    df = pd.read_excel(f"{SRC}/23__Environnement_AS_2024.xlsx", sheet_name="ENV 9-10", header=None)
    bilan = []
    bassins = []
    in_bassins = False
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if "bassin" in cell.lower() and "versant" in cell.lower():
            in_bassins = True
        if not in_bassins:
            # Bilan hydrique (rows: Précipitation, Evapotranspiration, etc.)
            if cell and cell != "nan" and pd.notna(row[3]):
                try:
                    v2223 = float(str(row[3]).strip())
                    bilan.append({"Indicateur": cell, "Annee_Hydro": "2022-2023", "Valeur_Mm3": v2223})
                except: pass
        else:
            if cell and cell not in ["nan","Total","Bassin versant","Millions de m3/ an"]:
                try:
                    apport = float(row[1]) if pd.notna(row[1]) else None
                    sup = float(row[3]) if pd.notna(row[3]) else None
                    if apport:
                        bassins.append({
                            "Bassin_Versant": cell, "Annee_Hydro": "2022-2023",
                            "Apport_Surface_Mm3": apport, "Superficie_km2": sup
                        })
                except: pass
    return pd.DataFrame(bilan), pd.DataFrame(bassins)

# =============================================================================
# 11. ENVIRONNEMENT — Plages par région (sheet 'ENV32-33-34')
# =============================================================================
def extract_env_plages():
    df = pd.read_excel(f"{SRC}/23__Environnement_AS_2024.xlsx", sheet_name="ENV32-33-34", header=None)
    data = []
    for i in range(5, 18):
        row = df.iloc[i]
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "total" in cell.lower() or "région" in cell.lower():
            continue
        try:
            v23 = int(float(row[3])) if pd.notna(row[3]) else None
            v22 = int(float(row[4])) if pd.notna(row[4]) else None
            if v23 is not None:
                data.append({"Region": cell, "Annee": 2023, "Nb_Plages": v23})
            if v22 is not None:
                data.append({"Region": cell, "Annee": 2022, "Nb_Plages": v22})
        except: pass
    return pd.DataFrame(data)

# =============================================================================
# RUN ALL
# =============================================================================
print("🚀 Extraction des données régionales 2022-2023\n")

df = extract_population()
df.to_csv(f"{OUT}/01_population_par_region.csv", index=False, encoding="utf-8-sig")
print(f"✅ [1] Population par région: {len(df)} lignes")

df = extract_ventes_elec()
df.to_csv(f"{OUT}/02_energie_ventes_electricite_par_province.csv", index=False, encoding="utf-8-sig")
print(f"✅ [2] Ventes électricité par province: {len(df)} lignes")

df = extract_prod_eau()
df.to_csv(f"{OUT}/03a_eau_production_superficielle.csv", index=False, encoding="utf-8-sig")
print(f"✅ [3a] Production eau superficielle par centre: {len(df)} lignes")

df = extract_onee_eau()
df.to_csv(f"{OUT}/03b_eau_onee_par_province_2023.csv", index=False, encoding="utf-8-sig")
print(f"✅ [3b] ONEE eau par province (2023): {len(df)} lignes")

df = extract_pib()
df.to_csv(f"{OUT}/04_pib_regional_par_secteur.csv", index=False, encoding="utf-8-sig")
print(f"✅ [4] PIB régional par secteur (2021-2022): {len(df)} lignes")

df = extract_industrie()
df.to_csv(f"{OUT}/05_industrie_par_region_2022.csv", index=False, encoding="utf-8-sig")
print(f"✅ [5] Industrie par région (2022): {len(df)} lignes")

df_reg, df_tot = extract_transport()
df_reg.to_csv(f"{OUT}/07_transport_routes_par_region_2023.csv", index=False, encoding="utf-8-sig")
df_tot.to_csv(f"{OUT}/07b_transport_reseau_total.csv", index=False, encoding="utf-8-sig")
print(f"✅ [7] Transport routes par région (2023): {len(df_reg)} lignes")
print(f"✅ [7b] Réseau routier total: {len(df_tot)} lignes")

df = extract_telecomm()
df.to_csv(f"{OUT}/08_telecomm_indicateurs_nationaux.csv", index=False, encoding="utf-8-sig")
print(f"✅ [8] Télécommunications indicateurs nationaux: {len(df)} lignes")

b1, b2 = extract_env_eau()
b1.to_csv(f"{OUT}/09a_env_ressources_eau_bilan.csv", index=False, encoding="utf-8-sig")
b2.to_csv(f"{OUT}/09b_env_ressources_eau_par_bassin.csv", index=False, encoding="utf-8-sig")
print(f"✅ [9a] Bilan eau: {len(b1)} lignes")
print(f"✅ [9b] Eau par bassin versant: {len(b2)} lignes")

df = extract_env_plages()
df.to_csv(f"{OUT}/10_env_plages_par_region.csv", index=False, encoding="utf-8-sig")
print(f"✅ [10] Plages par région: {len(df)} lignes")

# Construction note
df_c = extract_construction()
df_c.to_csv(f"{OUT}/06_construction_autorisations_par_province_2020.csv", index=False, encoding="utf-8-sig")
print(f"✅ [6] Construction autorisations par province (2020 - seule année régionale dispo): {len(df_c)} lignes")

print(f"\n📁 Fichiers CSV générés dans: {OUT}")
print(f"📊 Total fichiers: {len(os.listdir(OUT))}")

# =============================================================================
# FIX: ONEE EAU — region has data in col1 (it's the subtotal row)
# =============================================================================
def extract_onee_eau_v2():
    df = pd.read_excel(f"{SRC}/5__Energie_et_Eau_AS_2024.xlsx", sheet_name="20-20suite", header=None)
    data = []
    current_region = None
    region_keywords = ["tanger","oriental","fès","meknès","rabat","béni","casablanca",
                       "marrakech","drâa","souss","guelmim","laâyoune","dakhla"]
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower() or "compris" in cell.lower():
            continue
        r = get_region(cell)
        if r:
            current_region = r  # also extract region total
        if current_region and pd.notna(row[1]):
            try:
                nb = float(str(row[1]).replace(' ','').replace('-','0').replace('…','0'))
                va = float(str(row[2]).strip()) if pd.notna(row[2]) and str(row[2]).strip() not in ['-','nan','…',''] else 0.0
                vr = float(str(row[3]).strip()) if pd.notna(row[3]) and str(row[3]).strip() not in ['-','nan','…',''] else 0.0
                pr = float(str(row[4]).strip()) if pd.notna(row[4]) and str(row[4]).strip() not in ['-','nan','…',''] else 0.0
                if cell not in ["Ensemble","المجموع"] and (pr > 0 or nb > 0):
                    data.append({
                        "Region": current_region, "Province_Prefecture": cell, "Annee": 2023,
                        "Nb_Abonnes": nb, "Ventes_Abonnes_m3k": va,
                        "Ventes_Regies_m3k": vr, "Production_Eau_m3k": pr
                    })
            except: pass
    return pd.DataFrame(data)

# =============================================================================
# FIX: CONSTRUCTION — Province with numeric values, no separate region header
# =============================================================================
def extract_construction_v2():
    df = pd.read_excel(f"{SRC}/7__Construction_et_Foncier_AS_2024.xlsx", sheet_name="11", header=None)
    data = []
    current_region = None
    for _, row in df.iterrows():
        cell = str(row[0]).strip() if pd.notna(row[0]) else ""
        if not cell or cell == "nan" or "source" in cell.lower():
            continue
        if "année" in cell.lower():
            continue
        r = get_region(cell)
        if r:
            current_region = r  # region row also has totals
        if current_region and pd.notna(row[1]):
            try:
                nb_pieces = float(row[1]) if pd.notna(row[1]) else 0
                nb_log = float(row[2]) if pd.notna(row[2]) and str(row[2]).strip() != '-' else 0
                val_prev = float(str(row[3]).replace(',','')) if pd.notna(row[3]) else 0
                surf_bat = float(row[4]) if pd.notna(row[4]) else 0
                surf_plan = float(row[5]) if pd.notna(row[5]) else 0
                nb_auth = float(row[6]) if pd.notna(row[6]) else 0
                if nb_auth > 0 or nb_log > 0:
                    data.append({
                        "Region": current_region, "Province_Prefecture": cell, "Annee": 2020,
                        "Nb_Autorisations": nb_auth, "Nb_Logements": nb_log,
                        "Nb_Pieces": nb_pieces, "Valeur_Prevue_kDH": val_prev,
                        "Surface_Batie_m2": surf_bat, "Surface_Planchers_m2": surf_plan
                    })
            except: pass
    return pd.DataFrame(data)

print("\n=== Corrections ===")
df = extract_onee_eau_v2()
df.to_csv(f"{OUT}/03b_eau_onee_par_province_2023.csv", index=False, encoding="utf-8-sig")
print(f"✅ [3b FIX] ONEE eau: {len(df)} lignes")

df = extract_construction_v2()
df.to_csv(f"{OUT}/06_construction_autorisations_par_province_2020.csv", index=False, encoding="utf-8-sig")
print(f"✅ [6 FIX] Construction: {len(df)} lignes")
