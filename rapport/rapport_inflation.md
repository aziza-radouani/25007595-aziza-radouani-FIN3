# Rapport du projet — Prévision de l'inflation

## 1. Introduction

L'inflation représente une augmentation générale et durable des prix des biens et services. Elle influence le pouvoir d'achat des ménages et les décisions économiques.

Ce projet a pour objectif d'étudier l'évolution de l'inflation et d'utiliser un modèle de Machine Learning pour prévoir son niveau douze mois à l'avance.

## 2. Source des données

Les données utilisées proviennent de la base FRED (Federal Reserve Economic Data), aux États-Unis.

Les variables étudiées sont :
- CPIAUCSL : indice des prix à la consommation.
- UNRATE : taux de chômage.
- FEDFUNDS : taux directeur effectif des fonds fédéraux.

**Remarque :** cette étude concerne les États-Unis et non le Maroc.

## 3. Méthodologie

Les principales étapes du projet sont :

1. Collecte des données économiques.
2. Nettoyage et préparation des données.
3. Calcul du taux d'inflation.
4. Création des variables explicatives et des décalages temporels.
5. Définition de la cible : inflation douze mois à l'avance.
6. Séparation chronologique des données en ensembles d'entraînement et de test.
7. Entraînement du modèle Ridge.
8. Comparaison avec une prévision de référence (baseline).

## 4. Évaluation du modèle

Les performances sont évaluées à l'aide de trois indicateurs :

- MAE : erreur absolue moyenne.
- RMSE : racine de l'erreur quadratique moyenne.
- R² : coefficient de détermination.

Les résultats numériques sont disponibles dans le notebook et dans le fichier CSV exporté.

## 5. Conclusion

Ce projet permet d'étudier l'utilisation du Machine Learning pour la prévision de l'inflation à douze mois.

La comparaison entre le modèle Ridge et la baseline permet d'évaluer l'intérêt du modèle prédictif.

Les résultats doivent être interprétés en tenant compte des limites des données et du fait que l'étude porte sur l'économie américaine.
