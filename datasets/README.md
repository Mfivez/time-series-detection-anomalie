# Jeu de données HVAC synthétique

Une ligne correspond à une mesure d'un équipement HVAC. La série de référence couvre 42 jours avec une fréquence de 15 minutes et des timestamps en UTC.

| Colonne | Unité | Description |
|---|---|---|
| `timestamp` | UTC | Date et heure de la mesure |
| `device_id` | — | Identifiant du capteur (`hvac_01`) |
| `temperature_c` | °C | Température mesurée |
| `humidity_pct` | % | Humidité relative |
| `power_kw` | kW | Puissance électrique consommée |
| `pressure_bar` | bar | Pression du circuit |
| `vibration_mm_s` | mm/s | Niveau de vibration |
| `is_anomaly` | 0/1 | Vérité terrain, uniquement dans le fichier labellisé |
| `anomaly_type` | texte | Type d'anomalie injectée, uniquement dans le fichier labellisé |

Les phénomènes normaux combinent rythme journalier, différence jours ouvrés/week-end, légère dérive et bruit de mesure. Les anomalies injectées comprennent des pics multivariés, une consommation nocturne inhabituelle et une dérive progressive de vibration.

Le fichier brut ne contient pas les labels. Il ajoute des défauts de qualité indépendants des anomalies métier : lignes manquantes, valeurs absentes, doublons et ordre mélangé.

