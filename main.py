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

    '''
    with open(os.path.join(artefacts, "behavior.txt"), "w") as file:
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

    with open(os.path.join(artefacts, "io_automata.txt"), "w") as file:
        original_stdout = sys.stdout
        sys.stdout = file
        for obj, automat in io_automata.items():
            print(f"{obj}:")
            print(f"states: {automat.states}")
            for t in automat.transitions:
                print(f"\tpre_state: {t.pre_state}")
                print(f"\tpost_state: {t.post_state}")
                print(f"\tmessage_in: {t.message_in}")
                print(f"\treturn_value: {t.return_value}")
                for out in t.messages_out:
                    print(f"\t\t{out}")
            print()
            print("-" * 100)
        sys.stdout = original_stdout

    from visualization import io_automata_viz
    
    # visualize
    for obj, automat in io_automata.items():
        io_automata_viz(automat, f"artefacts/{obj}_io_automat.png")
    '''

    uml = IO2UML(io_automata["atm"]).io_2_uml()
    print(uml)
    from visualization import uml_viz
    print(uml_viz(uml, f"artefacts/atm_uml.png"))
    
