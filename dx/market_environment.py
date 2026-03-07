
class market_environment(object):
    ''' Modélise un environnement de marché pour évaluation

    Attributs
    =========
    name : string
        nom de l'environnement
    pricing_date : datetime object 
        date de valorisation

    Méthodes
    ========
    add_constant : 
        ajoute une constante (un paramètre du modèle)
    get_constant :
        relit la valeur d'une constante
    add_list :
        ajoute une liste (un sous-jacent)
    get_list :
        relit une liste
    add_curve :
        ajoute une courbe de marché (ex. courbe des taux)
    get_curve :
        relit une courbe de marché
    add_environment :
        ajoute et met à jour tout l'environnement avec des constantes, 
        des listes et des courbes 
    '''

    def __init__(self, name, pricing_date):
        self.name = name
        self.pricing_date = pricing_date
        self.constants = {}
        self.lists = {}
        self.curves = {}

    def add_constant(self, key, constant):
        self.constants[key] = constant

    def get_constant(self, key):
        return self.constants[key]

    def add_list(self, key, list_object):
        self.lists[key] = list_object

    def get_list(self, key):
        return self.lists[key]

    def add_curve(self, key, curve):
        self.curves[key] = curve

    def get_curve(self, key):
        return self.curves[key]

    def add_environment(self, env):
        # Ecrase toute valeur déjà présente 
        self.constants.update(env.constants)
        self.lists.update(env.lists)
        self.curves.update(env.curves)