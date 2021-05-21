class AtomicAgent:
    def __init__(self, new_name, new_id, new_compartment, new_state=""):
        self.name = new_name
        self.id = new_id
        self.compartment = new_compartment
        self.state = new_state

    def __str__(self):
        if not self.state:
            out_str = "{0}{{_}}".format(self.name)
            return out_str
        out_str = "{0}{{{1}}}".format(self.name, self.state)
        return out_str


class StructureAgent:
    def __init__(self, new_name, new_id, new_compartment, composition=None):
        self.name = new_name
        self.id = new_id
        self.compartment = new_compartment
        self.composition = composition

    def __str__(self):
        if not self.composition:
            return "{0}()".format(self.name)

        composition_str = ", ".join(map(lambda m: m.__str__(), self.composition))
        out_str = "{0}({1})".format(self.name, composition_str)
        return out_str


class ComplexAgent:
    def __init__(self, new_name, new_id, new_compartment, composition=None):
        self.name = new_name
        self.id = new_id
        self.compartment = new_compartment
        self.composition = composition

    def __str__(self):
        assert(self.composition is not None)

        composition_str = ".".join(map(lambda m: m.__str__(), self.composition))
        out_str = "{0}".format(composition_str)
        return out_str


class Rule:
    def __init__(self, new_id, reactants=None, products=None, modifiers=None):
        self.id = new_id
        self.reactants = reactants
        self.products = products
        self.modifiers = modifiers

    def __str__(self, include_modifiers=False, include_artificial_rates=False):
        base_string = "{0}::{1}"

        reactants_str = " + ".join(map(lambda s: base_string.format(s.__str__(), s.compartment), self.reactants))
        products_str = " + ".join(map(lambda s: base_string.format(s.__str__(), s.compartment), self.products))
        modifiers_str = " + ".join(map(lambda s: base_string.format(s.__str__(), s.compartment), self.modifiers))

        if include_modifiers and self.modifiers:
            reactants_str += " + {0}".format(modifiers_str)
            products_str += " + {0}".format(modifiers_str)

        out_str = "{0} => {1}".format(reactants_str, products_str)
        if include_artificial_rates:
            out_str += " @ 1"
        return out_str
