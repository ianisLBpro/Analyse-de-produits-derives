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
| `numpy` | Calcul numérique |
| `pandas` | Manipulation de données |
| `matplotlib` | Visualisation statique |
| `plotly` | Visualisation interactive |
| `scipy` | Calcul scientifique |
| `statsmodels` | Modèles statistiques |
| `scikit-learn` | Machine learning |
| `torch` / `torchvision` | Deep learning |
| `numba` | Accélération numérique (JIT) |
| `Cython` | Extensions C |
| `tables` / `h5py` | Stockage HDF5 |
| `yfinance` | Données de marché |
| `openpyxl` / `xlrd` | Fichiers Excel |
| `ipykernel` / `ipywidgets` | Support Jupyter |

> Le fichier `requirements.txt` sera mis à jour au fur et à mesure de l'avancement du projet.
