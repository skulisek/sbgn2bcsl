<h1>sbgn2bcsl</h1>
The sbgn2bcsl tool is a CLI tool written in python 3 that converts <a href=http://celldesigner.org/>CellDesigner<a/> models into 
<a href=https://journals.plos.org/plosone/article?id=10.1371/journal.pone.0238838>BioChemical Space Language<a/> rules conforming to the 
<a href=https://www.fi.muni.cz/~xtrojak/files/papers/eBCSgen_tutorial.pdf>eBCSgen</a> definition of the "rule" term.
<ln/>

<h3>Usage Instructions</h3>

    $python sbgn2bcsl --help
    usage: sbgn2bcsl path out_path [options]

    Tool for converting CellDesigner 4.4.2 diagrams to BCSL

    positional arguments:
      path                  The path to the CellDesigner 4.4.2 diagram SBML file
      out_path              The path to the file where the BCSL result will be
                            saved

    optional arguments:
      -h, --help            show this help message and exit
      -q, --quiet           Disable the generation of warning messages.
      -c, --unpack-complexes
                            Enable the unpacking of top-level complexes.
      -C, --unpack-nested-complexes
                            Enable the unpacking of nested complexes.
      -i, --include-positive-influences
                            Include positive influences on both sides of the rule.
      -w, --replace-non-word-chars
                            Replace whitespaces in names with an underscore.
      -r, --rates           Include artificial rates to the output rules.
