import math


class Bellman_Ford:

    def __init__(self, times, s, gamma):
        # Initialize the parameters needed (List with times and intervals along with s and gamma params from user)
        self.times = times
        self.intervals = self.calculate_intervals()
        self.s = s
        self.gamma = gamma

        # Calculate extra parameters needed
        # Initialize total period time
        self.T = sum(self.intervals)
        # Initialize the number of intervals which is the number of times - 1
        self.n = len(self.intervals)
        # Calculate the number of states our system should have
        self.K = self.calculate_k(min(self.intervals))
        # Calculate the g parameter, needed to calculate the lambdas
        self.g = self.T / self.n
        # Calculate the labda parameters, one for each state
        self.lambdas = self.lambdas()

        # Initialize the graph, the list with the links and the optimal path.
        self.V = [(t, i) for t in range(self.n + 1) for i in range(self.K)]
        self.E = []
        self.path = []

        # The list that will store all the relaxations of the Bellman_Ford.
        self.relaxation = []

        self.bellman_ford()

    def calculate_intervals(self):
        """
        A method that calculates the intervals between successive emissions of the 'times' data.

        :return: An n-1 array that contains the intervals, where n is the length of the 'times' array.
        """
        return [self.times[i] - self.times[i - 1] for i in range(1, len(self.times))]

    def calculate_k(self, min_interval):
        """
        A method that calculates the number of states our system should have,
        by taking the min interval of successive emissions and the s parameter user gave and the total Period.

        :param min_interval: The min interval value between the successive emissions.
        :return: The number of the states that our system will have.
        """
        return math.ceil(1 + math.log(self.T, self.s) + math.log(1 / min_interval, self.s))

    def lambdas(self):
        """
        Calculate the different lambdas for every state, according to the parameter s, g

        :return: An array with all the lambda values for every state.
        """
        return [math.pow(self.s, i) / self.g for i in range(self.K)]

    def extra_cost(self, i, j):
        """
        A method that will calculate the extra cost when changing states.

        :param i: First state.
        :param j: Moving state
        :return: 0 in case we are downgrading state, the extra cost if we are upgrading.
        """
        return self.gamma * (j - i) * math.log(self.n) if i < j else 0

    def exponential_distr(self, j, t):
        """
        A method that implements the f𝑖(x) = 𝜆𝑖 * 𝑒^(−𝜆𝑖𝑥) and calculates the exponential probability density.

        :param j: The lambda value position of the state in the lambdas list.
        :param t: The interval position value in the intervals list.
        :return: The exponential probability density of the specific state.
        """
        return self.lambdas[j] * math.exp(-self.lambdas[j] * self.intervals[t])

    def bellman_ford(self):
        # Calculate the weight to move from a state to another state. Append the states along with the weight in a list
        for t in range(self.n):
            for i in range(self.K):
                for j in range(self.K):

                    # Calculate extra cost to move from i to j and exponential distribution.
                    weight = self.extra_cost(i, j)
                    expo_dist = self.exponential_distr(j, t)

                    # If the expo_dist is 0, then the cost of moving from state i to state j in the next time is inf
                    if expo_dist == 0:
                        weight = math.inf
                    else:
                        weight -= math.log(expo_dist)

                    # Append the cost of moving from state i to state j in the next time in the list
                    self.E.append(((t, i), (t + 1, j), weight))

        # Initialize distance and predecessor lists to find the optimal path
        dist = {v: float('inf') for v in self.V}
        dist[(0, 0)] = 0
        preds = {v: None for v in self.V}

        # Update the dist tables. For every node, find the min cost and the predecessor.
        for _ in range(len(self.V) - 1):
            for (u, v, weight) in self.E:
                new_dist = dist[u] + weight
                if new_dist < dist[v]:
                    # A new relaxation occurred so add it to the relaxation list
                    self.relaxation.append((v, dist[v], new_dist, u, dist[u], weight))

                    # Update the tables
                    dist[v] = new_dist
                    preds[v] = u

        # The algorithm has calculated the optimal paths to reach every node.
        # Let's find the optimal path for the last time of the system
        # Initialize a list with all possible end nodes
        end_nodes = [(self.n, j) for j in range(self.K)]
        # Find the end node that the system was in the last time by finding the node with the smallest cost
        end_node = min(end_nodes, key=lambda x: dist[x])

        while end_node is not None:
            # Append the end note in the path and update the end node with its predecessor
            self.path.append(end_node[1])
            end_node = preds[end_node]

        # Reverse the sequence of the path because we were reading it from the end note to the start of the system
        self.path.reverse()

    def time_state_seq(self):
        """
        A method that will print out the state that the system is in the period of time we have.
        """
        # Count the every sequence of the system state
        sequences = []
        prev_value = self.path[0]
        count = 1

        for i in range(1, len(self.path)):
            if self.path[i] == prev_value:
                count += 1
            else:
                sequences.append([prev_value, count])
                prev_value = self.path[i]
                count = 1

        sequences.append([prev_value, count])

        # Print the corresponding time range that the system was in every state.
        sums = 0
        for seq in sequences:
            if sums == 0:
                print(f"{seq[0]} [{self.times[sums]}, {self.times[sums + seq[1] - 1]})")
                sums += seq[1] - 1
            else:
                print(f"{seq[0]} [{self.times[sums]}, {self.times[sums + seq[1]]})")
                sums += seq[1]

    def print_relaxations(self):
        """
        A method
        that will print out all the relaxations
        that the bellman ford algorithm does to each combination for states and times.
        The output values will be:
         Updating (time,state), old cost, -> new cost,
         from which predecessor (time,state) comes the new min cost,
         the cost to reach the predecessor, the transition cost and the emission cost.
        """
        for v, old_cost, new_cost, u, u_cost, weight in self.relaxation:
            # The cost of the previous state and time.
            emission_cost = -math.log(self.exponential_distr(v[1], v[0] - 1))

            # The cost associated with moving from one state to another state
            transition_cost = weight - emission_cost

            print(f"({v[0]}, {v[1]}) {old_cost:.2f} -> "
                  f"{new_cost:.2f} from ({u[0]}, {u[1]}) "
                  f"{u_cost:.2f} + {transition_cost:.2f} + {emission_cost:.2f}")

    def results(self, d):
        """
        A method that prints the results of the algorithm according to the parameter d.
        Because this is the BurstViterbi algo,
        the d parameter determines whether to show the cost table and the optimal path.

        :param d: The d parameter from the args that defines the output.
        """
        if d:
            # Print the relaxations.
            self.print_relaxations()

            # Print the optimal states in a sequence
            print(len(self.path), self.path)

            # Print the optimal states according to successive emissions
            self.time_state_seq()
        else:
            # Print the optimal states according to successive emissions
            self.time_state_seq()
