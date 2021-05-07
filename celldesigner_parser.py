import xml.etree.ElementTree as ET
import logging
import sbgn_structures
from collections import deque


class CellDesignerParser:
    xml_namespace = '{http://www.sbml.org/sbml/level2/version4}'
    xml_namespace_celldesigner = '{http://www.sbml.org/2001/ns/celldesigner}'

    generate_warnings = True

    def __init__(self, celldesigner_filename):
        self.filename = celldesigner_filename
        self.process_list = []
        self.species_dict = dict()
        self.residues_dict = dict()
        self.compartments_dict = dict()
        self.parse_tree()

    def parse_reaction(self, reaction_node):
        reactants = []
        products = []

        attributes = reaction_node.attrib
        id_attribute = attributes["id"]

        base_reactant_nodes = reaction_node.findall(".//{}baseReactant".format(self.xml_namespace_celldesigner))
        for base_reactant_node in base_reactant_nodes:
            base_reactant_species = self.species_dict[base_reactant_node.attrib["species"]]
            reactants.append(base_reactant_species)

        base_product_nodes = reaction_node.findall(".//{}baseProduct".format(self.xml_namespace_celldesigner))
        for base_product_node in base_product_nodes:
            base_product_species = self.species_dict[base_product_node.attrib["species"]]
            products.append(base_product_species)

        reactant_links_nodes = reaction_node.findall(".//{0}listOfReactantLinks/{0}reactantLink"
                                                     .format(self.xml_namespace_celldesigner))
        product_links_nodes = reaction_node.findall(".//{0}listOfProductLinks/{0}productLink"
                                                    .format(self.xml_namespace_celldesigner))
        for reactant_node in reactant_links_nodes:
            reactant_species = self.species_dict[reactant_node.attrib["reactant"]]
            reactants.append(reactant_species)

        for product_node in product_links_nodes:
            product_species = self.species_dict[product_node.attrib["product"]]
            products.append(product_species)

        process = sbgn_structures.Transition(id_attribute)
        for reactant in reactants:
            process.add_reactant(reactant)
        for product in products:
            process.add_product(product)

        self.process_list.append(process)

    def parse_species(self, species_node, queue=None):
        attributes = species_node.attrib
        name = attributes["name"]
        id_attribute = attributes["id"]

        # Using dict.get() here to avoid missing key exception
        #   Compartment is not always specified ( for example for proteins inside a complex )
        compartment_id = attributes.get("compartment")
        compartment = self.compartments_dict.get(compartment_id)

        species_type = species_node.find(".//{}class".format(self.xml_namespace_celldesigner)).text

        species = sbgn_structures.Species(name, id_attribute, species_type, compartment)

        state_modification_nodes = species_node.findall(".//{0}state/{0}listOfModifications/{0}modification"
                                                        .format(self.xml_namespace_celldesigner))
        for state_modification_node in state_modification_nodes:
            smn_attributes = state_modification_node.attrib
            res_id = smn_attributes["residue"]
            res_state = smn_attributes["state"]
            species.add_or_update_residue(res_id, None, res_state)

        complex_species_node = species_node.find(".//{0}complexSpecies".format(self.xml_namespace_celldesigner))
        # Process complex parents later, as all species might not have been processed yet.
        if complex_species_node is not None and queue is not None:
            parent_id = complex_species_node.text
            queued = (parent_id, species)
            queue.append(queued)

        self.species_dict[id_attribute] = species

    def parse_protein(self, protein_node):
        attributes = protein_node.attrib
        species_lst = []
        for species in self.species_dict.values():
            if species.name == attributes["name"]:
                species_lst.append(species)

        residue_nodes = protein_node.findall(".//{0}listOfModificationResidues/{0}modificationResidue"
                                             .format(self.xml_namespace_celldesigner))
        for residue_node in residue_nodes:
            residue_attributes = residue_node.attrib
            res_id = residue_attributes["id"]
            res_name = residue_attributes.get("name")
            for species in species_lst:
                species.add_or_update_residue(res_id, res_name)

    def parse_compartment(self, compartment_node):
        attributes = compartment_node.attrib
        # Name attribute does not have to be present, using "default" instead
        self.compartments_dict[attributes["id"]] = attributes.get("name", "default")

    def parse_tree(self):
        tree = ET.parse(self.filename)

        # Find all compartments, species, and reactions nodes.
        compartment_nodes = tree.findall(".//{0}listOfCompartments/{0}compartment".format(self.xml_namespace))
        species_nodes = tree.findall(".//{0}listOfSpecies/{0}species".format(self.xml_namespace))
        reactions_nodes = tree.findall(".//{0}listOfReactions/{0}reaction".format(self.xml_namespace))

        protein_nodes = tree.findall(".//{0}annotation//{1}listOfProteins/{1}protein"
                                     .format(self.xml_namespace,
                                             self.xml_namespace_celldesigner))
        included_species_nodes = tree.findall(".//{0}annotation//{1}listOfIncludedSpecies/{1}species"
                                              .format(self.xml_namespace,
                                                      self.xml_namespace_celldesigner))

        if self.generate_warnings:
            if not compartment_nodes:
                logging.warning("No compartments found in file {}\n".format(self.filename))
            if not species_nodes:
                logging.warning("No species found in file {}\n".format(self.filename))
            if not reactions_nodes:
                logging.warning("No reactions found in file {}\n".format(self.filename))

        for compartment_node in compartment_nodes:
            self.parse_compartment(compartment_node)

        # Extract required information about species
        for species_node in species_nodes:
            self.parse_species(species_node)

        # using a queue here because CellDesigner included species are not necessarily ordered
        #   children can appear before parents, and thus cannot be assigned to their parent right away
        queue = deque()
        for species_node in included_species_nodes:
            self.parse_species(species_node, queue)

        # now we assign species to their complexes
        while queue:
            parent_id, species = queue.pop()
            self.species_dict[parent_id].add_complex_component(species)

        # parse proteins and reactions
        for protein_node in protein_nodes:
            self.parse_protein(protein_node)

        for reaction_node in reactions_nodes:
            self.parse_reaction(reaction_node)
