from typing import List, Optional

from pydantic import BaseModel

from models.behavior import OutMessage


class Transition(BaseModel):
    pre_state: str
    post_state: str
    message_in: str
    messages_out: List[OutMessage]
    return_value: Optional[str]


class IOautomat(BaseModel):
    states: List[str]
    transitions: List[Transition]
