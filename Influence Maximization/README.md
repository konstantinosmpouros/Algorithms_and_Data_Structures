# Influence Maximization Program

## Purpose

The Influence Maximization Program is designed to measure and maximize the influence that can be exerted within a social network by certain key members. This project is based on the concept of influence maximization, which has garnered significant interest from researchers due to its practical applications in fields such as viral marketing, information dissemination, and social media strategies.

The core objective of this program is to identify a set of nodes in a graph (representing the social network) that, when activated, can maximize the spread of influence across the network. The program implements well-known algorithms in the field, such as the Greedy and Max Degree algorithms, to solve this optimization problem effectively. In the greedy approach, the process is stochastic and nodes are activated based on some probability rather than deterministically, so in order to specify the specific nodes that maximise influence, we use Monte Carlo simulation.


## How to run

The program can be executed with the following command:


 python influence_maximization.py [-r RANDOM_SEED] graph k {greedy,max_degree} probability mc

- **Graph File Input (graph):** The program must take a graph file as input. Some files that already have a structured directional graph are the Barabasi-Albert, Watts-Strogatz and Erdos-Renyi models.
- **Seed Selection (k) :** The number of nodes that will be activated initially to perform the maximisation search. The user defines how many nodes to activate in the beginning and the algorithm will search k nodes to maximise the influence.
- **Algorithm Choice:** Users can choose between the Greedy algorithm and the Max Degree algorithm for influence maximization.
- **Influence Probability (probability):** Configurable probability value that determines the likelihood of influence spread between connected nodes.
- **Monte Carlo Simulations (mc):** Supports multiple iterations of Monte Carlo simulations to provide an accurate estimate of the spread of the influence.
- **Random Seed (-r):** Optional, random seed parameter to ensure reproducibility of results.


## Examples
```sh
python influence_maximization.py erdos_renyi.txt 10 max_degree 0.1 1000 -r 42
```

```sh
python influence_maximization.py erdos_renyi.txt 10 greedy 0.1 1000 -r 42
```

```sh
python influence_maximization.py barabasi_albert.txt 10 max_degree 0.1 1000 -r 42
```

```sh
python influence_maximization.py barabasi_albert.txt 10 greedy 0.1 1000 -r 42
```

```sh
python influence_maximization.py watts_strogatz.txt 10 max_degree 0.1 1000 -r 42
```

```sh
python influence_maximization.py watts_strogatz.txt 10 greedy 0.1 1000 -r 42
```