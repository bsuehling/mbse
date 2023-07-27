from transformations import *

if __name__ == "__main__":
    input_file = "./input/MDD_Model.xml"
    interaction_table = XMLToTable(input_file).transform()
    projection = ObjectProjection(interaction_table).transform()
    behaviors = BehaviorExtraction(projection).transform()

    for obj, behavior in behaviors.items():
        print(f"{obj}:")
        for scenario, behavior in behavior.items():
            print(f"\t{scenario}:")
            for behavior_block in behavior:
                print(f"\t\t{behavior_block}")
        print("-" * 100)
