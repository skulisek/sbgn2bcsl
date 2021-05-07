from translation import Translator
from celldesigner_parser import CellDesignerParser

cp = CellDesignerParser("Curation_Interferon-lambda-pathway_IFN-lambda_stable.xml")
tsr = Translator()

rules_list = []
for process in cp.process_list:
    rule = tsr.sbgn_transition_to_bcsl_rule(process)
    rules_list.append(rule)

for rule in rules_list:
    print(rule)
