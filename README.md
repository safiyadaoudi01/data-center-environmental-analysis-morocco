# Water & Energy Sustainability Assessment for Data Center Development in Morocco (2024)

## 📌 Description
Ce projet évalue la capacité des régions marocaines à accueillir des Data Centers de manière durable, en tenant compte de la disponibilité en eau, de la capacité énergétique et du contexte économique régional.

L’étude repose uniquement sur des données publiques :
- Water Efficiency Dataset
- Annuaire Statistique du Maroc 2024 (HCP)

Le résultat principal est un indice composite :
**Data Center Suitability Index (DCSI)**, utilisé pour comparer les régions.


## 🎯 Objectifs
- Analyser la pression hydrique par région
- Évaluer la capacité énergétique régionale
- Intégrer des indicateurs économiques et démographiques
- Construire un indice comparatif (DCSI)
- Identifier les régions favorables et les régions à risque


## 🧩 Méthodologie (vue d’ensemble)
1. Préparation des données
   - Harmonisation des noms de régions
   - Sélection des régions communes
   - Nettoyage et normalisation

2. Construction des indicateurs
   - Indice hydrique
   - Indice énergétique
   - Indice économique

3. Modélisation
   - Calcul du DCSI
   - Classement des régions
   - Analyse de sensibilité

4. Restitution
   - Tableaux comparatifs
   - Cartographie régionale
   - Recommandations


## 📊 Sources de données
### Annuaire Statistique du Maroc 2024 (HCP)
Fichiers utilisés :
- Division administrative
- Énergie et Eau
- Population
- Environnement
- Industrie
- Comptes de la Nation

### Water Efficiency Dataset
- Stress hydrique
- Disponibilité en eau
- Indicateurs d’efficacité hydrique



## 🗂 Structure du projet

```
├── data_raw/       # Données brutes
├── data_processed/ # Données nettoyées et fusionnées
├── notebooks/      # Analyses exploratoires et modélisation
├── powerbi/        # Tableaux de bord Power BI
├── scripts/        # Fonctions et scripts
├── slides/         # Présentation du projet
├── README.md
└── requirements.txt # Librairies Python nécessaires
```


## 🧮 Indice DCSI (principe)
Le Data Center Suitability Index combine :
- un sous-indice hydrique,
- un sous-indice énergétique,
- un sous-indice économique,
- une pénalisation par le stress hydrique.

Les indicateurs sont normalisés (Min-Max) puis agrégés avec des pondérations justifiées analytiquement.


## ⚠️ Limites
- Données agrégées par région
- Absence de données réelles de Data Centers
- Hypothèses sur un profil standard de consommation eau/énergie


## 🚀 Résultats attendus
- Classement des régions marocaines
- Identification des zones favorables
- Identification des zones à risque hydrique
- Support d’aide à la décision

