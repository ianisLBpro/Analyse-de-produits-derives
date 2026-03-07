import numpy as np

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