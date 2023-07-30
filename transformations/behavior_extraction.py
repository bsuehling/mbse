from typing import Dict, List

from models import Behavior, BehaviorBlock, Interaction, OutMessage


class BehaviorExtraction:
    """Takes the result of ObjectProjection as input and creates a dict, which, for each
    involved object and each scenario, contains the behavior of the object based on the
    pre-state and the incoming message.

    Parameters
    ----------
    interactions : List[Interaction]
        The ObjectProjection output
    """

    def __init__(self, input: Dict[str, Dict[str, List[Interaction]]]):
        
        self._input = input

        self._behaviors: Dict[str, Dict[str, Behavior]] = {}

    def transform(self) -> Dict[str, Dict[str, Behavior]]:
        for obj, scenarios in self._input.items():
            behaviors = {}
            for scenario, interactions in scenarios.items():
                behavior: Behavior = []
                behavior_block = None
                for interaction in interactions:
                    if interaction.receiver == obj:
                        if behavior_block is not None:
                            behavior.append(behavior_block)
                        behavior_block = BehaviorBlock(
                            pre_state=interaction.pre_state_rcv,
                            message_in=interaction.operation,
                            messages_out=[],
                            return_value=interaction.return_value,
                            post_state=interaction.post_state_rcv,
                        )
                    else:
                        behavior_block.messages_out.append(
                            OutMessage(
                                operation=interaction.operation,
                                receiver=interaction.receiver,
                                return_value=interaction.return_value,
                            )
                        )
                behavior.append(behavior_block)
                behaviors[scenario] = behavior
            self._behaviors[obj] = behaviors
        
        return self._behaviors
