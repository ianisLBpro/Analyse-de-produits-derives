'''
Dans ce chapitre nous allons aborder la question de l'actualisation risque neutre, 
il est évident qu'elle est essentielle dans l'approche d'évaluation risque neutre. 

Nous allons donc définir une classe Python pour réaliser cette actualisation.


Tout d'abord voyons plus en détail la modélisation et le traitement des dates pertinentes d'une évaluation.
On va diviser l'intervalle temporel entre le jour même et la date de maturité d'un modèle de marché général T en plusieurs intervalles discrets. 
Les intervalles peuvent être tous de même longueur ou pas. La librairire d'évaluation doit être en mesure de gérer le cas général d'intervalles non homogènes. 
Le code doit fonctionner avec des listes de dates, nous supposerons que la durée minimale est égale à un jour. 
Les évèvenements intraday sont considérés comme non pertinents, car cela supposerait de mobiliser également le temps en plus de la date. 

2 approches sont possibles pour modéliser les dates :
- Construire la liste explicitement, sous formes d'objets datetime 
- Travailler avec des fractions d'année sous forme de valeurs décimales

'''


from tracemalloc import start

import numpy as np
import pandas as pd
import datetime as dt

from pylab import mpl, plt
plt.style.use('seaborn-v0_8')
mpl.rcParams['font.family'] = 'serif'

import sys
sys.path.append('../dx')


# Les 2 définition dates et fractions d'année sont équivalentes 
dates = [dt.datetime(2020,1,1), dt.datetime(2020,7,1), dt.datetime(2021,1,1)]
print("Dates 1")
print((dates[1] - dates[0]).days / 365.0)
print("\n Dates 2")
print((dates[2] - dates[1]).days / 365.0)

fractions = [0.0, 0.5, 1.0]

'''
L'équivalence est imparfaite car une fraction d'année tombe rarement sur le même début qu'une date exprimée explicitement. (0 heure le premier jour)
On ne peut pas diviser le nombre de jours d'une année par 50. 

Nous allons créer une fonction get_year_deltas() afin de générer des fractions d'année à partir d'une liste de dates.
'''

def get_year_deltas(date_list, day_count=365.):
    ''' Return vector of floats with day deltas in year fractions.
    Initial value normalized to zero.

    Parameters
    ==========
    date_list: list or array
    collection of datetime objects
    day_count: float
    number of days for a year
    (to account for different conventions)

    Results
    =======
    delta_list: array
    year fractions
    '''

    start = date_list[0]
    delta_list = [(date - start).days / day_count for date in date_list]
    return np.array(delta_list)

# La fonction s'utilise de la manière suivante : 
print("\n Fonction get_year_deltas()")
print(get_year_deltas(dates))