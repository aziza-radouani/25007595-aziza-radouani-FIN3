"""
F3 — Prévision de l'inflation à 12 mois
Script Python extrait du notebook projet_F3_corrige.ipynb.
Données : États-Unis, source FRED.
"""

import warnings
warnings.filterwarnings("ignore")

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from pandas_datareader import data as pdr
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import Ridge
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score

SEED = 42
pd.set_option("display.max_columns", 30)
plt.rcParams["figure.figsize"] = (10, 5)

# 1. Télécharger les séries mensuelles depuis FRED
cpi = pdr.DataReader("CPIAUCSL", "fred", start="1947-01-01")
chomage = pdr.DataReader("UNRATE", "fred", start="1948-01-01")
taux = pdr.DataReader("FEDFUNDS", "fred", start="1954-07-01")

df = pd.concat([cpi, chomage, taux], axis=1)
df.columns = ["cpi", "chomage", "taux_directeur"]
df = df.sort_index()

# Inflation annuelle : variation du CPI sur 12 mois, en pourcentage
df["inflation"] = df["cpi"].pct_change(periods=12) * 100
df = df.dropna().copy()

print("Nombre d'observations :", len(df))
print("Première date :", df.index.min().strftime("%Y-%m"))
print("Dernière date :", df.index.max().strftime("%Y-%m"))
print("\nStatistiques descriptives :")
print(df.describe().round(2))
print("\nNombre de lignes dupliquées :", df.index.duplicated().sum())
print("\nValeurs manquantes :")
print(df.isna().sum())

