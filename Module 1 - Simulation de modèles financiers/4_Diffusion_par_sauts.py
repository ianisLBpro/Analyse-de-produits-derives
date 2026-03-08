'''
4_Diffusion_par_sauts

Le modèle de diffusion par sauts étend le GBM en ajoutant des sauts discontinus au processus.

L'équation différentielle stochastique du modèle de diffusion par sauts de Merton est :

    dS_t = (r - r_J) * S_t * dt + σ * S_t * dZ_t + J_t * S_t * dN_t

Cette équation se décompose en trois parties :

    (r - r_J) * S_t * dt  → le DRIFT AJUSTÉ : comme dans le GBM mais corrigé
                            par r_J pour compenser l'espérance des sauts
                            et rester sous la mesure risque-neutre.

    σ * S_t * dZ_t        → la VOLATILITÉ CONTINUE : le bruit brownien classique,
                            les fluctuations normales du marché.

    J_t * S_t * dN_t      → le COMPOSANT DE SAUT : les chocs discontinus,
                            les événements rares et brutaux
                            (krach, annonce surprise, crise...).

Où :
    S_t   = valeur du processus au temps t
    r     = taux court constant (taux sans risque)
    r_J   = correction de drift liée aux sauts = λ * (e^(μ_J + σ_J²/2) - 1)
    σ     = volatilité du processus brownien continu
    dZ_t  = incrément du mouvement brownien standard

    J_t   = amplitude du saut, log-normale : ln(1 + J_t) ~ N(μ_J, σ_J²)
              └─ μ_J = moyenne du log des sauts
              └─ σ_J = volatilité des sauts

    dN_t  = incrément du processus de Poisson
              └─ λ = intensité de Poisson (nombre moyen de sauts par an)


Dans le cas d'une simulation discrète, on exploite une discrétisation d'EULER pour un modèle de diffusion par sauts :
On passe d'une équation continue à une équation discrète .

    S_(t_m+1) = S_(t_m) * ( exp( (r - r_J - σ²/2) * (t_m+1 - t_m) + σ * √(t_m+1 - t_m) * z_t ) + (e^(μ_J + σ_J² * z_J²) - 1) * y_t )

                            ↑_______________________________________________________________↑    ↑_________________________________↑
                                                COMPOSANT BROWNIEN CONTINU                                COMPOSANT DE SAUT
                                        
    0 ≤ t_m < t_m+1 ≤ T  = contrainte sur la grille temporelle

Décomposition terme par terme :

    S_(t_m)                       = valeur de départ au temps t_m

    --- COMPOSANT BROWNIEN CONTINU ---
    exp(...)                      = identique au GBM mais avec drift corrigé par r_J
    (r - r_J - σ²/2)              = drift ajusté par la correction d'Itô (σ²/2)
                                    ET par la compensation des sauts (r_J)
    σ * √(t_m+1 - t_m) * z_t      = choc brownien continu
    z_t ~ N(0,1)                  = nombre aléatoire pour la diffusion continue

    --- COMPOSANT DE SAUT ---
    e^(μ_J + σ_J * z_J) - 1       = amplitude du saut log-normal
    z_J ~ N(0,1)                  = nombre aléatoire pour l'amplitude du saut
    y_t                           = variable de Poisson : nombre de sauts
                                    sur l'intervalle (t_m, t_m+1)

Le modèle nécessite donc deux sources de nombres aléatoires indépendantes :
    z_t → pour la diffusion continue (comme dans le GBM)
    z_J → pour l'amplitude des sauts (spécifique au modèle de Merton)

Pour plus de précisions revoir la description des paramètres et variables dans le Repositories Github :
"Science-des-donnees-financieres" → Module 4 - Stochastique → 2_Simulation.py.
'''

import sys
sys.path.append('.')

import pandas as pd
import numpy as np
import time 
import datetime as dt
import matplotlib.pyplot as plt
from tabulate import tabulate

import dx
from dx.geometric_brownian_motion import geometric_brownian_motion
from dx.sn_random_numbers import sn_random_numbers
from dx.simulation_class import simulation_class


