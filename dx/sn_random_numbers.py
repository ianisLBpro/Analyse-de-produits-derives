import numpy as np

def sn_random_numbers(shape, antithetic=True, moment_matching=True, fixed_seed=False):
    '''Renvoie un ndarray de forme shape peuplé de (pseudo)aléatoires 
    en distribution standard normale.
    
    Paramètres
    ==========
    shape: tuple (o, n, m)
        produitun tableau en forme (o, n, m)
    antithetic: boolean
        génération de variantes antithétiques
    moment_matching: boolean
        correspondance des premier et deuxième moments 
    fixed_seed: Boolean
        drapeau pour fixer le germe du générateur

    Résultats
    =========
    ran: (o, n, m) tableau de nombres aléatoires
    '''

    if fixed_seed:
        np.random.seed(1000)
    if antithetic:
        ran = np.random.standard_normal((shape[0], shape[1], shape[2]//2))
        ran = np.concatenate((ran, -ran), axis=2)
    else:
        ran = np.random.standard_normal(shape)
    if moment_matching:
        ran = ran - np.mean(ran)
        ran = ran / np.std(ran)
    if shape[0] == 1:
        return ran[0]
    else:
        return ran