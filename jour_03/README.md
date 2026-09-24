# Jour 3 — Anomalies, maintenance prédictive et autoencoder

## Objectifs de la journée

À 17 h, les participants savent construire des règles statistiques, utiliser Isolation Forest, comprendre le principe d'un autoencoder et replacer les alertes dans une architecture IoT exploitable.

## Déroulé indicatif

| Horaire | Contenu | Support |
|---|---|---|
| 09:00–09:20 | Types d'anomalies et coût des erreurs | Discussion |
| 09:20–10:30 | Seuils métier et Z-score mobile | `01_anomalies_statistiques.ipynb` |
| 10:30–10:45 | Pause | |
| 10:45–12:00 | Isolation Forest et alertes de maintenance | `02_isolation_forest_et_maintenance.ipynb` |
| 12:00–13:00 | Pause déjeuner | |
| 13:00–13:45 | Neurone, couche Dense, loss et entraînement | Début du notebook 03 |
| 13:45–14:45 | Autoencoder et erreur de reconstruction | `03_introduction_autoencoder.ipynb` |
| 14:45–15:00 | Pause | |
| 15:00–16:20 | Projet final : comparer les détecteurs | `04_projet_final_comparaison.ipynb` |
| 16:20–17:00 | Architecture IoT, exploitation et bilan | Discussion finale |

## Messages essentiels

- Commencer par la règle la plus simple qui répond au besoin.
- Entraîner un détecteur non supervisé sur un comportement aussi normal que possible.
- Le seuil encode un compromis opérationnel.
- Un modèle n'est utile que si son alerte arrive à la bonne personne avec du contexte.

## Illustrations statiques

Les notebooks utilisent 12 images stockées dans `assets/jour_03`. Elles illustrent les formes d'anomalies, les seuils, Isolation Forest, le fonctionnement d'un autoencoder et le passage du score à une intervention de maintenance.

Les 11 schémas et graphiques reproductibles peuvent être reconstruits depuis la racine du projet avec :

```powershell
.venv\Scripts\python.exe scripts\build_course_illustrations.py
```

L'illustration d'ouverture `00_detection_maintenance_hvac.png` est un visuel pédagogique fixe et n'est pas remplacée par ce script.
