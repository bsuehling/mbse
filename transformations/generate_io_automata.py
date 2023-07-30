from typing import Dict, List

from plantuml import PlantUML

from models.behavior import Behavior
from models.io_automata import IOautomat, OutMessage, Transition


class GenerateIOAutomata:
    def __init__(self, input: Dict[str, Dict[str, Behavior]], initial_states):
        self._input = input
        self.initial_states = initial_states
        self.plantUML_server = PlantUML(url="http://www.plantuml.com/plantuml/img/")

    def io_automata(self):
        _io_automata: Dict[str, IOautomat] = {}
        for obj, behaviors in self._input.items():
            _states: set[str] = set()
            _transitions: List[Transition] = []
            for _, behavior in behaviors.items():
                for behavior_block in behavior:
                    _states.add(behavior_block.pre_state)
                    _states.add(behavior_block.post_state)
                    _transitions.append(
                        Transition(
                            pre_state=behavior_block.pre_state,
                            post_state=behavior_block.post_state,
                            message_in=behavior_block.message_in,
                            messages_out=behavior_block.messages_out,
                            return_value=behavior_block.return_value,
                        )
                    )
            _io_automata.update(
                {obj: IOautomat(states=list(_states), transitions=_transitions)}
            )
        _io_automata_final: Dict[str, IOautomat] = {}
        for obj, automat in _io_automata.items():
            _states = automat.states
            _transitions = automat.transitions
            _changed = True
            while _changed and len(_transitions) > 1:
                _changed = False
                head = _transitions[0]
                _transitions = _transitions[1:]
                for i in range(len(_transitions)):
                    t = _transitions[i]
                    if (
                        head.pre_state == t.pre_state
                        and head.post_state == t.post_state
                        and head.message_in == t.message_in
                        and head.return_value == t.return_value
                    ):
                        _transitions[i].messages_out += head.messages_out
                        _changed = True
                        break
                if not _changed:
                    _transitions = [head] + _transitions
            # Remove duplicate OutMessages
            for transition in _transitions:
                transition.messages_out = [
                    item
                    for idx, item in enumerate(transition.messages_out)
                    if item not in transition.messages_out[:idx]
                ]
            _io_automata_final.update(
                {obj: IOautomat(states=_states, transitions=_transitions)}
            )
        return _io_automata_final

    def generate_plant_uml(self, automaton, initial_states):
        plant_uml = "@startuml\n"
        plant_uml += "circle entry\n"

        for state in automaton.states:
            plant_uml += f"rectangle {state}\n"

        for initial_state in initial_states:
            plant_uml += f"entry -> {initial_state}\n"

        for transition in automaton.transitions:
            plant_uml += f"{transition.pre_state} --> {transition.post_state} : {transition.message_in} / "
            for message_out in transition.messages_out:
                plant_uml += f"\\n <{message_out.operation}, {message_out.receiver}, {message_out.return_value if message_out.return_value is not None else 'void'}> "
            plant_uml += f" {transition.return_value if transition.return_value is not None else 'void'} \n"

        plant_uml += "@enduml"

        return plant_uml

    def visualize(self, filepath):
        automata = self.io_automata()
        for object, automaton in automata.items():
            uml_text = self.generate_plant_uml(automaton, self.initial_states[object])
            output_path = f"{filepath}/io_automaton_{object}.uml"
            with open(output_path, "w") as file:
                file.write(uml_text)
            self.plantUML_server.processes_file(output_path)