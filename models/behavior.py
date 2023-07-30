from typing import List, Optional

from pydantic import BaseModel


class OutMessage(BaseModel):
    operation: str
    receiver: str
    return_value: Optional[str]

    def __eq__(self, other):
        return self.operation == other.operation and \
            self.receiver == other.receiver and self.return_value == other.return_value

class BehaviorBlock(BaseModel):
    pre_state: str
    message_in: str
    messages_out: List[OutMessage]
    return_value: Optional[str]
    post_state: str


Behavior = List[BehaviorBlock]
