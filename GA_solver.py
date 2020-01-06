import random
import time

from deap import base
from deap import creator
from deap import tools

import networkx as nx
import matplotlib.pyplot as plt

toolbox = base.Toolbox()

G = nx.Graph()


# the goal ('fitness') function to be maximized
def is_connected_to_all(node, clique):
    for other_node in clique:
        if not G.has_edge(node, other_node):
            return False
    return True


def evalOneMax(individual):
    node = 0
    clique_dict = {0: []}
    clique_next_index = 1
    for attr in individual:
        belong_to_clique = False
        if attr:
            for clique_num in range(0, clique_next_index):
                if is_connected_to_all(node, clique_dict[clique_num]):
                    clique_dict[clique_num].append(node)
                    belong_to_clique = True
            if not belong_to_clique:
                clique_dict[clique_next_index] = [node]
                clique_next_index = clique_next_index + 1
        node = node + 1
    max_clique_size = 0
    for clique_num in range(0, clique_next_index):
        if len(clique_dict[clique_num]) > max_clique_size:
            max_clique_size = len(clique_dict[clique_num])
    return max_clique_size * 10 - (sum(individual) - max_clique_size),


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
    # draw_graph(G)


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
    solset = set()
    for i in range(0, len(solution)):
        if solution[i] == 1:
            solset.add(i)
    nx.draw_networkx_nodes(graph, pos, nodelist=solset, node_size=250, node_color='#FF0000')
    plt.show()


def create_model():
    creator.create("FitnessMax", base.Fitness, weights=(1.0,))
    creator.create("Individual", list, fitness=creator.FitnessMax)

    # Attribute generator
    #                      define 'attr_bool' to be an attribute ('gene')
    #                      which corresponds to integers sampled uniformly
    #                      from the range [0,1] (i.e. 0 or 1 with equal
    #                      probability)
    toolbox.register("attr_bool", random.randint, 0, 1)

    # Structure initializers
    #                         define 'individual' to be an individual
    #                         consisting of 100 'attr_bool' elements ('genes')
    toolbox.register("individual", tools.initRepeat, creator.Individual,
                     toolbox.attr_bool, len(G.nodes))

    # define the population to be a list of individuals
    toolbox.register("population", tools.initRepeat, list, toolbox.individual)

    # ----------
    # Operator registration
    # ----------
    # register the goal / fitness function
    toolbox.register("evaluate", evalOneMax)

    # register the crossover operator
    toolbox.register("mate", tools.cxTwoPoint)

    # register a mutation operator with a probability to
    # flip each attribute/gene of 0.05
    toolbox.register("mutate", tools.mutFlipBit, indpb=0.05)

    # operator for selecting individuals for breeding the next
    # generation: each individual of the current generation
    # is replaced by the 'fittest' (best) of three individuals
    # drawn randomly from the current generation.
    toolbox.register("select", tools.selTournament, tournsize=3)


def main():
    create_graph()
    create_model()
    random.seed(64)

    # create an initial population of 300 individuals (where
    # each individual is a list of integers)
    pop = toolbox.population(n=100)
    generations = 50

    # CXPB  is the probability with which two individuals
    #       are crossed
    #
    # MUTPB is the probability for mutating an individual
    CXPB, MUTPB = 0.5, 0.2

    print("Start of evolution")

    # Evaluate the entire population
    fitnesses = list(map(toolbox.evaluate, pop))
    for ind, fit in zip(pop, fitnesses):
        ind.fitness.values = fit

    print("  Evaluated %i individuals" % len(pop))

    # Extracting all the fitnesses of
    fits = [ind.fitness.values[0] for ind in pop]

    # Variable keeping track of the number of generations
    g = 0

    # Begin the evolution
    while g < generations:
        # A new generation
        g = g + 1
        print("-- Generation %i --" % g)

        # Select the next generation individuals
        offspring = toolbox.select(pop, len(pop))
        # Clone the selected individuals
        offspring = list(map(toolbox.clone, offspring))

        # Apply crossover and mutation on the offspring
        for child1, child2 in zip(offspring[::2], offspring[1::2]):

            # cross two individuals with probability CXPB
            if random.random() < CXPB:
                toolbox.mate(child1, child2)

                # fitness values of the children
                # must be recalculated later
                del child1.fitness.values
                del child2.fitness.values

        for mutant in offspring:

            # mutate an individual with probability MUTPB
            if random.random() < MUTPB:
                toolbox.mutate(mutant)
                del mutant.fitness.values

        # Evaluate the individuals with an invalid fitness
        invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
        fitnesses = map(toolbox.evaluate, invalid_ind)
        for ind, fit in zip(invalid_ind, fitnesses):
            ind.fitness.values = fit

        print("  Evaluated %i individuals" % len(invalid_ind))

        # The population is entirely replaced by the offspring
        pop[:] = offspring

        # Gather all the fitnesses in one list and print the stats
        fits = [ind.fitness.values[0] for ind in pop]

        length = len(pop)
        mean = sum(fits) / length
        sum2 = sum(x * x for x in fits)
        std = abs(sum2 / length - mean ** 2) ** 0.5

        print("  Min %s" % min(fits))
        print("  Max %s" % max(fits))
        print("  Avg %s" % mean)
        print("  Std %s" % std)

    print("-- End of (successful) evolution --")

    best_ind = tools.selBest(pop, 1)[0]
    print("Best individual is %s, %s" % (best_ind, best_ind.fitness.values))
    draw_graph(G, best_ind)


if __name__ == "__main__":
    start_time = time.time()
    main()
    print("--- %s seconds ---" % (time.time() - start_time))
