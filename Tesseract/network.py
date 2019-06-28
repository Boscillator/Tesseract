import uuid
import networkx as nx
from typing import Callable, Any, TypeVar, Generic, Optional, Dict, List

MessageType = TypeVar('MessageType')


def simulate_network(G: nx.DiGraph,
                     activate: Callable[[Dict[str, Any]], Optional[MessageType]],
                     translate: Callable[[MessageType, Dict[str, Any]], Optional[MessageType]],
                     activations: List[str],
                     log: Callable[[str, MessageType], None]):
    """
    Simulate a single round a spontaneous activations on network G.
    :param G: A directed graph where vertices are user ids. User parameters as specified as vertex data.
    :param activate: A function to be called when a user spontaneously posts.
                    Takes a user nodes parameters as a argument.
    :param translate: A function that takes an event, and returns how a user responds to it. Also takes user parameters.
    :param activations: A list of the user ids to spontaneously activate at the start of the simulation.
    :param log: A function to be called whenever a user posts. Takes the user's id and the message being sent
    """

    # queue is a list of pairs (neighbor_user_id, message).
    # Events that need to be processed by neighbors are stored here.
    queue = []

    # Activate the users
    for user in activations:
        e = activate(G.nodes[user])

        if e is None:
            continue

        log(user, e)

        # Queue the events for processing by neighbors
        for neighbor in G.neighbors(user):
            queue.append((neighbor, e))

    # Until we have finished processing all events
    while len(queue) > 0:
        user, message = queue.pop(0)

        # Give neighbor chance to react
        e = translate(message, G.nodes[user])

        if e is None:
            continue

        log(user, e)

        # Queue all the neighbor's neighbors to process the new event
        for neighbor in G.neighbors(user):
            queue.append((neighbor, e))
