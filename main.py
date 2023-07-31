import os
import sys
from typing import Dict, List

from transformations import *
from transformations.generate_io_automata import GenerateIOAutomata
from transformations.io_automata_to_integrated_uml import IO2UML


def get_initial_states(behaviors) -> Dict[str, List[str]]:
    initial_states: Dict[str, List[str]] = {}

    for obj, scenario in behaviors.items():
        init = []
        for _, beh in scenario.items():
            init.append(beh[0].pre_state)
            break  # very hacky work around, the assumption is wrong
        initial_states.update({obj: list(set(init))})

    return initial_states


if __name__ == "__main__":
    input_file = "./input/MDD_Model.xml"
    uml_artefacts_folder = "artefacts/uml"
    io_automata_artefacts_folder = "artefacts/io_automata"

    if not os.path.exists(uml_artefacts_folder):
        os.makedirs(uml_artefacts_folder, exist_ok=True)
    if not os.path.exists(io_automata_artefacts_folder):
        os.makedirs(io_automata_artefacts_folder, exist_ok=True)

    interaction_table = XMLToTable(input_file).transform()
    projection = ObjectProjection(interaction_table).transform()
    behaviors = BehaviorExtraction(projection).transform()

    with open(os.path.join("artefacts", "behavior.txt"), "w") as file:
        original_stdout = sys.stdout
        sys.stdout = file
        for obj, behavior in behaviors.items():
            print(f"{obj}:")
            for scenario, behavior in behavior.items():
                print(f"\t{scenario}:")
                for behavior_block in behavior:
                    print(f"\t\t{behavior_block}")
            print("-" * 100)
        sys.stdout = original_stdout


    initial_states = get_initial_states(behaviors)

    io_automata_transformation = GenerateIOAutomata(behaviors, initial_states)
    io_automata = io_automata_transformation.io_automata()
    io_automata_transformation.visualize(io_automata_artefacts_folder)

    for obj, automat in io_automata.items():
        uml = IO2UML(obj, io_automata[obj], initial_states[obj])
        os.makedirs(f"{uml_artefacts_folder}/{obj}", exist_ok=True)
        uml.visualize_uml(f"{uml_artefacts_folder}/{obj}")
        uml.visualize_composite_state_state_machines(f"{uml_artefacts_folder}/{obj}")
