from typing import Dict, List, Optional

from models.behavior import Behavior
from models.io_automata import IOautomat
from models.uml2 import StateMachine, Transition, State, StateTypeEnum, TransitionTypeEnum
from plantuml import PlantUML
from os.path import abspath

class IO2UML:
    def __init__(self, input: IOautomat):
        self.io_automat = input
        self.state_machine = self._io_2_uml()
        self.plantUML_server =  PlantUML(url='http://www.plantuml.com/plantuml/img/')

    def _io_2_uml(self):
        iostates = self.io_automat.states
        iotransitions = self.io_automat.transitions
        states = []
        for s in iostates:
            states.append(State(
                label=s,
                type = StateTypeEnum.simple
            ))
        transitions = []
        for t in iotransitions:
            action = t.message_in

            composite_state = State(
                label=action,
                type=StateTypeEnum.composite
            )
            if not composite_state in states:
                states.append(composite_state)

            transitions.append(Transition(
                pre_state=t.pre_state,
                post_state=action,
                type=TransitionTypeEnum.action,
                action=action,
                return_value=None
            ))

            transitions.append(Transition(
                pre_state=action,
                post_state=t.post_state,
                type=TransitionTypeEnum.ret,
                action="",
                return_value=t.return_value
            ))

        return StateMachine(
            states=states,
            transitions=transitions
        )

    def get_state(self, state_label):
        return ([state for state in self.state_machine.states if state.label == state_label])[0]

    def generate_plant_uml(self):
        plant_uml = "@startuml\n"
        for state in self.state_machine.states:
            if state.type == StateTypeEnum.simple:
                plant_uml += f"rectangle {state.label}\n"
            else:
                plant_uml += f"hexagon {state.label}\n"
        for transition in self.state_machine.transitions:
            arrow = "-->" if self.get_state(transition.pre_state).type == StateTypeEnum.simple else "+-->"
            plant_uml += f"{transition.pre_state} {arrow} {transition.post_state} : {transition.action} / {transition.return_value}\n"
        plant_uml += "@enduml"
        return plant_uml

    def visualize_uml(self):
        uml_text = self.generate_plant_uml()
        output_path = "artefacts/state_machine.uml"
        with open(output_path, "w") as file:
            file.write(uml_text)
        self.plantUML_server.processes_file(output_path)