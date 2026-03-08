'''
2_Classe_de_simulation_generique

Dans ce chapitre, nous abordons un des mécanismes FONDAMENTAUX de l'orientation objet :
- La transmission par héritage des valeurs des attributs, des définitions et des méthodes

Nous allons définir un classe de simulation générique ("ancestrale") qui définit
les attributs et les méthodes dont toutes les classes de simulation spécialisés vont avoir besoin.

Dans chaque classe descendante, nous traiterons les éléments spécifiques au processus stochastique qu'elle incarne. 

Quelle que soit la classe de simulation, la création d'une instance, d'un objet, requiert trois attributs d'entrée :
- name : un objet de type str contenant le nom de l'objet de simulation
- mar_env : une instance de la classe dx.market_environement définit dans le module 0 
- corr : un témoin de type booléen qui détermine si l'objet est corrélé ou pas

L'intérêt de la classe d'environnement de marché est de fournir en une étape 
les données et les objets nécessaires à la simulation et à l'évaluation. 

Voici les méthodes définies dans la classe générique : 
- generate_time_grid() : cette méthode génère la grille temporelle des dates utilisées dans la simulation;
l'opération est la même pour toutes les classes de simulation.
- generate_instrument_values() : chaque classe de simulation doit renvoyer un objet ndarray contenant 
les valeurs d'instruments simulés (cours d'actions, prix de commodités, volatilté, etc.). 
'''



import numpy as np
import pandas as pd
from tabulate import tabulate


class simulation_class(object):
    ''' Définit des méthodes de base pour les classes de simulation. 

    Attributs
    =========
    name: chaîne str
        nom de l'objet
    mar_env: instance de market_environment
        données de l'environnement de marché pour la simulation
    corr: booléen
        True si corrélé avec un autre objet de modèle

    Méthodes
    ========
    generate_time_grid:
        renvoie une grille temporelle 
    get_instrument_values:
        renvoie un tableau des valeurs d'instruments actuelles
    '''

    def __init__(self, name, mar_env, corr):
        self.name = name
        self.pricing_date = mar_env.pricing_date
        self.initial_value = mar_env.get_constant('initial_value')
        self.volatility = mar_env.get_constant('volatility')
        self.final_date = mar_env.get_constant('final_date')
        self.currency = mar_env.get_constant('currency')
        self.frequency = mar_env.get_constant('frequency')
        self.paths = mar_env.get_constant('paths')
        self.discount_curve = mar_env.get_curve('discount_curve')
        try:
            # si time_grid dans mar_env prendre cet objet (pour l'évaluation du portefeuille)
            self.time_grid = mar_env.get_list('time_grid')
        except:
            self.time_grid = None
        try:
            # si date spéciales, les ajouter 
            self.special_dates = mar_env.get_list('special_dates')
        except:
            self.special_dates = []
        self.instrument_values = None
        self.correlated = corr
        if corr is True:
            # requis seulement pour portefeuille si corrélation de facteurs de risque
            self.cholesky_matrix = mar_env.get_list('cholesky_matrix')
            self.rn_set = mar_env.get_list('rn_set')[self.name]
            self.random_numbers = mar_env.get_list('random_numbers')

    def generate_time_grid(self):
        start = self.pricing_date
        end = self.final_date
        # Fonction pandas date_range
        # freq = ex. 'B' pour jour ouvré (Business), 'W' pour hebdomadaire (Weekly), 'M' pour mensuel (Monthly)
        time_grid = pd.date_range(start=start, end=end, freq=self.frequency).to_pydatetime()
        time_grid = list(time_grid)
        # complète time_grid avec start, end et spécial_dates
        if start not in time_grid:
            time_grid.insert(0, start)
            # ajoute date de début si pas présente 
        if end not in time_grid:
            time_grid.append(end)
            # insère date de fin si pas présente
        if len(self.special_dates) > 0:
            # ajoute les dates spéciales
            time_grid.extend(self.special_dates)
            # supprime les doublons
            time_grid = list(set(time_grid))
            # trie la liste
            time_grid.sort()
        self.time_grid = np.array(time_grid)

    def get_instrument_values(self, fixed_seed=True):
        if self.instrument_values is None:
            # Démarre la simulation seulement si pas de valeurs d'instruments
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        elif fixed_seed is False:
            # Relance la re-simulation si fixed_seed vaut False 
            self.generate_paths(fixed_seed=fixed_seed, day_count=365.)
        return self.instrument_values


'''
NOTE IMPORTANTE : Absence de vérification des types

Lors de l'instanciation, __init__() récupère les données du market_environment
sans vérifier que ce qu'il reçoit est bien du bon type.

Exemple concret avec la discount_curve :
    self.discount_curve = mar_env.get_curve('discount_curve')

Python acceptera cette ligne SANS erreur même si on passe n'importe quoi
à la place d'une vraie instance de constant_short_rate.

L'erreur n'apparaîtra que plus tard, quand on essaiera d'utiliser
self.discount_curve pour actualiser des cash flows avec un message
d'erreur confus, loin du vrai problème.

BONNE PRATIQUE : quand on construit market_environment, assurons-nous
toujours de passer le bon type d'objet :

    taux = dx.constant_short_rate('taux_rf', 0.05)
    me.add_curve('discount_curve', taux)

    Attention à ne pas mettre un float par exemple :
    me.add_curve('discount_curve', 0.05) 
'''


# Affichage des composants de l'environnement de marché pour les classes de simulation
table_composants_classique = {
    'Composant': ['currency', 'discount_curve', 'final_date', 'frequency', 
                  'initial_value', 'paths', 'volatility', 'cholesky_matrix',
                  'random_numbers', 'rn_set', 'time_grid'],
    
    'Type': ['Constante', 'Courbe', 'Constante', 'Constante', 
             'Constante', 'Constante', 'Constante', 'Liste',
             'Liste', 'Liste', 'Liste'],
    
    'Obligatoire ?': ['Oui', 'Oui', 'Oui', 'Oui', 
                      'Oui', 'Oui', 'Oui', 'Non',
                      'Non', 'Non', 'Non'],
    
    'Description': [
        "Devise de l'entité financière",
        'Instance de dx.constant_short_rate',
        'Horizon de simulation',
        'Fréquence, comme freq de pandas',
        'Valeur initiale en date de pricing_date',
        'Nombre de trajectoires à simuler',
        'Coefficient de volatilité du processus',
        'Matrice de Cholesky (pour objets corrélés)',
        'np.ndarray de nombres aléatoires (pour objets corrélés)',
        'Objet dict avec pointeur sur le jeu de nombres aléatoires à utiliser',
        'Grille temporelle des dates (contexte de portefeuille)'
    ]
}

df_composants_classique = pd.DataFrame(table_composants_classique)
print('\n Composants de l\'environnement de marché pour les classes de simulation :')
print(tabulate(df_composants_classique, headers='keys', tablefmt='pretty', showindex=False))

