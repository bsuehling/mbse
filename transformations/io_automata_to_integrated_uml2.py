from typing import Dict, List, Optional

from models.behavior import Behavior
from models.io_automata import IOautomat
from models.uml2 import StateMachine, Transition, State, StateTypeEnum, TransitionTypeEnum

class IO2UML:
    # input Dict[obj, Dict[scenario, Behavior]]
    def __init__(self, input: IOautomat):
        self._input = input
        
    def io_2_uml(self):
        _io_states = self._input.states
        _io_transitions = self._input.transitions
        _states = []
        for s in _io_states:
            _states.append(State(
                label=s,
                type = StateTypeEnum.simple
            ))
        _transitions = []
        for t in _io_transitions:
            action = t.message_in

            _states.append(State(
                label=action,
                type=StateTypeEnum.composite
            ))

            _transitions.append(Transition(
                pre_state=t.pre_state,
                post_state=action,
                type=TransitionTypeEnum.action,
                action=action,
                return_value=None
            ))

            _transitions.append(Transition(
                pre_state=action,
                post_state=t.post_state,
                type=TransitionTypeEnum.ret,
                action="",
                return_value=t.return_value
            ))
        return StateMachine(
            states=_states,
            transitions=_transitions
        )

                

            
                
                
            

