from typing import List, Optional, Dict, Tuple

from pydantic import BaseModel

from enum import Enum

from abc import ABC

class StateTypeEnum(str, Enum):
    simple = 'simple'
    composite = 'composite'

class TransitionTypeEnum(str, Enum):
    action = 'action'
    ret = 'return'

class State(BaseModel, ABC):
    label: str
    type: StateTypeEnum

    def __eq__(self, other):
        return self.label == other.label and self.type == other.type

class SimpleState(State):
    type: StateTypeEnum = StateTypeEnum.simple

    def __eq__(self, other):
        return super.__eq__(self, other)

class CompositeState(State):
    type: StateTypeEnum = StateTypeEnum.composite
    parent: str

    def __eq__(self, other):
        if other.type != self.type:
            return False
        return super.__eq__(self, other) and self.parent == other.parent

class Transition(BaseModel):
    pre_state: str
    post_state: str
    type: TransitionTypeEnum
    action: str
    return_value: Optional[str]
    exit_id: Optional[int]

    def __eq__(self, other):
        return self.pre_state == other.pre_state and self.post_state == other.post_state \
            and self.type == other.type and self.action == other.action and self.return_value == other.return_value \
            and self.exit_id == other.exit_id 

class StateMachine(BaseModel):
    states: List[State]
    transitions: List[Transition]

class BlockLabelElement(BaseModel):
    operation: str
    receiver: str

class BlockLabel(BaseModel):
    is_check: bool
    elems: List[BlockLabelElement]
    
class Block(BaseModel):
    label: BlockLabel
    is_input: bool
    output_ids: List[int]

class BlockTransition(BaseModel):
    from_block: Block
    to_block: Block
    check: str

class CompositeStateStateMachine(BaseModel):
    label: str
    parent: str
    blocks: List[Block]
    transitions: List[BlockTransition]

class IntegratedUML(BaseModel):
    state_machine: StateMachine
    composite_states: List[CompositeStateStateMachine]