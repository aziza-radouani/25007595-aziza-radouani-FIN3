# Projet Data Science — Prévision de l'inflation à 12 mois

## 1. Informations générales

- **Étudiante :** Aziza Radouani
- **Code Apogée :** 25007595
- **Groupe :** S7 FIN3
- **Matière :** Base de données & Data Science
- **Sujet :** Prévision de l'inflation à 12 mois

## 2. Présentation du projet

Ce projet consiste à étudier et prévoir l'évolution de l'inflation à partir de données macroéconomiques mensuelles des États-Unis.

L'objectif est de construire un modèle de Machine Learning capable de prévoir l'inflation à un horizon de 12 mois et de comparer ses performances à une méthode de référence (Baseline).

## 3. Problématique

Le chômage et le taux d'intérêt améliorent-ils la prévision de l'inflation à 12 mois ?

Le projet utilise une régression Ridge afin d'étudier les relations entre les indicateurs macroéconomiques et l'évolution future de l'inflation.

## 4. Données utilisées

Les données proviennent de la base FRED (Federal Reserve Bank of St. Louis).

| Variable | Description |
|---|---|
| CPIAUCSL | Indice des prix à la consommation |
| UNRATE | Taux de chômage |
| FEDFUNDS | Taux effectif des fonds fédéraux |

L'inflation annuelle est calculée à partir de la variation du CPI sur 12 mois.

Sources :
- https://fred.stlouisfed.org/series/CPIAUCSL
- https://fred.stlouisfed.org/series/UNRATE
- https://fred.stlouisfed.org/series/FEDFUNDS

Les données sont destinées à l'analyse de l'économie américaine. Elles ne représentent pas l'économie marocaine.

## 5. Méthodologie

Les principales étapes sont :

1
