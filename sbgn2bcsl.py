from translation import Translator
from celldesigner_parser import CellDesignerParser
from argparse import ArgumentParser

arg_parser = ArgumentParser(prog='sbgn2bcsl',
                            description='Tool for converting CellDesigner 4.4.2 diagrams to BCSL',
                            usage='%(prog)s path [options]')

arg_parser.add_argument('Path',
                        metavar='path',
                        type=str,
                        help='The path to the CellDesigner 4.4.2 diagram SBML file')
arg_parser.add_argument('Out_path',
                        metavar='out_path',
                        type=str,
                        help='The path to the file where the BCSL result will be saved')
arg_parser.add_argument('-q',
                        '--quiet',
                        action='store_true',
                        help='Disable the generation of warning messages.')
arg_parser.add_argument('-c',
                        '--unpack-complexes',
                        action='store_true',
                        help='Enable the unpacking of top-level complexes.')
arg_parser.add_argument('-C',
                        '--unpack-nested-complexes',
                        action='store_true',
                        help='Enable the unpacking of nested complexes.')
arg_parser.add_argument('-i',
                        '--include-positive-influences',
                        action='store_true',
                        help='Include positive influences on both sides of the rule.')
arg_parser.add_argument('-w',
                        '--replace-spaces',
                        action='store_true',
                        help='Replace whitespaces in names with an underscore.')

args = arg_parser.parse_args()
input_path = args.Path
output_path = args.Out_path
unpack_complexes = args.unpack_complexes
unpack_nested = args.unpack_nested_complexes
include_influences = args.include_positive_influences
quiet = args.quiet
replace_spaces = args.replace_spaces

if unpack_nested:
    unpack_complexes = True

cp = CellDesignerParser(input_path)
cp.generate_warnings = not quiet
cp.parse_tree()

tsr = Translator()
tsr.unpack_complexes = unpack_complexes
tsr.unpack_nested_complexes = unpack_nested
tsr.generate_warnings = not quiet
tsr.include_positive_influences = include_influences
tsr.replace_spaces = replace_spaces

rules_list = []
for process in cp.process_list:
    rule = tsr.sbgn_transition_to_bcsl_rule(process)
    rules_list.append(rule)

out_file = open(output_path, "w")
for rule in rules_list:
    out_file.write(rule.__str__())
    out_file.write('\n')
out_file.close()
