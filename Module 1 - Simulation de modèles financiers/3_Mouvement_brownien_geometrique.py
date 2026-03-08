'''
3_Mouvement_brownien_geometrique

Le GBM est un processus stochastique dont l'équation différentielle est :

    dS_t = r * S_t * dt + σ * S_t * dZ_t

Cette équation se décompose en deux parties :

    r * S_t * dt    → le DRIFT : la tendance moyenne du processus.
                      C'est la direction générale que suit l'actif,
                      comme une balle qui roule sur une table inclinée.

    σ * S_t * dZ_t  → la VOLATILITÉ : le bruit aléatoire autour du drift,
                      les zigzags imprévisibles autour de la tendance.

Où :
    S_t   = valeur du processus au temps t
    r     = taux court constant (taux sans risque)
    σ     = volatilité du processus
    dZ_t  = incrément du mouvement brownien standard
    dt    = incrément de temps infinitésimal

Le drift est fixé au taux sans risque r car on travaille sous la mesure
martingale équivalente (mesure risque-neutre) : 
Dans ce monde fictif, tous les actifs rapportent en moyenne le taux sans risque.
C'est le fondement du pricing d'options (Black-Scholes).


Pour simuler le GBM on utilise la discrétisation d'EULER, on passe d'une équation continue à une équation discrète :

    S_(t_m+1) = S_(t_m) * exp( (r - σ²/2) * (t_m+1 - t_m)  +  σ * √(t_m+1 - t_m) * z )
                               ↑________________________↑    ↑_______________________↑
                                     DRIFT AJUSTÉ                  CHOC ALÉATOIRE

    0 ≤ t_m < t_m+1 ≤ T  = contrainte sur la grille temporelle                  

Décomposition terme par terme :

    S_(t_m)              = valeur de départ au temps t_m

    exp(...)             = on exponentielle car le GBM est un processus MULTIPLICATIF
                           (les rendements sont log-normaux, pas normaux)

    (r - σ²/2)           = drift ajusté par la correction d'Itô :
                           sans ce -σ²/2, la simulation serait biaisée à la hausse
                           à cause de la convexité de l'exponentielle (lemme d'Itô)

    (t_m+1 - t_m)        = pas de temps entre deux dates de la grille temporelle

    σ * √(t_m+1 - t_m)   = volatilité mise à l'échelle du pas de temps
                           (la volatilité scale en racine carrée du temps)

    z                    = nombre aléatoire normal standard ~ N(0,1)
                           généré par sn_random_numbers()

Le modèle est discret : on simule S à chaque date de la grille temporelle.

Pour plus de précisions revoir la description des paramètres et variables dans le Repositories Github :
"Science-des-donnees-financieres" → Module 4 - Stochastique → 2_Simulation.py.
'''

import sys
sys.path.append('.')

import numpy as np
import time 
import datetime as dt
import matplotlib.pyplot as plt

import dx
from dx.sn_random_numbers import sn_random_numbers
from dx.simulation_class import simulation_class



class geometric_brownian_motion(simulation_class):
    ''' Classe générant des trajectoires simulés selon le modèle
    de mouvement brownien géométrique Black-Scholes-Merton.

    Attributs
    ========
    name : chaîne str
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
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None 

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            # Méthode de la classe générique
            self.generate_time_grid()
        # nombre de dates pour time_grid
        M = len(self.time_grid)
        # nombre de trajectoires à simuler
        I = self.paths
        # initialisation ndarray pour simulation de trajectoire 
        paths = np.zeros((M, I))
        # initialisation de la première date avec initial_value
        paths[0] = self.initial_value
        if not self.correlated:
            # si pas corrélé, générer les valeurs aléatoires
            rand = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            # si corrélé, exploiter valeurs aléatoires fournies par l'environnement de marché 
            rand = self.random_numbers
        short_rate = self.discount_curve.short_rate
        # obtention du taux court pour drift du processus
        for t in range(1, len(self.time_grid)):
            # sélection de la bonne tranche temporelle pour le jeu de valeurs aléatoires concerné
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            delta_t = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # différence entre deux dates en fraction d'année 
            paths[t] = paths[t - 1] * np.exp((short_rate - 0.5 * 
                                              self.volatility ** 2) * delta_t + 
                                              self.volatility * np.sqrt(delta_t) * ran)
            # génère des valeurs simulés pour la date concernée 
        self.instrument_values = paths


'''
Pour instancier un objet GBM, le market_environment doit contenir
au minimum les composants du Tableau 'table_composants_classique' 
disponible en fin de chapitre 2_classe_de_simulation_générique.py (les éléments obligatoires).

