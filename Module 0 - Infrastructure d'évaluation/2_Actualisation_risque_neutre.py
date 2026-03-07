'''
2_Actualisation risque neutre

L'actualisation risque neutre est au coeur de la valorisation des produits dérivés.
L'idée est simple : pour connaître la valeur aujourd'hui d'un flux futur,
on l'actualise au taux sans risque r sous la probabilité risque neutre Q.

Avant d'implémenter cette logique, il faut résoudre une question pratique :
comment représenter et manipuler le temps en Python ?

Pour valoriser un dérivé, on découpe la durée de vie du contrat entre aujourd'hui
et la date de maturité T en une série d'intervalles discrets.
Ces intervalles n'ont pas besoin d'être de longueur égale, notre code doit
gérer le cas général d'intervalles non homogènes.

Deux règles de base s'appliquent :
- La granularité minimale est le jour (pas de gestion des heures ou des minutes)
- Le code travaille avec des listes de dates, qu'il convertit ensuite en fractions d'année
'''


import numpy as np
import pandas as pd
import datetime as dt

from pylab import mpl, plt
plt.style.use('seaborn-v0_8')
mpl.rcParams['font.family'] = 'serif'



'''
Modélisation et traitement des dates :

2 approches sont possibles pour modéliser les dates :
- Construire la liste explicitement, sous formes d'objets datetime 
- Travailler avec des fractions d'année sous forme de valeurs décimales
'''

# Date format datetime :
dates = [dt.datetime(2020,1,1), dt.datetime(2020,7,1), dt.datetime(2021,1,1)]

# Date format fractions d'année :
print("Dates format fractions d'année :")
print((dates[1] - dates[0]).days / 365.0)
print((dates[2] - dates[1]).days / 365.0)

fractions = [0.0, 0.5, 1.0]


'''
L'équivalence est imparfaite car une fraction d'année tombe rarement 
sur le même début qu'une date exprimée explicitement. 
(0 heure le premier jour)
On ne peut pas diviser le nombre de jours d'une année par 50. 

Nous allons créer une fonction get_year_deltas() afin de générer des fractions d'année à partir d'une liste de dates.
'''

def get_year_deltas(date_list, day_count=365.):
    ''' Renvoie un vecteur de floats avec des deltas de jour en fraction d'année.
    Valeur initiale normalisée à zéro. 

    Paramètres
    ==========
    date_list: list ou array
        collection d'objets datetime
    day_count: float
        nombre de jours dans une année
        (pour tenir compte des différentes conventions)

    Résultats
    =======
    delta_list: array
        fractions d'année
    '''

    start = date_list[0]
    delta_list = [(date - start).days / day_count for date in date_list]
    return np.array(delta_list)

# La fonction s'utilise de la manière suivante : 
print("\nFonction get_year_deltas() :")
print(get_year_deltas(dates))




'''
Taux court constant :

On suppose ici que le taux sans risque r est constant sur toute la durée de vie 
du contrat. C'est l'hypothèse retenue par la plupart des modèles classiques 
de valorisation d'options (Black-Scholes-Merton, Cox-Ross-Rubinstein...).

Sous cette hypothèse, le facteur d'actualisation entre aujourd'hui et une date t
(exprimée en fraction d'année) est :

    D(0, t) = e^(-r * t)

Ce facteur représente également la valeur aujourd'hui d'un zéro-coupon 
(obligation qui paie 1 unité monétaire à maturité, sans coupons intermédiaires).

Entre deux dates t > s, le facteur d'actualisation devient :

    D(s, t) = D(0,t) / D(0,s) = e^(-r*(t-s))

Nous allons implémenter ces calculs dans une classe ConstantShortRate.
'''

class constant_short_rate(object):
    ''' Classe pour l'actualisation à taux court constant.

    Attributs
    =========
    name : string
        nom de l'objet
    short_rate : float (>= 0)
        taux d'actualisation constant

    Méthodes
    ========
    get_discount_factors :
        obtient les facteurs d'actu à partir d'une liste/tableau d'objets datetime
        ou de fractions d'année
    '''

    def __init__(self, name, short_rate):
        self.name = name
        self.short_rate = short_rate
        if short_rate < 0:
            raise ValueError('Le taux court ne peut pas être négatif.')
            # c'est discutable au vu des taux négatifs déjà observés

    def get_discount_factors(self, date_list, dtobjects=True):
        if dtobjects is True:
            dlist = get_year_deltas(date_list)
        else:
            dlist = np.array(date_list)
        dflist = np.exp(self.short_rate * np.sort(-dlist))
        return np.array((date_list, dflist))


'''
Exemple d'utilisation de la classe constant_short_rate :
On instancie la classe avec un taux de 5%, puis on calcule les facteurs
d'actualisation dans les deux formats possibles.
'''

csr = constant_short_rate('csr', 0.05)
print("\nFacteurs d'actualisation format datetime :")
print(csr.get_discount_factors(dates))

deltas = get_year_deltas(dates)
print("\nDeltas de jour en fractions d'année :")
print(deltas)

print("\nFacteurs d'actualisation format fractions d'année :")
print(csr.get_discount_factors(deltas, dtobjects=False))
