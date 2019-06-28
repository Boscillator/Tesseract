import pytest
import networkx as nx
from Tesseract import simulate_network


def zero(_):
    return 0


def increment(x, _):
    return x + 1


@pytest.fixture
def two_node_network():
    G = nx.DiGraph()
    G.add_edge('a', 'b')
    return G


@pytest.fixture
def complex_network():
    G = nx.DiGraph()
    G.add_edge('0', '1')
    G.add_edge('0', '2')
    G.add_edge('2', '3')
    G.add_edge('3', '4')
    G.add_edge('3', '5')
    return G


def test_simulate_simple_network(two_node_network):
    events = []

    def log(user_id, e):
        events.append(e)

    simulate_network(two_node_network, zero, increment, ['a'], log)

    assert events == [0, 1]


def test_simulate_complex_network(complex_network):
    events = []

    def log(user_id, e):
        events.append(e)

    simulate_network(complex_network, zero, increment, ['0'], log)

    assert events == [0, 1, 1, 2, 3, 3]
