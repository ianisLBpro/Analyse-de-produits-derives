'''
3_Environnement de marché

Un environnement de marché est un conteneur qui regroupe en un seul objet
toutes les données nécessaires à la simulation et à la valorisation d'un dérivé.

Plutôt que de passer une dizaine de paramètres séparément à chaque classe,
on les rassemble dans un objet unique qu'on transmet en une seule fois.

Il se compose de trois compartiments :
- constantes : les scalaires (taux r, volatilité σ, prix spot S0, maturité...)
- listes     : les collections d'objets (grilles de dates, sous-jacents...)
- courbes    : les objets d'actualisation (instance de constant_short_rate)
'''


import numpy as np
import pandas as pd
import datetime as dt

from pylab import mpl, plt
plt.style.use('seaborn-v0_8')
mpl.rcParams['font.family'] = 'serif'

import sys
sys.path.append('..')

from dx.get_year_deltas import get_year_deltas
from dx.constant_short_rate import constant_short_rate


class market_environment(object):
    ''' Modélise un environnement de marché pour évaluation

    Attributs
    =========
    name : string
        nom de l'environnement
    pricing_date : datetime object 
        date de valorisation

    Méthodes
    ========
    add_constant : 
        ajoute une constante (un paramètre du modèle)
    get_constant :
        relit la valeur d'une constante
    add_list :
        ajoute une liste (un sous-jacent)
    get_list :
        relit une liste
    add_curve :
        ajoute une courbe de marché (ex. courbe des taux)
    get_curve :
        relit une courbe de marché
    add_environment :
        ajoute et met à jour tout l'environnement avec des constantes, 
        des listes et des courbes 
    '''

    def __init__(self, name, pricing_date):
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}

    def add_constant(self, key, constant):
        self.constants[key] = constant

    def get_constant(self, key):
        return self.constants[key]

    def add_list(self, key, list_object):
        self.lists[key] = list_object

    def get_list(self, key):
        return self.lists[key]

    def add_curve(self, key, curve):
        self.curves[key] = curve

    def get_curve(self, key):
        return self.curves[key]

    def add_environment(self, env):
        # Ecrase toute valeur déjà présente 
        self.constants.update(env.constants)
        self.lists.update(env.lists)
        self.curves.update(env.curves)


'''
Exemple d'utilisation :
On crée un environnement pour un modèle de mouvement brownien géométrique (GBM)
et on y stocke tous les paramètres dont on aura besoin pour la simulation.
'''

# On crée un objet constant_short_rate avec un taux de 5%
csr = constant_short_rate('csr', 0.05)

# On crée un environnement de marché daté du 1er janvier 2020
me = market_environment('me_gbm', dt.datetime(2020, 1, 1))

# On ajoute les paramètres du modèle
me.add_constant('initial_value', 36.)
me.add_constant('volatility', 0.2)
me.add_constant('final_date', dt.datetime(2020, 12, 31))
me.add_constant('currency', 'EUR')
me.add_constant('frequency', 'M')
me.add_constant('paths', 10000)

# On ajoute la courbe d'actualisation
me.add_curve('discount_curve', csr)

# Vérification : on récupère les valeurs stockées
print("Volatilité :", me.get_constant('volatility'))
print("Taux court :", me.get_curve('discount_curve').short_rate)