import numpy as np
import pandas as pd


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