class jump_diffusion(simulation_class):
    ''' Classe pour générer des trajectoires simulées
    selon le modèle de Merton.

    Attributs
    =========
    name : str
        nom de l'objet
    mar_env : instance de market_environment
        données d'environnement de marché pour simulation
    corr : booléen
        True si corrélé avec autre objet de simulation

    Méthodes
    ========
    update :
        Actualise les paramètres
    generate_paths :
        Renvoie des trajectoires de Monte Carlo fonctions de l'environnement
    '''

    def __init__(self, name, mar_env, corr=False):
        super(jump_diffusion, self).__init__(name, mar_env, corr)
        # Autres paramètres requis
        self.lamb = mar_env.get_constant('lambda')
        self.mu = mar_env.get_constant('mu')
        self.delt = mar_env.get_constant('delta')

    def update(self, initial_value=None, volatility=None, lamb=None,
               mu=None, delta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if lamb is not None:
            self.lamb = lamb
        if mu is not None:
            self.mu = mu
        if delta is not None:
            self.delt = delta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            # méthode de la classe générique
            self.generate_time_grid()
        # nombre de dates pour time_grid
        M = len(self.time_grid)
        # nombre de trajectoires
        I = self.paths
        # initialisation ndarray pour simulation de trajectoire
        paths = np.zeros((M, I))
        # initialisation première date avec initial_value
        paths[0] = self.initial_value
        if self.correlated is False:
            # si pas corrélé, générer valeurs aléatoires
            sn1 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            # si corrélé, exploiter valeurs aléatoires fournies par l'environnement de marché
            sn1 = self.random_numbers
        # valeur aléatoire en distribution normale standard pour le composant de saut
        sn2 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)

        rj = self.lamb * (np.exp(self.mu + 0.5 * self.delt ** 2) - 1)

        short_rate = self.discount_curve.short_rate
        for t in range(1, len(self.time_grid)):
            # sélection de la bonne tranche temporelle pour le jeu de valeurs aléatoires concerné
            if self.correlated is False:
                ran = sn1[t]
            else:
                # seulement si corrélation dans portefeuille
                ran = np.dot(self.cholesky_matrix, sn1[:, t, :])
                ran = ran[self.rn_set]
            delta_t = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # différence entre deux dates comme fraction d'année
            poi = np.random.poisson(self.lamb * delta_t, I)
            # nombre aléatoire en distribution de Poisson pour le saut
            paths[t] = paths[t - 1] * (
                np.exp((short_rate - rj - 0.5 * self.volatility ** 2) * delta_t +
                        self.volatility * np.sqrt(delta_t) * ran) +
                        (np.exp(self.mu + self.delt * sn2[t]) - 1) * poi)
        self.instrument_values = paths


'''
Ce modèle étant différent du GBM, il a besoin de trois paramètres supplémentaires
par rapport aux composants de la table_composants_classique disponible 
en fin de chapitre 2_classe_de_simulation_générique.py.

Ce sont les paramètres du composant de saut log-normal :

    λ (lambda) = intensité de Poisson (nombre moyen de sauts par an)
    μ (mu)     = moyenne du log des sauts
    δ (delta)  = écart-type du log des sauts (noté σ_J dans la théorie)

Cette classe a besoin d'un plus grand nombre de valeurs aléatoires pour générer les trajectoires, 
à cause du composant de saut. Revoir "Science-des-donnees-financieres" → Module 4 - Stochastique 
en ce qui concerne la génération de valeurs aléatoires en distribution de Poisson. 
'''

table_composants_Merton = {
    'Composant': ['lambda', 'mu', 'delta'],
    
    'Type': ['Constante', 'Constante', 'Constante'],
    
    'Obligatoire ?': ['Oui', 'Oui', 'Oui'],
    
    'Description': [
        'Intensité de saut (probabilité par an)',
        'Taille de saut espérée',
        'Écart-type de taille de saut'
    ]
}

df_composants_Merton = pd.DataFrame(table_composants_Merton)
print('\nTableau 18.2 : Composants spécifiques de l\'environnement pour dx.jump_diffusion :')
print(tabulate(df_composants_Merton, headers='keys', tablefmt='pretty', showindex=False))




'''
Exercice : Simulation de trajectoires de diffusion par sauts
Nous allons simuler des trajectoires de diffusion par sauts avec deux niveaux d'intensité de saut différents.
Tout d'abord nous générons un objet dx.market_environment spécifique au modèle de diffusion par sauts,
en ajoutant les trois paramètres spécifiques du composant de saut à l'environnement GBM déjà créé.
'''

# Recréation de l'environnement GBM
me_gbm = dx.market_environment('me_gbm', dt.datetime(2020, 1, 1))
me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2020, 12, 31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'ME')
me_gbm.add_constant('paths', 10000)
csr = dx.constant_short_rate('csr', 0.06)
me_gbm.add_curve('discount_curve', csr)
gbm = geometric_brownian_motion('gbm', me_gbm)
gbm.generate_time_grid()


# Création du market environment spécifique au Jump Diffusion
me_jd = dx.market_environment('me_jd', dt.datetime(2020, 1, 1))

# Trois paramètres complémentaires spécifiques à dx.jump_diffusion
me_jd.add_constant('lambda', 0.3)
me_jd.add_constant('mu', -0.75)
me_jd.add_constant('delta', 0.1)

# Ajout d'un environnement complexe à celui déjà existant
me_jd.add_environment(me_gbm)

# Instanciation de l'objet de simulation
jd = jump_diffusion('jd', me_jd)

# Simulation des trajectoires avec les paramètres de base
start = time.time()
paths_3 = jd.get_instrument_values()
end = time.time()
print('\nTrajectoires paths_3 (arrondi à 3 décimales) :')
print(paths_3.round(3))
print(f'Temps d\'exécution paths_3 : {(end - start) * 1000:.1f} ms')

# Augmentation du paramètre d'intensité de sauts
jd.update(lamb=0.9)

# Simulation des trajectoires avec les paramètres actualisés
start = time.time()
paths_4 = jd.get_instrument_values()
end = time.time()
print('\nTrajectoires paths_4 (arrondi à 3 décimales) :')
print(paths_4.round(3))
print(f'Temps d\'exécution paths_4 : {(end - start) * 1000:.1f} ms')

# Visualisation
plt.figure(figsize=(10, 6))
p1 = plt.plot(gbm.time_grid, paths_3[:, :10], 'b')
p2 = plt.plot(gbm.time_grid, paths_4[:, :10], 'r-.')
l1 = plt.legend([p1[0], p2[0]],
                ['faible intensité', 'haute intensité'], loc=3)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.title('Trajectoires simulées avec la classe de simulation Jump Diffusion')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.tight_layout()
plt.show()