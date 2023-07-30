from transformations import *
from transformations.generate_io_automata import GenerateIOAutomata
from transformations.io_automata_to_integrated_uml2 import IO2UML
import os
import sys

if __name__ == "__main__":
    input_file = "./input/MDD_Model.xml"
    artefacts = "artefacts"
    if not os.path.exists(artefacts):
        os.makedirs(artefacts)
    interaction_table = XMLToTable(input_file).transform()
    projection = ObjectProjection(interaction_table).transform()
    behaviors = BehaviorExtraction(projection).transform()
    io_automata = GenerateIOAutomata(behaviors).io_automata()
    uml = IO2UML("atm", io_automata["atm"])
    for s in uml.state_machine.states:
        print(f"\t{s}")
    for t in uml.state_machine.transitions:
        print(f"\t{t}")
    uml.visualize_uml()
    uml.visualize_composite_state_state_machines()

