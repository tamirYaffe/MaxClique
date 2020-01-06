import time
import random
from mcts import mcts
from copy import deepcopy
import networkx as nx
import matplotlib.pyplot as plt

G = nx.Graph()
mcts = mcts(timeLimit=0.03)


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
    for i in range(0, 60):
        G.add_node(i)
    make_clique(G, [0, 2, 5, 14, 17, 18, 19, 36, 30, 25, 55, 57, 49])
    make_clique(G, [1, 3, 4, 6, 10, 13, 20, 22, 25, 34, 37, 38, 39, 52, 58])
    make_clique(G, [1, 43, 4, 6, 30, 53, 56])
    make_clique(G, [3, 5, 6, 17, 50, 51])
    make_clique(G, [2, 11, 55, 17, 29, 12, 57])
    G.add_edge(0, 16)
    G.add_edge(13, 15)
    G.add_edge(13, 12)
    G.add_edge(20, 22)
    G.add_edge(40, 21)
    G.add_edge(44, 26)
    G.add_edge(54, 37)
    G.add_edge(41, 23)
    G.add_edge(35, 22)
    G.add_edge(13, 1)
    G.add_edge(3, 59)
    G.add_edge(1, 2)
    G.add_edge(4, 36)
    G.add_edge(41, 23)
    G.add_edge(5, 12)
    G.add_edge(6, 34)
    G.add_edge(7, 15)
    G.add_edge(7, 8)
    G.add_edge(9, 30)
    G.add_edge(10, 46)
    G.add_edge(10, 11)
    G.add_edge(24, 31)
    G.add_edge(27, 31)
    G.add_edge(28, 11)
    G.add_edge(29, 32)
    G.add_edge(42, 33)
    G.add_edge(48, 33)
    G.add_edge(42, 45)
    G.add_edge(47, 45)
    G.add_edge(49, 45)
    G.add_edge(24, 7)
    G.add_edge(26, 7)
    G.add_edge(26, 24)
    G.add_edge(47, 16)
    G.add_edge(59, 33)
    G.add_edge(45, 21)
    G.add_edge(41, 19)


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
    draw_graph(G, state.clique_set)
    print(state)


def draw_graph(graph, solution={}):
    # pos = {}
    nodes_labels = {}
    for node in graph.nodes:
        #     pos[node] = (int(node / 5), node % 5)
        nodes_labels[node] = node
    pos = nx.circular_layout(graph)
    nx.draw_networkx_nodes(graph, pos, nodelist=graph.nodes, node_size=250)
    nx.draw_networkx_edges(graph, pos, edgelist=graph.edges, alpha=1, width=2)
    nx.draw_networkx_labels(graph, pos, nodes_labels, font_size=10)
    nx.draw_networkx_nodes(graph, pos, nodelist=solution, node_size=250, node_color='#FF0000')
    plt.show()


if __name__ == "__main__":
    create_graph()
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
