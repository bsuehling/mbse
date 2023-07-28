from typing import Dict, List

from models.behavior import Behavior
from models.io_automata import OutMessage, Transition, IOautomat



class GenerateIOAutomata:
    # input Dict[obj, Dict[scenario, Behavior]]
    def __init__(self, input: Dict[str, Dict[str, Behavior]]):
        self._input = input
        

    def io_automata(self):
        _io_automata: Dict[str, IOautomat] = {}
        for obj, behaviors in self._input.items():
            _states: set[str] = set()
            _transitions: List[Transition] = []
            for _ , behavior in behaviors.items():
                for behavior_block in behavior:
                    _states.add(behavior_block.pre_state)
                    _states.add(behavior_block.post_state)
                    _transitions.append(Transition(
                        pre_state=behavior_block.pre_state,
                        post_state=behavior_block.post_state,
                        message_in=behavior_block.message_in,
                        messages_out=behavior_block.messages_out,
                        return_value=behavior_block.return_value
                    ))
            _io_automata.update({obj: IOautomat(
                states = list(_states),
                transitions = _transitions
            )})
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
                    if head.pre_state == t.pre_state and head.post_state == t.post_state and head.message_in == t.message_in and head.return_value == t.return_value:
                        _transitions[i].messages_out += head.messages_out
                        _changed = True
                        break
                if not _changed:
                    _transitions = [head] + _transitions
            _io_automata_final.update({obj: IOautomat(
                states=_states,
                transitions=_transitions
            )})
        return _io_automata_final
