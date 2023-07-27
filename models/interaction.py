from typing import Optional

from pydantic import BaseModel


class Interaction(BaseModel):
    pre_state_rcv: Optional[str] = None
    sender: Optional[str] = None
    operation: str = ""
    receiver: Optional[str] = None
    return_value: Optional[str] = None
    post_state_rcv: Optional[str] = None
