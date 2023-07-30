from typing import List, Optional, Dict, Tuple

from pydantic import BaseModel

from enum import Enum

class StateTypeEnum(str, Enum):
    simple = 'simple'
    composite = 'composite'

class TransitionTypeEnum(str, Enum):
    action = 'action'
    ret = 'return'

class State(BaseModel):
    label: str
    type: StateTypeEnum

    def __eq__(self, other):
        return self.label == other.label and self.type == other.type
    
class Transition(BaseModel):
    pre_state: str
    post_state: str
    type: TransitionTypeEnum
    action: str
    return_value: Optional[str]

class StateMachine(BaseModel):
    states: List[State]
    transitions: List[Transition]