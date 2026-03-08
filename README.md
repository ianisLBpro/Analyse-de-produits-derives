# Analyse de Produits Dérivés

Ce projet regroupe l'ensemble de mes travaux sur l'évaluation des produits dérivés financiers avec Python. Il couvre un large spectre de sujets allant de la construction de l'infrastructure d'évaluation risque-neutre jusqu'à la calibration de modèles sur données de marché, en passant par la simulation Monte Carlo et le pricing d'options européennes et américaines.

## Technologies utilisées

| Catégorie | Librairies |
|---|---|
| Calcul scientifique | `numpy`, `pandas` |
| Visualisation | `matplotlib` |
| Utilitaires | `tabulate` |

> **Python 3.14** — Voir le fichier [installation.md](installation.md) pour la mise en place de l'environnement virtuel.

---

## Structure du projet

### Module 0 — Infrastructure d'évaluation

Ce module pose les fondations théoriques et techniques de l'évaluation des produits dérivés : théorème fondamental, actualisation risque-neutre et construction de l'environnement de marché.

| Fichier | Statut | Description |
|---|---|---|
| `1_Theoreme_fondamental_d_evaluation_des_actifs.ipynb` | ✅ Disponible | Formalisation du cadre théorique d'absence d'arbitrage et existence de la mesure risque-neutre. |
| `2_Actualisation_risque_neutre.py` | ✅ Disponible | Représentation du temps en Python, fonction `get_year_deltas` et classe `constant_short_rate` pour l'actualisation à taux court constant. |
| `3_Environnement_de_marche.py` | ✅ Disponible | Classe `market_environment` regroupant en un seul objet tous les paramètres nécessaires à la simulation et à la valorisation d'un dérivé. |

---

### Module 1 — Simulation de modèles financiers

Ce module implémente les processus stochastiques nécessaires à la simulation Monte Carlo : génération de nombres aléatoires, mouvement brownien géométrique, diffusion par sauts et modèle CIR.

| Fichier | Statut | Description |
|---|---|---|
| `1_Generation_de_nombres_aleatoires.py` | ✅ Disponible | Fonction `sn_random_numbers()` générant des nombres pseudo-aléatoires en distribution normale standard, avec options de réduction de variance : variantes antithétiques et moment matching. |
| `2_Classe_de_simulation_generique.py` | ✅ Disponible | Classe mère `simulation_class` pour tous les processus stochastiques : initialisation depuis un `market_environment`, méthodes `generate_time_grid()` (grille temporelle commune) et `generate_instrument_values()` (valeurs simulées). |
| `3_Mouvement_brownien_geometrique.py` | ✅ Disponible | Classe `geometric_brownian_motion` héritant de `simulation_class` : discrétisation d'Euler du GBM sous mesure risque-neutre (`dS = r·S·dt + σ·S·dZ`), avec correction d'Itô `(r - σ²/2)`. |
| `4_Diffusion_par_sauts.py` | ✅ Disponible | Modèle de Merton avec sauts log-normaux : discrétisation d'Euler du processus, correction de drift `r_J = λ(e^(μ_J + σ_J²/2) - 1)`, deux sources aléatoires indépendantes (diffusion continue + amplitude des sauts), classe `jump_diffusion` héritant de `simulation_class`. |
| `5_Diffusion_a_racine_carree_CIR.py` | À venir | Processus de Cox-Ingersoll-Ross pour la modélisation des taux d'intérêt. |

---

### Module 2 — Évaluation de produits dérivés

Ce module construit les classes de pricing par Monte Carlo pour les options européennes et américaines, en s'appuyant sur les simulations du module précédent.

| Fichier | Statut | Description |
|---|---|---|
| `1_La_classe_d_evaluation_generique.py` | À venir | Classe mère pour le pricing de produits dérivés par Monte Carlo. |
| `2_La_classe_d_exercice_europeen.py` | À venir | Pricing d'options européennes (calls, puts, digitales…). |
| `3_La_classe_d_exercice_americain.py` | À venir | Pricing d'options américaines via l'algorithme de Longstaff-Schwartz (LSM). |

---

### Module 3 — Évaluation de portefeuille

Ce module étend l'évaluation à l'échelle d'un portefeuille multi-actifs en modélisant les positions individuelles puis en les agrégeant.

| Fichier | Statut | Description |
|---|---|---|
| `1_Position_de_produits_derives.py` | À venir | Modélisation d'une position individuelle (quantité, sous-jacent, payoff). |
| `2_Portefeuille_de_produits_derives.py` | À venir | Agrégation et évaluation d'un portefeuille de produits dérivés. |
| `3_Autres_ressources.py` | À venir | Ressources complémentaires et utilitaires. |

---

### Module 4 — Évaluation basée marché

Ce module confronte les modèles théoriques aux données réelles du marché : récupération des cotations d'options, calibration des paramètres et évaluation du portefeuille avec les paramètres calibrés.

| Fichier | Statut | Description |
|---|---|---|
| `1_Les_donnees_des_options.py` | À venir | Récupération et traitement des données d'options cotées sur le marché. |
| `2_La_calibration_du_modele.py` | À venir | Calibration des paramètres du modèle sur les prix de marché observés. |
| `3_L_evaluation_du_portefeuille.py` | À venir | Évaluation du portefeuille avec les paramètres calibrés. |

---

## Exécution

### Scripts Python
```bash
python '.\Module X - Nom du module\<nom_du_script>.py'
```