# 2. Analyse exploratoire et graphiques
plt.figure()
plt.plot(df.index, df["inflation"], label="Inflation annuelle")
plt.axhline(2, linestyle="--", label="Repère de 2 %")
plt.title("Inflation annuelle aux États-Unis")
plt.xlabel("Date")
plt.ylabel("Inflation (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("inflation_annuelle.png", dpi=150)
plt.show()

fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
ax[0].plot(df.index, df["chomage"])
ax[0].set_title("Taux de chômage aux États-Unis")
ax[0].set_ylabel("Chômage (%)")
ax[0].grid(alpha=0.3)
ax[1].plot(df.index, df["taux_directeur"])
ax[1].set_title("Taux effectif des fonds fédéraux")
ax[1].set_ylabel("Taux (%)")
ax[1].set_xlabel("Date")
ax[1].grid(alpha=0.3)
plt.tight_layout()
plt.savefig("chomage_taux_directeur.png", dpi=150)
plt.show()

correlations = df[["inflation", "chomage", "taux_directeur"]].corr()
print("\nMatrice de corrélation :")
print(correlations.round(2))

plt.figure(figsize=(7, 5))
plt.imshow(correlations, vmin=-1, vmax=1, cmap="coolwarm")
plt.colorbar(label="Corrélation")
plt.xticks(range(len(correlations.columns)), correlations.columns, rotation=25)
plt.yticks(range(len(correlations.index)), correlations.index)
for i in range(len(correlations.index)):
    for j in range(len(correlations.columns)):
        plt.text(j, i, f"{correlations.iloc[i, j]:.2f}", ha="center", va="center")
plt.title("Matrice de corrélation")
plt.tight_layout()
plt.savefig("matrice_correlation.png", dpi=150)
plt.show()

# 3. Préparer les variables explicatives et la cible à t+12
model_data = pd.DataFrame(index=df.index)
model_data["inflation_t"] = df["inflation"]
model_data["inflation_lag1"] = df["inflation"].shift(1)
model_data["inflation_lag3"] = df["inflation"].shift(3)
model_data["inflation_lag6"] = df["inflation"].shift(6)
model_data["inflation_lag12"] = df["inflation"].shift(12)
model_data["chomage_lag1"] = df["chomage"].shift(1)
model_data["taux_directeur_lag1"] = df["taux_directeur"].shift(1)
model_data["cible_inflation_t_plus_12"] = df["inflation"].shift(-12)
model_data["date_cible"] = model_data.index + pd.DateOffset(months=12)
model_data = model_data.dropna().copy()

features = [
    "inflation_t",
    "inflation_lag1",
    "inflation_lag3",
    "inflation_lag6",
    "inflation_lag12",
    "chomage_lag1",
    "taux_directeur_lag1",
]
X = model_data[features]
y = model_data["cible_inflation_t_plus_12"]

print("\nDimensions de X :", X.shape)
print("Nombre de valeurs de y :", len(y))

# 4. Séparation chronologique entraînement/test avec purge de 12 mois
split_position = int(len(model_data) * 0.80)
date_debut_test = model_data.index[split_position]
train_mask = model_data["date_cible"] < date_debut_test
test_mask = model_data.index >= date_debut_test

X_train = X.loc[train_mask]
y_train = y.loc[train_mask]
X_test = X.loc[test_mask]
y_test = y.loc[test_mask]

print("Début du test :", date_debut_test.strftime("%Y-%m"))
print("Observations d'entraînement :", len(X_train))
print("Observations de test :", len(X_test))

if len(X_train) == 0 or len(X_test) == 0:
    raise ValueError("Pas assez de données pour effectuer la séparation entraînement/test.")

# 5. Modèle Ridge
model = Pipeline(steps=[
    ("scaler", StandardScaler()),
    ("ridge", Ridge(alpha=1.0))
])
model.fit(X_train, y_train)
y_pred = model.predict(X_test)
print("\nModèle Ridge entraîné avec succès.")

# 6. Modèle de référence : inflation connue à la date t
y_baseline = model_data.loc[X_test.index, "inflation_t"]
assert y_test.index.equals(y_baseline.index)

# 7. Évaluation
def calculer_metriques(y_reel, y_estime):
    return {
        "MAE": mean_absolute_error(y_reel, y_estime),
        "RMSE": np.sqrt(mean_squared_error(y_reel, y_estime)),
        "R2": r2_score(y_reel, y_estime),
    }

metriques_ridge = calculer_metriques(y_test, y_pred)
metriques_baseline = calculer_metriques(y_test, y_baseline)
comparaison = pd.DataFrame(
    [metriques_baseline, metriques_ridge],
    index=["Baseline", "Ridge"]
)
print("\nComparaison des modèles :")
print(comparaison.round(4))

reduction_rmse = (1 - metriques_ridge["RMSE"] / metriques_baseline["RMSE"]) * 100
print(f"Réduction du RMSE : {reduction_rmse:.2f} %")

# 8. Graphiques des prévisions
plt.figure(figsize=(12, 5))
plt.plot(y_test.index, y_test.values, label="Inflation réelle à t+12", linewidth=2)
plt.plot(y_test.index, y_pred, label="Prévision Ridge", alpha=0.85)
plt.plot(y_test.index, y_baseline.values, label="Prévision baseline", alpha=0.8)
plt.title("Inflation réelle et prévisions à 12 mois — période de test")
plt.xlabel("Date de prévision (t)")
plt.ylabel("Inflation annuelle à t+12 (%)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("comparaison_previsions.png", dpi=150)
plt.show()

plt.figure(figsize=(6, 6))
plt.scatter(y_test, y_pred, alpha=0.6)
limites = [
    min(float(y_test.min()), float(np.min(y_pred))),
    max(float(y_test.max()), float(np.max(y_pred))),
]
plt.plot(limites, limites, linestyle="--", label="Prévision parfaite")
plt.xlabel("Inflation réelle à t+12 (%)")
plt.ylabel("Inflation prévue par Ridge (%)")
plt.title("Valeurs réelles et prédites — Ridge")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("reel_vs_predit.png", dpi=150)
plt.show()

# 9. Coefficients du modèle Ridge
ridge_estimator = model.named_steps["ridge"]
coefficients = pd.DataFrame({
    "Variable": features,
    "Coefficient_standardise": ridge_estimator.coef_,
}).sort_values("Coefficient_standardise", key=lambda s: s.abs(), ascending=False)

print("\nCoefficients :")
print(coefficients.round(4))

plt.figure(figsize=(9, 5))
plt.barh(coefficients["Variable"], coefficients["Coefficient_standardise"])
plt.axvline(0, linewidth=0.8)
plt.title("Coefficients du modèle Ridge")
plt.xlabel("Coefficient (variables standardisées)")
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig("coefficients_ridge.png", dpi=150)
plt.show()

# 10. Exporter les résultats
resultats = pd.DataFrame(index=y_test.index)
resultats.index.name = "date_prevision"
resultats["date_cible"] = model_data.loc[y_test.index, "date_cible"]
resultats["inflation_reelle_t_plus_12"] = y_test
resultats["prevision_ridge"] = y_pred
resultats["prevision_baseline"] = y_baseline
resultats.to_csv("resultats_inflation_12_mois.csv", index=True)

# Exporter également le dataset utilisé
df.to_csv("dataset_fred_inflation.csv", index=True)

print("\nFichiers créés :")
print("- resultats_inflation_12_mois.csv")
print("- dataset_fred_inflation.csv")
print("- inflation_annuelle.png")
print("- chomage_taux_directeur.png")
print("- matrice_correlation.png")
print("- comparaison_previsions.png")
print("- reel_vs_predit.png")
print("- coefficients_ridge.png")

# 11. Conclusion chiffrée
print("\nCONCLUSION DES RÉSULTATS")
print("------------------------")
print(f"RMSE baseline : {metriques_baseline['RMSE']:.3f}")
print(f"RMSE Ridge    : {metriques_ridge['RMSE']:.3f}")
print(f"MAE baseline  : {metriques_baseline['MAE']:.3f}")
print(f"MAE Ridge     : {metriques_ridge['MAE']:.3f}")
print(f"R² Ridge      : {metriques_ridge['R2']:.3f}")
print(f"Évolution du RMSE : {reduction_rmse:.2f} % par rapport au baseline")

if reduction_rmse >= 10:
    print("Ridge atteint l'objectif d'une réduction du RMSE d'au moins 10 %.")
elif reduction_rmse > 0:
    print("Ridge améliore le baseline, mais n'atteint pas la réduction de 10 %.")
else:
    print("Ridge ne surpasse pas le baseline sur le RMSE.")

print("\nLimites à rappeler :")
print("- Les données concernent les États-Unis et non le Maroc.")
print("- Les résultats dépendent de la période de test choisie.")
print("- Les relations statistiques ne démontrent pas une causalité.")
print("- Les séries macroéconomiques peuvent être révisées et publiées avec retard.")