La classe GBM contient deux méthodes principales :

    update()          → permet de mettre à jour les paramètres clés du modèle
                        (ex. changer la volatilité ou la valeur initiale)
                        sans avoir à recréer un nouvel objet.

    generate_paths()  → génère les trajectoires simulées du processus.
                        C'est la méthode centrale de la classe.
                        Elle gère également la corrélation entre plusieurs
                        objets de simulation (utile en contexte portefeuille,
                        détaillé dans le Module 3 - Evaluation de portefeuille).
'''




'''
Exercice : Simulation de trajectoires de GBM
Nous allons ici simuler des trajectoires de GBM avec deux niveaux de volatilité différents.
Tout d'abord nous générons un objet dx.market_environment contenant les éléments attendus. 
'''

me_gbm = dx.market_environment('me_gbm', dt.datetime(2020, 1, 1))

me_gbm.add_constant('initial_value', 36.)
me_gbm.add_constant('volatility', 0.2)
me_gbm.add_constant('final_date', dt.datetime(2020, 12, 31))
me_gbm.add_constant('currency', 'EUR')
me_gbm.add_constant('frequency', 'ME')  # fréquence mensuelle (fin de mois)
me_gbm.add_constant('paths', 10000)

csr = dx.constant_short_rate('csr', 0.06)

me_gbm.add_curve('discount_curve', csr)

'''
Nous pouvons alors créer un objet de simulation pour travailler. 
'''

# Instanciation de l'objet de simulation 
gbm = geometric_brownian_motion('gbm', me_gbm)

# Génération de la grille temporelle 
gbm.generate_time_grid()

# Affichage de la grille temporelle, la date initiale a été ajoutée
print('Grille temporelle :')
print(gbm.time_grid)

# Affichage de la vitesse d'exécution de paths_1
start = time.time()
paths_1 = gbm.get_instrument_values()
end = time.time()
# Génération des trajectoires simulés pour paths_1 arrondies à 3 décimales
print('\nTrajectoires paths_1 (arrondi à 3 décimales) :')
print(paths_1.round(3))
print(f'Temps d\'exécution paths_1 : {(end - start) * 1000:.1f} ms')

# Actualisation du paramètre de volatilité 
gbm.update(volatility=0.5)

# Affichage de la vitesse d'exécution de paths_2
start = time.time()
paths_2 = gbm.get_instrument_values()
end = time.time()
# Génération des trajectoires simulés pour paths_2 arrondies à 3 décimales
print('\nTrajectoires paths_2 (arrondi à 3 décimales) :')
print(paths_2.round(3))
print(f'Temps d\'exécution paths_2 : {(end - start) * 1000:.1f} ms')


# Visualisation de trajectoires simulés pour les deux niveaux de volatilité
plt.figure(figsize=(10, 6))
p1 = plt.plot(gbm.time_grid, paths_1[:, :10], 'b')
p2 = plt.plot(gbm.time_grid, paths_2[:, :10], 'r-.')
l1 = plt.legend([p1[0], p2[0]],
                ['faible volatilité', 'haute volatilité'], loc=2)
plt.gca().add_artist(l1)
plt.xticks(rotation=30)
plt.title('Trajectoires simulées avec la classe de simulation GBM')
plt.xlabel('Date')
plt.ylabel('Valeur')
plt.tight_layout()
plt.show()
