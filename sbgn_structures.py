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
                if residue_name is not None:
                    residue.name = residue_name
                if residue_state is not None:
                    residue.state = residue_state
                return

        residue = Residue(residue_id, residue_name, residue_state)
        self.residues.append(residue)

    def add_complex_component(self, component):
        self.composition.append(component)


class Transition:
    def __init__(self, new_id, reversible=False, reactants=None, products=None, modifiers=None):
        if reactants is None:
            reactants = []
        if products is None:
            products = []
        if modifiers is None:
            modifiers = []
        self.id = new_id
        self.reactants = reactants
        self.products = products
        self.modifiers = modifiers
        self.reversible = reversible

    def add_reactant(self, reactant):
        self.reactants.append(reactant)

    def add_product(self, product):
        self.products.append(product)

    def add_modifier(self, modifier):
        self.modifiers.append(modifier)
