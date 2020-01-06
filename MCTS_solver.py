import time
import random
from mcts import mcts
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

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
        G.add_node(100 + i)
        G.add_node(200 + i)
    make_clique(G, [0, 2, 5, 14, 17, 18, 19, 116, 110, 105, 215, 217, 209])
    make_clique(G, [1, 3, 4, 6, 10, 13, 100, 102, 105, 114, 117, 118, 119, 212, 218])
    make_clique(G, [1, 203, 4, 6, 110, 213, 216])
    make_clique(G, [3, 5, 6, 17, 210, 211, 217])
    make_clique(G, [2, 11, 215, 17, 109, 217])
    G.add_edge(0, 16)
    G.add_edge(13, 15)
    G.add_edge(13, 12)
    G.add_edge(100, 102)
    G.add_edge(200, 101)
    G.add_edge(204, 106)
    G.add_edge(214, 117)
    G.add_edge(201, 103)
    G.add_edge(115, 102)
    G.add_edge(13, 1)
    G.add_edge(3, 219)
    G.add_edge(1, 2)
    G.add_edge(4, 116)
    G.add_edge(201, 103)
    G.add_edge(5, 12)
    G.add_edge(6, 114)
    G.add_edge(7, 15)
    G.add_edge(7, 8)
    G.add_edge(9, 110)
    G.add_edge(10, 206)
    G.add_edge(10, 11)
    G.add_edge(104, 111)
    G.add_edge(107, 111)
    G.add_edge(108, 11)
    G.add_edge(109, 112)
    G.add_edge(202, 113)
    G.add_edge(208, 113)
    G.add_edge(202, 205)
    G.add_edge(207, 205)
    G.add_edge(209, 205)
    G.add_edge(104, 7)
    G.add_edge(106, 7)
    G.add_edge(106, 104)
    G.add_edge(207, 16)
    G.add_edge(219, 113)
    G.add_edge(205, 101)
    G.add_edge(201, 19)


def generate_random_graph(number_of_vertices=20, edges_probability=0.8):
    global G
    G = nx.Graph()
    for i in range(0, number_of_vertices):
        G.add_node(i)
    for i in range(0, number_of_vertices):
        for j in range(0, number_of_vertices):
            if random.random() < edges_probability:
                G.add_edge(i, j)


def main():
    # generate_random_graph(50, 0.08)
    state = CliqueState()
    while not state.isTerminal():
        best_action = mcts.search(initialState=state)
        state = state.takeAction(best_action)
    draw_graph(G)
    print(state)


def draw_graph(graph):
    # pos = {}
    nodes_labels = {}
    for node in graph.nodes:
        #     pos[node] = (int(node / 5), node % 5)
        nodes_labels[node] = node
    pos = nx.spring_layout(graph)
    nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes, node_size=250)
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges, alpha=1, width=2)
    nx.draw_networkx_labels(graph, pos, nodes_labels, font_size=10)
    plt.show()


if __name__ == "__main__":
    create_graph()
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
