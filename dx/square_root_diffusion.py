import numpy as np

from dx.simulation_class import simulation_class
from dx.sn_random_numbers import sn_random_numbers

class square_root_diffusion(simulation_class):
    ''' Classe de génération de trajectoires simulées selon le modèle
    Cox-Ingersoll-Ross (CIR) ou diffusion à racine carrée.

    Attributs
    =========
    name : chaîne str
        nom de l'objet
    mar_env : instance de market_environment
        données de l'environnement de marché pour la simulation
    corr : booléen
        True si corrélation avec d'autres objets modèles 

    Methodes
    ========
    update :
        Actualise les paramètres
    generate_paths :
        Renvoie des trajectoires de Monte Carlo en fonction de l'environnement 
    '''

    def __init__(self, name, mar_env, corr=False):
        super(square_root_diffusion, self).__init__(name, mar_env, corr)
        # Récupération des paramètres spécifiques au modèle CIR
        self.kappa = mar_env.get_constant('kappa')
        self.theta = mar_env.get_constant('theta')

    def update(self, initial_value=None, volatility=None, kappa=None, theta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if kappa is not None:
            self.kappa = kappa
        if theta is not None:
            self.theta = theta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=True, day_count=365.):
        if self.time_grid is None:
            self.generate_time_grid()
        M = len(self.time_grid)
        I = self.paths
        # paths : trajectoires tronquées (toujours >= 0)
        paths = np.zeros((M, I))
        # paths_ : trajectoires brutes avant troncature
        paths_ = np.zeros_like(paths)
        paths[0] = self.initial_value
        paths_[0] = self.initial_value
        if self.correlated is False:
            rand = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            rand = self.random_numbers

        for t in range(1, len(self.time_grid)):
            dt = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            if self.correlated is False:
                ran = rand[t]
            else:
                ran = np.dot(self.cholesky_matrix, rand[:, t, :])
                ran = ran[self.rn_set]

            # discretisation d'Euler à troncature complète
            paths_[t] = (paths_[t - 1] + self.kappa *
                        (self.theta - np.maximum(0, paths_[t - 1, :])) * dt +
                        np.sqrt(np.maximum(0, paths_[t - 1, :])) *
                        self.volatility * np.sqrt(dt) * ran)
            paths[t] = np.maximum(0, paths_[t])
        self.instrument_values = paths