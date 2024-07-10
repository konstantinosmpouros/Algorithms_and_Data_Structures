import argparse
import random
from collections import deque


def specify_args():
    """

    Parse command line arguments for the Influence Maximization Program.

    :return: An object containing parsed arguments.
    """
    parser = argparse.ArgumentParser(description="Influence Maximization Program")

    # Optional argument for random seed
    parser.add_argument('-r', '--random_seed',
                        type=int,
                        help="The seed for the random number generator")

    # Mandatory positional arguments
    parser.add_argument('graph',
                        type=str,
                        choices=['barabasi_albert.txt', 'watts_strogatz.txt', 'erdos_renyi.txt',
                                 r'.\barabasi_albert.txt', r'.\watts_strogatz.txt', r'.\erdos_renyi.txt'],
                        help="The file with the graph links")

    parser.add_argument('k',
                        type=int,
                        help="The number of nodes to be selected as seeds")
    parser.add_argument('algorithm',
                        choices=['greedy', 'max_degree'],
                        help="Algorithm to use (greedy or max_degree)")
    parser.add_argument('probability',
                        type=float,
                        help="Probability with which a node is influenced by a neighbor")
    parser.add_argument('mc',
                        type=int,
                        help="Number of iterations in the Monte Carlo method")

    args = parser.parse_args()

    return args


def read_file(filename):
    """

    A function that takes a file name containing a graph and returns the adjacency table and a list of nodes.

    :param filename: The file name that contains the graph.
    :return: The adjacency table, a list with the nodes.
    """
    try:
        # Open the file in read mode
        with open(filename, 'r') as file:
            # Determine the number of nodes
            num_nodes = int(file.readlines()[-1].split()[0]) + 1

            # Initialize an empty adjacency matrix (num_nodes x num_nodes)
            adjacency_matrix = [[0] * num_nodes for _ in range(num_nodes)]

            # Reset the file cursor to the beginning
            file.seek(0)

            for line in file:
                # Split the 2 numbers
                node1, node2 = map(int, line.split())
                adjacency_matrix[node1][node2] = 1

            return adjacency_matrix

    except ValueError:
        print("Error: The file contains non-numeric values.")
        exit(0)


def find_connections(adj_table, node):
    """

    Finds and returns the nodes connected to a given node.

    :param adj_table: The adjacency matrix.
    :param node: The node that we want to find its connections.
    :return: A list with the connected nodes.
    """
    connections = []
    for i, connected in enumerate(adj_table[node]):
        if connected == 1:
            connections.append(i)
    return connections


def influence_score(adj_table, seeds, p, mc):
    """

    Computes the influence score of a set of seed nodes using the Independent Cascade Model
    with Monte Carlo simulations.

    :param adj_table: The adjacency matrix of the graph.
    :param seeds: List of integers representing the seed nodes which are initially active.
    :param p: The probability with which an active node can activate its neighbors.
    :param mc: The number of Monte Carlo simulations to run.
    :return: The average number of nodes that become active after the Monte Carlo simulation.
    """
    # The score of the simulation
    scores = 0
    for _ in range(mc):
        # Initialize a list that will show for every node if it is active or not
        is_active = [False for _ in range(len(adj_table))]

        # Create a FIFO queue to store the active nodes that we haven't visited yet
        active_nodes = deque()
        active_nodes += seeds

        # Make these initial nodes that we will start with, active
        for seed in seeds:
            is_active[seed] = True

        # For every node in the active nodes that we haven't visited, visit it and try to influence its connections
        while active_nodes:
            # Extract the first node and find its connections
            first_node = active_nodes.popleft()
            connections = find_connections(adj_table, first_node)

            # Try to influence each one of its connections if they are not active and according to the p
            for con in connections:
                if not is_active[con] and random.random() < p:
                    is_active[con] = True
                    active_nodes.appendleft(con)

        # Sum the score of this simulation
        scores += sum(is_active)

    # Return the average score from all simulations
    return scores / mc


def seeds_max_degree(adj_table, k):
    """

    A method that takes the adjacency matrix and return the top k nodes that have the most connections.

    :param adj_table: A table with all the connections between the nodes.
    :param k: The number of seeds that we will pick.
    :return: A list with the nodes id that we will use as starting seeds.
    """
    # Sum the numbers of outer connections each node has
    out_degrees = [sum(row) for row in adj_table]

    # Create a list of tuples (value, index)
    indexed_lst = list(enumerate(out_degrees))

    # Sort the list by value in descending order
    indexed_lst.sort(key=lambda x: x[1], reverse=True)

    # Extract the indices of the top k values
    top_k = indexed_lst[:k]
    seeds = [index for index, value in top_k]

    return seeds


def seeds_greedy(adj_table, k, p, mc):
    """

    A functions the select k nodes in a graph using a greedy approach upon which node maximize the influence score.

    :param adj_table: The adjacency matrix of the graph.
    :param k: The number of seed nodes to select.
    :param p: The probability with which an active node can activate its neighbors.
    :param mc: The number of Monte Carlo simulations to run.
    :return: A list with the chosen nodes that maximize the influence score, and a list with the scores.
    """
    # Initialize the 2 list we will return
    seeds, infl = [], []

    # A list with all the nodes
    all_nodes = [_ for _ in range(len(adj_table))]

    # While the seeds we have chosen are less than k, continue the greedy search
    for _ in range(k):
        # V, is a list that contain all the nodes except those that has already been appended in the 'seeds' list
        V = [node for node in all_nodes if node not in seeds]

        # Initialize a list that we will store the influence scores for every node in V
        scores = []

        # For every node in V, calculate the influence score that would have if we append it to the 'seeds' list
        for node in V:
            trial_seeds = seeds + [node]
            scores.append(influence_score(adj_table, trial_seeds, p, mc))

        # Find the index of the node that had the best score
        best_node = scores.index(max(scores))

        # Append the node and the score to each list
        seeds.append(best_node)
        infl.append(scores[best_node])

    return seeds, infl


if __name__ == "__main__":
    # Specify the args
    args = specify_args()

    # Initialize a variable for each arg
    rd_seed, filename, algo = args.random_seed, args.graph, args.algorithm
    k, p, mc = args.k, args.probability, args.mc

    # Create the adjacency matrix from the file given
    adj_table = read_file(filename)

    # Set the random seed
    if rd_seed is not None:
        random.seed(rd_seed)

    # Run the appropriate algorithm according to the args
    if algo == 'max_degree':
        # Find the k seeds according to the max out degree method and calculate the influence scores
        seeds = seeds_max_degree(adj_table, k)
        influ_scores = [influence_score(adj_table, seeds[:i], p, mc) for i in range(1, len(seeds) + 1)]

    else:
        # Find the k seeds according to the greedy method that maximize the influence score
        seeds, influ_scores = seeds_greedy(adj_table, k, p, mc)

    print(seeds)
    print(influ_scores)

