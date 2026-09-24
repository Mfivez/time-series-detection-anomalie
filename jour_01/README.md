# Jour 1 — Comprendre et préparer une série temporelle

## Objectifs de la journée

À 17 h, les participants comprennent la chaîne complète du capteur à l'alerte, savent charger un CSV IoT, manipuler les timestamps, rendre une série régulière, visualiser ses motifs et créer un découpage temporel sans fuite de données.

## Déroulé indicatif

| Horaire | Contenu | Support |
|---|---|---|
| 09:00–09:45 | Mission HVAC, carte des trois jours et rôle des outils | `00_introduction_au_parcours.ipynb` |
| 09:45–10:30 | Première exploration d'un CSV de capteurs | `01_decouvrir_une_serie_temporelle.ipynb` |
| 10:30–10:45 | Pause | |
| 10:45–12:00 | Dates, tri, doublons et diagnostic | Fin du notebook 01 |
| 12:00–13:00 | Pause déjeuner | |
| 13:00–14:30 | Trous, fréquence, resampling et interpolation | `02_nettoyer_et_reechantillonner.ipynb` |
| 14:30–14:45 | Pause | |
| 14:45–16:00 | Tendance, saisonnalité, bruit et moyennes mobiles | `03_comprendre_le_signal.ipynb` |
| 16:00–16:15 | Pause | |
| 16:15–16:35 | Découpage train/test et fuite temporelle | Fin du notebook 03 |
| 16:35–17:00 | Mini-challenge et synthèse | `04_mini_challenge.ipynb` |

## Messages essentiels

- Toujours trier avant un calcul temporel.
- Rendre les trous visibles avant de décider de les remplir.
- Choisir l'agrégation selon le sens physique du signal.
- Le futur ne doit jamais influencer l'entraînement.

## Illustrations statiques

Les notebooks affichent quatorze illustrations PNG stockées dans `assets/jour_01/`. Elles restent visibles sans exécuter les cellules et servent de repères avant la manipulation des données.

Les treize schémas et graphiques reproductibles peuvent être reconstruits depuis la racine avec :

```powershell
.venv\Scripts\python.exe scripts\build_day1_illustrations.py
```
