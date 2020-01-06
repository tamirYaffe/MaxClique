import time
from mcts import mcts
from copy import deepcopy
import networkx as nx

G = nx.Graph()
mcts = mcts(timeLimit=1)


def is_connected_to_all(node, clique):
    for other_node in clique:
        if not G.has_edge(node, other_node):
            return False
    return True


class CliqueState:
    def __init__(self):
        self.clique_set = set()

    def getPossibleActions(self):
        possibleActions = []
        for node in G.nodes:
            if node not in self.clique_set and is_connected_to_all(node, self.clique_set):
                possibleActions.append(node)
        return possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        newState.clique_set.add(action)
        return newState

    def isTerminal(self):
        for node in G.nodes:
            if node not in self.clique_set and is_connected_to_all(node, self.clique_set):
                return False
        return True

    def getReward(self):
        return len(self.clique_set)

    def __str__(self):
        return str(self.clique_set)


def make_clique(graph, nodes):
    for node in nodes:
        for other_node in nodes:
            if other_node == node or graph.has_edge(node, other_node):
                continue
            graph.add_edge(node, other_node)


def create_graph():
    global G
    G = nx.Graph()
    for i in range(0, 20):
        G.add_node(i)
    make_clique(G, [0, 2, 5, 14, 17, 18, 19])
    make_clique(G, [1, 3, 4, 6, 10, 13])
    make_clique(G, [3, 5, 6, 17])
    G.add_edge(0, 16)
    G.add_edge(13, 15)
    G.add_edge(13, 12)


def main():
    state = CliqueState()
    while not state.isTerminal():
        best_action = mcts.search(initialState=state)
        state = state.takeAction(best_action)
    print(state)


if __name__ == "__main__":
    create_graph()
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))