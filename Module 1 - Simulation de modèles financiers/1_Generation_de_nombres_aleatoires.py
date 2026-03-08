'''
1_Generation_de_nombres_aleatoires

La génération de nombres aléatoires est une composante essentielle des simulations de Monte Carlo. 
Dans ce chapitre, nous allons voir comment générer des valeures aléatoires en sitribution normale standard.
pour cela, nous allons définir une fonction dédiée sn_random_numbers() 
qui permet de générer ce type de valeurs aléatoires. 

A savoir : 
Le livre de Glasserman, "Monte Carlo Methods in Financial Engineering", 
est une référence incontournable pour comprendre les méthodes de Monte Carlo en finance,
il aborde la génération de valeurs aléatoires et des variables et des détails théoriques de différentes
techniques de réduction de variance que nous utilisons. 
'''

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


'''
Deux techniques de réduction de variance sont disponibles dans la fonction sn_random_numbers() :
La première moment_matching = False, génère des nombres aléatoires standard sans ajuster les moments.
La seconde moment_matching = True, ajuste les nombres aléatoires pour correspondre exactement à une moyenne de 0.
'''
snrn = sn_random_numbers((2, 2, 2), antithetic=False, moment_matching=False, fixed_seed=True)
print('Nombres aléatoires moment_matching = False')
print(snrn)
print('Moyenne : ')
print(round(snrn.mean(), 6))
print('Écart-type : ')
print(round(snrn.std(), 6))

snrn = sn_random_numbers((2, 2, 2), antithetic=False, moment_matching=True, fixed_seed=True)
print('\nNombres aléatoires moment_matching = True')
print(snrn)
print('Moyenne : ')
print(round(snrn.mean(), 6))
print('Écart-type : ')
print(round(snrn.std(), 6))
