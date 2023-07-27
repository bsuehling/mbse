from os import PathLike
from typing import Dict, List
from xml.dom.minidom import Element, parse

from models import Interaction


class XMLToTable:
    """Takes a UML input specified as an XML file as input and converts it into a
    table, or rather, list of interactions for each scenario.

    Parameters
    ----------
    input : PathLike
        The XML file.
    """

    def __init__(self, input: PathLike):
        self._dom = parse(input)
        self._refs = self._build_ref_dict()
        self._interactions: Dict[str, List[Interaction]] = {}

        self._states: Dict[str, str] = {}
        self._sender = self._receiver = None
        self._return_queue: List[Interaction] = []
        self._last_rcv: Dict[str, Interaction] = {}

    def _build_ref_dict(self) -> Dict[str, Element]:
        return {
            e.getAttribute("xmi:id"): e for e in self._dom.getElementsByTagName("*")
        }

    def _get_covered_class(self, fragment: Element):
        lifeline = self._refs[fragment.getAttribute("covered")]
        return lifeline.getAttribute("name")

    def _message_occur_spec(self, fragment: Element):
        message = self._refs[fragment.getAttribute("message")]
        return message.getAttribute("name")

    def _has_return_value(self, fragment: Element):
        message = self._refs[fragment.getAttribute("message")]
        if message.getAttribute("messageSort") == "reply":
            return False
        operation = self._refs[message.getAttribute("signature")]
        descendants = operation.getElementsByTagName("ownedParameter")
        return len(descendants) > 0

    def _is_return_value(self, fragment: Element):
        message = self._refs[fragment.getAttribute("message")]
        if message.getAttribute("messageSort") == "reply":
            return True
        return False

    def _is_send_action(self, fragment: Element):
        return "MessageSend" in fragment.getAttribute("name")

    def _is_receive_action(self, fragment: Element):
        return "MessageRecv" in fragment.getAttribute("name")

    def transform(self):
        for scenario in self._dom.getElementsByTagName("packagedElement"):
            interactions = []
            if not scenario.getAttribute("xmi:type") == "uml:Interaction":
                continue
            for fragment in scenario.getElementsByTagName("fragment"):
                fragment_type = fragment.getAttribute("xmi:type")
                if fragment_type == "uml:StateInvariant":
                    state_class = self._get_covered_class(fragment)
                    self._states[state_class] = fragment.getAttribute("name")
                    last_rcv = self._last_rcv.pop(state_class, None)
                    if last_rcv is not None:
                        last_rcv.post_state_rcv = fragment.getAttribute("name")
                elif fragment_type == "uml:MessageOccurrenceSpecification":
                    message = self._message_occur_spec(fragment)
                    if self._is_send_action(fragment):
                        self._sender = self._get_covered_class(fragment)
                    elif self._is_receive_action(fragment):
                        self._receiver = self._get_covered_class(fragment)
                    if self._sender is not None and self._receiver is not None:
                        if self._is_return_value(fragment):
                            last_msg = self._return_queue.pop()
                            last_msg.return_value = message
                        else:
                            interaction = Interaction(
                                scenario=scenario.getAttribute("name"),
                                pre_state_rcv=self._states.get(self._receiver),
                                sender=self._sender,
                                operation=message,
                                receiver=self._receiver,
                            )
                            interactions.append(interaction)
                            self._last_rcv[self._receiver] = interaction
                            if self._has_return_value(fragment):
                                self._return_queue.append(interactions[-1])
                        self._sender = self._receiver = None
            self._interactions[scenario.getAttribute("name")] = interactions

        return self._interactions
