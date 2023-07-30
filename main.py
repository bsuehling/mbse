import os
import sys

from transformations import *

if __name__ == "__main__":
    input_file = "./input/MDD_Model.xml"
    artifacts = "artifacts"
    os.makedirs(artifacts, exist_ok=True)
    interaction_table = XMLToTable(input_file).transform()
    projection = ObjectProjection(interaction_table).transform()
    behaviors = BehaviorExtraction(projection).transform()
    io_automata = GenerateIOAutomata(behaviors).io_automata()

    with open(os.path.join(artifacts, "behavior.txt"), "w") as file:
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

    with open(os.path.join(artifacts, "io_automata.txt"), "w") as file:
        original_stdout = sys.stdout
        sys.stdout = file
        for obj, automaton in io_automata.items():
            print(f"{obj}:")
            print(f"states: {automaton.states}")
            for t in automaton.transitions:
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
    for obj, automaton in io_automata.items():
        io_automata_viz(automaton, f"artifacts/{obj}_io_automaton.png")
