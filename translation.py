import sbgn_structures
import logging
import bcsl_structures


def sbgn_residue_to_bcs_atomic_agent(residue):
    name = residue.name
    r_id = residue.id
    state = residue.state

    if name is None:
        name = r_id

    agent = bcsl_structures.AtomicAgent(name, r_id, None, state)
    return agent


class Translator:
    unpack_complexes = True
    unpack_nested_complexes = False
    generate_warnings = True

    to_atomic = ["ION", "SIMPLE_MOLECULE"]
    to_structure = ["DRUG", "UNKNOWN", "RNA", "DNA", "GENE", "PROTEIN"]
    to_complex = ["COMPLEX"]
    to_ignore = ["DEGRADED"]

    def sbgn_species_to_bcsl_agent(self, species):
        name = species.name
        s_id = species.id
        s_type = species.type
        compartment = species.compartment

        if s_type in self.to_ignore:
            return None

        if s_type in self.to_atomic:
            out_agent = bcsl_structures.AtomicAgent(name, s_id, compartment)
            return out_agent

        if s_type in self.to_structure:
            structure = []
            for residue in species.residues:
                tmp_residue = sbgn_residue_to_bcs_atomic_agent(residue)
                structure.append(tmp_residue)

            out_agent = bcsl_structures.StructureAgent(name, s_id, compartment, structure)
            return out_agent

        if s_type in self.to_complex:
            is_empty = species.composition == []

            # when not unpacking complexes, we must convert into BCSL Structure Agent with empty composition
            if not self.unpack_complexes or is_empty:
                if self.generate_warnings and not is_empty:
                    warning = "Turning Complex Species \"{0}\" into Structure Agents with empty structure " \
                              "leads to a loss of information".format(name)
                    logging.warning(warning)
                if self.generate_warnings and is_empty:
                    warning = "\"{0}\" is marked as Complex Species but has empty structure.\n" \
                              "Turning \"{0}\" into Structure Agent.".format(name)
                    logging.warning(warning)
                out_agent = bcsl_structures.StructureAgent(name, s_id, compartment)
                return out_agent

            # when unpacking complexes, we convert into BCSL Complex Agent
            #   but children must be BCSL Structure Agents
            if not self.unpack_nested_complexes:
                if self.generate_warnings:
                    warning = "Turning children of Complex Species \"{0}\" into Structure Agents" \
                              " with empty structure leads to a loss of information".format(name)
                    logging.warning(warning)

                tmp_unpack = self.unpack_complexes
                tmp_generate = self.generate_warnings
                self.unpack_complexes = False
                self.generate_warnings = False

                composition = []
                for child in species.composition:
                    tmp_child = self.sbgn_species_to_bcsl_agent(child)
                    if tmp_child is not None:
                        composition.append(tmp_child)

                self.unpack_complexes = tmp_unpack
                self.generate_warnings = tmp_generate

                out_agent = bcsl_structures.ComplexAgent(name, s_id, compartment, composition)
                return out_agent

        # When not recognised, transform into empty structure agent
        out_agent = bcsl_structures.StructureAgent(name, s_id, compartment)
        return out_agent

    def sbgn_transition_to_bcsl_rule(self, transition):
        reactants = []
        products = []
        for reactant in transition.reactants:
            tmp_reactant = self.sbgn_species_to_bcsl_agent(reactant)
            if tmp_reactant is not None:
                reactants.append(tmp_reactant)
        for product in transition.products:
            tmp_product = self.sbgn_species_to_bcsl_agent(product)
            if tmp_product is not None:
                products.append(tmp_product)

        rule = bcsl_structures.Rule(transition.id, reactants, products)
        return rule
