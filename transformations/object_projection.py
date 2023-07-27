from typing import Dict, List

from models import Interaction


class ObjectProjection:
    """Takes the result of XMLToTable as input and creates a dict, which, for each
    involved object and each scenario, contains the interaction this object is concerned
    with.

    Parameters
    ----------
    interactions : List[Interaction]
        The XMLToTable output
    """

    def __init__(self, interactions: Dict[str, List[Interaction]]):
        self._interactions = interactions

        self._projection: Dict[str, Dict[str, List[Interaction]]] = {}

    def _get_objects(self) -> List[str]:
        senders = [i.sender for o in self._interactions.values() for i in o]
        receivers = [i.receiver for o in self._interactions.values() for i in o]
        objects = list(set(senders + receivers))
        objects.remove("user")
        return objects

    def transform(self) -> Dict[str, Dict[str, List[Interaction]]]:
        objects = self._get_objects()
        for obj in objects:
            scenarios = {}
            for scenario, inters in self._interactions.items():
                interactions = []
                for interaction in inters:
                    if obj in [interaction.sender, interaction.receiver]:
                        interactions.append(interaction)
                scenarios[scenario] = interactions
            self._projection[obj] = scenarios

        return self._projection
