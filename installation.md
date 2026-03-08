# Installation

## Prérequis

- Python 3.11+
- Git

## Mise en place

### 1. Cloner le dépôt

```bash
git clone <url-du-repo>
cd Analyse-de-produits-derives
```

### 2. Créer et activer l'environnement virtuel

```bash
python -m venv .venv
```

**Windows (PowerShell) :**
```powershell
.venv\Scripts\Activate.ps1
```

**macOS / Linux :**
```bash
source .venv/bin/activate
```

### 3. Installer les dépendances

```bash
pip install -r requirements.txt
```

## Dépendances

| Package | Rôle |
|---|---|
| `matplotlib` | Visualisation (graphiques statiques, pylab) |
| `numpy` | Calcul numérique et tableaux |
| `pandas` | Manipulation de données tabulaires |
| `tabulate` | Affichage de tableaux formatés en console |

## Lancer les fichiers

> **Important :** Toujours exécuter les fichiers depuis la racine du projet
> `Analyse-de-produits-derives/` pour que le package `dx` soit trouvé.

```powershell
# Depuis la racine du projet
python "Module 1 - Simulation de modèles financiers/3_Mouvement_brownien_geometrique.py"
```

## Structure du projet

| Dossier | Contenu |
|---|---|
| `dx/` | Package principal (classes de base réutilisables) |
| `Module 0/` | Infrastructure d'évaluation |
| `Module 1/` | Simulation de modèles financiers |
| `Module 2/` | Evaluation de produits dérivés |
| `Module 3/` | Evaluation de portefeuille |
| `Module 4/` | Evaluation basée marché |
