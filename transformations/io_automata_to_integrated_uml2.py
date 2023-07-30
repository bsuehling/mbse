from typing import Dict, List, Optional

from models.behavior import Behavior
from models.io_automata import IOautomat
from models.uml2 import *
from plantuml import PlantUML
from os.path import abspath

class IO2UML:
    def __init__(self, obj, input: IOautomat):
        self.io_automat = input
        self.obj = obj
        self.state_machine = self._io_2_state_machine()
        self.composite_state_state_machines = self._io_to_composite_state_state_machines()
        self.plantUML_server =  PlantUML(url='http://www.plantuml.com/plantuml/img/')

    def _io_incoming_messages(self, state):
        return set([transition.message_in for transition in self.io_automat.transitions if transition.pre_state == state])

    def _io_transitions_with_incoming_message(self, state, in_message):
        return [transition for transition in self.io_automat.transitions if transition.message_in == in_message and transition.pre_state == state]

    def _io_to_composite_state_state_machines(self) -> List[CompositeStateStateMachine]:
        io_states = self.io_automat.states
        io_transitions = self.io_automat.transitions
        state_machines = []
        for state in io_states:
            for action in self._io_incoming_messages(state):
                io_similar_transitions = self._io_transitions_with_incoming_message(state, action)
                state_machine_label = action
                state_machine_parent = state
                blocks = []
                block_transitions = []
                if len(io_similar_transitions) == 1:
                    transition= io_similar_transitions[0]
                    operations = "" # TODO: Try to extract a function for this
                    for message_out in transition.messages_out:
                        operations += f"{message_out.receiver}_{message_out.operation}_"
                    blocks.append(Block(
                        label = f"do_{operations}",
                        is_input = True,
                        output_ids = [1]
                    ))
                else:
                    # We assume that the check only happens (if ever) in the first message-out
                    # TODO: We assumed that the first message_outs in "similar" transitions have the same operation and receiver
                    # TODO: We also assumed that when there are similar transitions, then there is at least one outgoing message
                    first_message = io_similar_transitions[0].messages_out[0]
                    check = f"check_{first_message.receiver}_{first_message.operation}"
                    initial_block = Block(
                        label = f"do_{check}",
                        is_input = True,
                        output_ids = []
                    )
                    blocks.append(initial_block)
                    output_counter = 1
                    for similar_transition in io_similar_transitions:
                        operations = ""
                        for message_out in similar_transition.messages_out[1:]:
                            operations += f"{message_out.receiver}_{message_out.operation}_"
                        intermediate_block = Block(
                            label = f"do_{operations}",
                            is_input = False,
                            output_ids = [output_counter]
                        )
                        output_counter += 1
                        block_transitions.append(BlockTransition(
                            from_block = initial_block,
                            to_block = intermediate_block,
                            check = f"[check_{similar_transition.messages_out[0].return_value}]"
                        ))
                        blocks.append(intermediate_block)
                state_machines.append(CompositeStateStateMachine(
                    label = state_machine_label,
                    parent = state_machine_parent,
                    blocks = blocks,
                    transitions = block_transitions
                ))
        return state_machines

    def _io_2_state_machine(self):
        iostates = self.io_automat.states
        iotransitions = self.io_automat.transitions
        states = []
        for state in iostates:
            states.append(SimpleState(label = state))
        transitions = []
        for transition in iotransitions:
            action = transition.message_in

            composite_state = CompositeState(label=action, parent=transition.pre_state)
            #if not composite_state in states:
            #    states.append(composite_state)

            states.append(composite_state)

            transitions.append(Transition(
                pre_state=transition.pre_state,
                post_state=action,
                type=TransitionTypeEnum.action,
                action=action,
                return_value=None
            ))

            transitions.append(Transition(
                pre_state=action,
                post_state=transition.post_state,
                type=TransitionTypeEnum.ret,
                action="",
                return_value=transition.return_value
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
            print(transition.pre_state)
            # print(self.state_machine.states)
            print(([state for state in self.state_machine.states if state.label == transition.pre_state]))
            arrow = "-->" if self.get_state(transition.pre_state).type == StateTypeEnum.simple else "+-->"
            return_value = transition.return_value if transition.return_value is not None \
                else "return void" if transition.action == "" else ""
            plant_uml += f"{transition.pre_state} {arrow} {transition.post_state} : {transition.action} / {return_value}\n"
        plant_uml += "@enduml"
        return plant_uml

    def visualize_uml(self):
        uml_text = self.generate_plant_uml()
        output_path = f"artefacts/{self.obj}_state_machine.uml" # TODO: Change this for different components
        with open(output_path, "w") as file:
            file.write(uml_text)
        self.plantUML_server.processes_file(output_path)

    def generate_composite_plant_uml(self, machine):
        plant_uml = "@startuml\n"
        plant_uml += f'state {machine.label} {{\n'
        plant_uml += "state entry <<entryPoint>>\n"
        for block in machine.blocks:
            plant_uml += f'state {block.label}\n'
            if len(block.output_ids) == 1: # We assume that a state doesn't return more than one value
                plant_uml += f"state exit{block.output_ids[0]} <<exitPoint>>\n"
                plant_uml += f'{block.label} -> exit{block.output_ids[0]}\n'
            if block.is_input:
                plant_uml += f'entry -> {block.label}\n'
        plant_uml += "}\n"
        for transition in machine.transitions:
            plant_uml += f'{transition.from_block.label} --> {transition.to_block.label} : {transition.check}\n'
        plant_uml += "@enduml"
        print(plant_uml)
        return plant_uml

    def visualize_composite_state_state_machines(self):
        state_machines = self.composite_state_state_machines
        for idx, machine in enumerate(state_machines):
            uml_text = self.generate_composite_plant_uml(machine)
            output_path = f"artefacts/{self.obj}_{machine.parent}_{machine.label}.uml"
            with open(output_path, "w") as file:
                file.write(uml_text)
            self.plantUML_server.processes_file(output_path)