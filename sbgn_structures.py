class Residue:
    def __init__(self, new_id, new_name=None, new_state=None):
        self.id = new_id
        self.state = new_state
        self.name = new_name


class Species:
    def __init__(self, new_name, new_id, new_type, new_compartment):
        self.name = new_name
        self.id = new_id
        self.type = new_type
        self.compartment = new_compartment
        self.composition = []
        self.residues = []

    def add_or_update_residue(self, residue_id, residue_name=None, residue_state=None):
        for residue in self.residues:
            if residue.id == residue_id:
                residue.name = residue_name
                residue.state = residue_state
                return

        residue = Residue(residue_id, residue_name, residue_state)
        self.residues.append(residue)

    def add_complex_component(self, component):
        self.composition.append(component)


class Transition:
    def __init__(self, new_id, reactants=None, products=None):
        if reactants is None:
            reactants = []
        if products is None:
            products = []
        self.id = new_id
        self.reactants = reactants
        self.products = products

    def add_reactant(self, reactant):
        self.reactants.append(reactant)

    def add_product(self, product):
        self.products.append(product)
