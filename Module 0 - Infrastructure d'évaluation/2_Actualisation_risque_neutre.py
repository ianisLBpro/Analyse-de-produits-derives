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


import numpy as np
import pandas as pd
import datetime as dt

from pylab import mpl, plt
plt.style.use('seaborn')
mpl.rcParams['font.family'] = 'serif'

import sys
sys.path.append('../dx')


# Définition dates 
dates = [dt.datetime(2020,1,1), dt.datetime(2020,7,1), dt.datetime(2021,1,1)]

# Définition fractions d'année
fractions = (dates[1] - dates[0]).days / 365.0 

