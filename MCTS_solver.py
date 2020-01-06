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
    make_clique(G, [0, 2, 5, 14, 17, 18, 19])
    make_clique(G, [1, 3, 4, 6, 10, 13])
    make_clique(G, [3, 5, 6, 17])
    G.add_edge(0, 16)
    G.add_edge(13, 15)
    G.add_edge(13, 12)


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
    generate_random_graph(50, 0.08)
    draw_graph(G)
    # state = CliqueState()
    # while not state.isTerminal():
    #     best_action = mcts.search(initialState=state)
    #     state = state.takeAction(best_action)
    # print(state)


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
