
import numpy as np
from dx.sn_random_numbers import sn_random_numbers
from dx.simulation_class import simulation_class


class jump_diffusion(simulation_class):
    ''' Classe pour générer des trajectoires simulées
    selon le modèle de Merton.

    Attributs
    =========
    name : str
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
        super(jump_diffusion, self).__init__(name, mar_env, corr)
        # Autres paramètres requis
        self.lamb = mar_env.get_constant('lambda')
        self.mu = mar_env.get_constant('mu')
        self.delt = mar_env.get_constant('delta')

    def update(self, initial_value=None, volatility=None, lamb=None,
               mu=None, delta=None, final_date=None):
        if initial_value is not None:
            self.initial_value = initial_value
        if volatility is not None:
            self.volatility = volatility
        if lamb is not None:
            self.lamb = lamb
        if mu is not None:
            self.mu = mu
        if delta is not None:
            self.delt = delta
        if final_date is not None:
            self.final_date = final_date
        self.instrument_values = None

    def generate_paths(self, fixed_seed=False, day_count=365.):
        if self.time_grid is None:
            # méthode de la classe générique
            self.generate_time_grid()
        # nombre de dates pour time_grid
        M = len(self.time_grid)
        # nombre de trajectoires
        I = self.paths
        # initialisation ndarray pour simulation de trajectoire
        paths = np.zeros((M, I))
        # initialisation première date avec initial_value
        paths[0] = self.initial_value
        if self.correlated is False:
            # si pas corrélé, générer valeurs aléatoires
            sn1 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)
        else:
            # si corrélé, exploiter valeurs aléatoires fournies par l'environnement de marché
            sn1 = self.random_numbers
        # valeur aléatoire en distribution normale standard pour le composant de saut
        sn2 = sn_random_numbers((1, M, I), fixed_seed=fixed_seed)

        rj = self.lamb * (np.exp(self.mu + 0.5 * self.delt ** 2) - 1)

        short_rate = self.discount_curve.short_rate
        for t in range(1, len(self.time_grid)):
            # sélection de la bonne tranche temporelle pour le jeu de valeurs aléatoires concerné
            if self.correlated is False:
                ran = sn1[t]
            else:
                # seulement si corrélation dans portefeuille
                ran = np.dot(self.cholesky_matrix, sn1[:, t, :])
                ran = ran[self.rn_set]
            delta_t = (self.time_grid[t] - self.time_grid[t - 1]).days / day_count
            # différence entre deux dates comme fraction d'année
            poi = np.random.poisson(self.lamb * delta_t, I)
            # nombre aléatoire en distribution de Poisson pour le saut
            paths[t] = paths[t - 1] * (
                np.exp((short_rate - rj - 0.5 * self.volatility ** 2) * delta_t +
                        self.volatility * np.sqrt(delta_t) * ran) +
                        (np.exp(self.mu + self.delt * sn2[t]) - 1) * poi)
        self.instrument_values = paths