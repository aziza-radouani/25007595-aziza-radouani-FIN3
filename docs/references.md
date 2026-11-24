
# Références et sources des données

## Source principale : FRED

Les données économiques utilisées dans ce projet proviennent de la base Federal Reserve Economic Data (FRED).

### 1. Indice des prix à la consommation (CPI)
- Code : CPIAUCSL
- Description : Consumer Price Index for All Urban Consumers.
- Source : https://fred.stlouisfed.org/series/CPIAUCSL

### 2. Taux de chômage
- Code : UNRATE
- Description : Civilian Unemployment Rate.
- Source : https://fred.stlouisfed.org/series/UNRATE

### 3. Taux des fonds fédéraux
- Code : FEDFUNDS
- Description : Effective Federal Funds Rate.
- Source : https://fred.stlouisfed.org/series/FEDFUNDS

## Utilisation des données

Les séries sont téléchargées à l'aide de Python et de la bibliothèque pandas-datareader.

Les données concernent les États-Unis et sont utilisées pour analyser et prévoir l'inflation à un horizon de 12 mois.

## Bibliographie

- Federal Reserve Bank of St. Louis — FRED.
- Documentation pandas-datareader : https://pandas-datareader.readthedocs.io/
- Documentation Scikit-learn : https://scikit-learn.org/
