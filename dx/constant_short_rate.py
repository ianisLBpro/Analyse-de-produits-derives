import numpy as np
from dx.get_year_deltas import *


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