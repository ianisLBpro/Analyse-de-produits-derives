import numpy as np
from dx.sn_random_numbers import sn_random_numbers
from dx.simulation_class import simulation_class


class geometric_brownian_motion(simulation_class):
    ''' Classe générant des trajectoires simulés selon le modèle
    de mouvement brownien géométrique Black-Scholes-Merton.

    Attributs
    ========
    name : chaîne str
        nom de l'objet 
    mar_env : instance de market_environment
        données d'environnement de marché pour simulation
    corr : booléen 
        True si corrélé avec autre objet de simulation

    Méthodes
    ========
    update : 
        Actualise les paramètres 
    generate_paths :
        Renvoie des trajectoires de Monte Carlo fonctions de l'environnement 
    '''

    def __init__(self, name, mar_env, corr=False):
        super(geometric_brownian_motion, self).__init__(name, mar_env, corr)

    def update(self, initial_value=None, volatility=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None 

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            # Méthode de la classe générique
            self.generate_time_grid()
        # nombre de dates pour time_grid
        M = len(self.time_grid)
        # nombre de trajectoires à simuler
        I = self.paths
        # initialisation ndarray pour simulation de trajectoire 
        paths = np.zeros((M, I))
        # initialisation de la première date avec initial_value
        paths[0] = self.initial_value
        if not self.correlated:
            # si pas corrélé, générer les valeurs aléatoires
            rand = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            # si corrélé, exploiter valeurs aléatoires fournies par l'environnement de marché 
            rand = self.random_numbers
        short_rate = self.discount_curve.short_rate
        # obtention du taux court pour drift du processus
        for t in range(1, len(self.time_grid)):
            # sélection de la bonne tranche temporelle pour le jeu de valeurs aléatoires concerné
            if not self.correlated:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]
            delta_t = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # différence entre deux dates en fraction d'année 
            paths[t] = paths[t - 1] * np.exp((short_rate - 0.5 * 
                                              self.volatility ** 2) * delta_t + 
                                              self.volatility * np.sqrt(delta_t) * ran)
            # génère des valeurs simulés pour la date concernée 
        self.instrument_values = paths