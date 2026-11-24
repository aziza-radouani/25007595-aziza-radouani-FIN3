
# F3 — Prévision de l'inflation

## 1. Présentation du projet
Ce projet porte sur la prévision de l'inflation à partir de données économiques.

L'objectif est de construire un modèle capable de prévoir le taux d'inflation à 12 mois à l'aide de variables économiques.

## 2. Problématique
Dans quelle mesure les données historiques de l'inflation, le taux de chômage et le taux directeur permettent-ils de prévoir l'inflation à 12 mois ?

## 3. Données utilisées
Les données proviennent de la base FRED (Federal Reserve Economic Data).

Variables utilisées :
- CPIAUCSL : indice des prix à la consommation.
- UNRATE : taux de chômage.
- FEDFUNDS : taux effectif des fonds fédéraux.

Les données concernent les États-Unis.

## 4. Méthodologie
- Collecte et préparation des données.
- Analyse exploratoire et visualisation.
- Construction de variables explicatives.
- Prévision de l'inflation à 12 mois.
- Utilisation du modèle Ridge Regression.
- Comparaison avec un modèle de référence.
- Évaluation avec MAE, RMSE et R².

## 5. Fichiers du projet
- projet_F3_corrige.ipynb : notebook contenant l'analyse et la modélisation.
- resultats_inflation_12_mois.csv : résultats exportés par le notebook.

## 6. Sources
- FRED : https://fred.stlouisfed.org/series/CPIAUCSL
- FRED : https://fred.stlouisfed.org/series/UNRATE
- FRED : https://fred.stlouisfed.org/series/FEDFUNDS

## 7. Outils utilisés
- Python
- Google Colab
- Pandas
- Matplotlib
- Scikit-learn
- Pandas Datareader
