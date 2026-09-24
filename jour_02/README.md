# Jour 2 — Forecasting simple et erreur de prévision

## Objectifs de la journée

À 17 h, les participants savent établir une baseline, mesurer une erreur, entraîner Prophet, comparer les approches et transformer un résidu important en signal d'anomalie.

## Déroulé indicatif

| Horaire | Contenu | Support |
|---|---|---|
| 09:00–09:20 | Rappel du jour 1 et définition d'une prévision | Discussion |
| 09:20–10:30 | Baselines de persistance et saisonnière | `01_baselines_et_metriques.ipynb` |
| 10:30–10:45 | Pause | |
| 10:45–12:00 | MAE, RMSE et protocole d'évaluation | Fin du notebook 01 |
| 12:00–13:00 | Pause déjeuner | |
| 13:00–14:30 | Premier modèle Prophet | `02_prevoir_avec_prophet.ipynb` |
| 14:30–14:45 | Pause | |
| 14:45–15:45 | Résidus, seuils et premières alertes | `03_erreur_de_prevision_et_anomalies.ipynb` |
| 15:45–16:00 | Pause | |
| 16:00–16:45 | Challenge complet de forecasting | `04_mini_challenge_forecasting.ipynb` |
| 16:45–17:00 | Mise en commun et transition vers le jour 3 | Synthèse |

## Messages essentiels

- Un modèle doit battre une baseline pour justifier sa complexité.
- MAE et RMSE racontent des aspects différents des erreurs.
- Le test représente un futur réellement inconnu.
- Une grande erreur de prévision est un signal, pas encore un diagnostic de panne.

## Illustrations statiques

Les notebooks utilisent 11 images stockées dans `assets/jour_02`. Elles rendent visibles les baselines, les métriques, les composantes de Prophet, les résidus et le pipeline complet de forecasting, même sans réexécuter les cellules de démonstration.

Les 10 schémas et graphiques reproductibles peuvent être reconstruits depuis la racine du projet avec :

```powershell
.venv\Scripts\python.exe scripts\build_course_illustrations.py
```

L'illustration d'ouverture `00_prevision_hvac.png` est un visuel pédagogique fixe et n'est pas remplacée par ce script.
