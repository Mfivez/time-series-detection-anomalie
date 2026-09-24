# Time Series et détection d'anomalies pour l'IoT
Le cours suit un même fil rouge : les mesures d'une installation HVAC passent du CSV brut au nettoyage, à la prévision, à la détection d'anomalies puis à une première approche par autoencoder.

Le parcours commence par `jour_01/00_introduction_au_parcours.ipynb`, qui présente la mission, la progression des trois jours et le rôle de chaque méthode avant toute manipulation du CSV brut.

## Installation

Le cours est validé avec **Python 3.12**. Ne pas créer l'environnement avec Python 3.14 : TensorFlow 2.20 ne fournit pas de paquet compatible pour cette version. TensorFlow est une dépendance assez volumineuse ; prévoir quelques minutes pour la première installation.

### Installation automatique sous Windows — recommandée

Double-cliquer sur **`INSTALLER_WINDOWS.cmd`** à la racine du cours. Il supprime l'ancien `.venv`, le recrée avec Python 3.12, installe `requirements.txt` puis vérifie les notebooks. L'installation peut prendre plusieurs minutes, particulièrement lors du téléchargement de TensorFlow.

### Linux, macOS ou WSL

```bash
python3.12 -m venv .venv
source .venv/bin/activate
python scripts/check_python.py
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m jupyter lab
```

### Windows PowerShell

```powershell
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python .\scripts\check_python.py
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python -m jupyter lab
```

La commande `py -3.12` est importante : `py` sans version sélectionne le Python par défaut, qui peut être Python 3.14.

### Si un environnement a été créé avec Python 3.14

Dans PowerShell, supprimer uniquement cet environnement incomplet puis le recréer :

```powershell
deactivate
Remove-Item -Recurse -Force .venv
py -0p
py -3.12 --version
py -3.12 -m venv .venv
.venv\Scripts\Activate.ps1
python .\scripts\check_python.py
python -m pip install --upgrade pip
python -m pip install -r .\requirements.txt
```

Si `py -3.12` n'est pas reconnu, installer d'abord Python 3.12 depuis python.org ou avec `winget install -e --id Python.Python.3.12`, puis rouvrir PowerShell.

Ouvrir ensuite les notebooks dans l'ordre numérique. Chaque notebook retrouve automatiquement la racine du projet : Jupyter peut donc être démarré depuis la racine ou depuis un dossier de journée.

## Utilisation pédagogique

1. Distribuer `datasets/` et le dossier du jour.
2. Alterner démonstrations courtes et cellules **À vous de jouer**.
3. Ne remettre le notebook `_corrige.ipynb` correspondant qu'après l'exercice.
4. Faire noter les observations en français avant de commenter le code.

Les cellules d'exercice sont volontairement valides même lorsqu'elles ne contiennent encore que `pass`. Ainsi, un participant peut exécuter tout le notebook, revenir sur un exercice et ne bloque pas les démonstrations suivantes.

## Données

Les données sont entièrement synthétiques et reproductibles. Elles représentent six semaines de mesures toutes les quinze minutes : température, humidité, puissance électrique, pression et vibration.

- `datasets/raw/iot_hvac_raw.csv` : données désordonnées avec trous, doublons et valeurs manquantes ;
- `datasets/prepared/iot_hvac_clean.csv` : série régulière et complète ;
- `datasets/prepared/iot_hvac_labeled.csv` : même série avec vérité terrain pour les anomalies.

Le fichier [datasets/README.md](datasets/README.md) contient le dictionnaire des variables.

## Vérification technique

Après l'installation, exécuter tous les notebooks dans un noyau neuf :

```bash
python scripts/verify_notebooks.py
```

Pour vérifier seulement une journée :

```bash
python scripts/verify_notebooks.py jour_01
```

La vérification exécute aussi les corrigés correspondants et s'arrête avec un code d'erreur si une cellule échoue.
