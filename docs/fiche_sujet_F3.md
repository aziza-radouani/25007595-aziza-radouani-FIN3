# F3. Prévision de l'inflation
- Question : le chômage et le taux directeur aident-ils à prévoir l'inflation d'un an sur l'autre ?
- Tâche : régression sur séries mensuelles.
- Données : FRED CPIAUCSL, UNRATE et FEDFUNDS.
- Modèles : dernière valeur (référence), Ridge, gradient boosting.
- Métriques : RMSE sur un horizon de 12 mois.
- Risque : révisions des séries (biais d'anticipation).
