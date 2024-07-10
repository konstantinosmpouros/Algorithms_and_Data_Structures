import math


class BurstViterbi:

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
        # Initialize the cost table
        self.C = self.init_cost_table()
        # Calculate the g parameter, needed to calculate the lambdas
        self.g = self.T / self.n
        # Calculate the labda parameters, one for each state
        self.lambdas = self.lambdas()

        # Initialize the table for the optimal path and the position
        self.P = [[0] * (self.n + 1) for _ in range(self.K)]
        self.p_min = 0

        # Run the algorithm
        self.viterbi()

    def calculate_intervals(self):
        """
        A method that calculates the intervals between successive emissions of the 'times' data.

        :return: An n-1 array that contains the intervals, where n is the length of the 'times' array.
        """
        return [self.times[i] - self.times[i - 1] for i in range(1, len(self.times))]

    def init_cost_table(self):
        """
        A method that initialize the cost table we will need to change the state.

        :return: An n*k array where all values are inf except the [0, 0].
         N is the number of intervals and K the number of states
        """
        C = [[math.inf for _ in range(self.K)] for _ in range(self.n + 1)]
        C[0][0] = 0
        return C

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

    def extra_cost(self, j, l):
        """
        A method that will calculate the extra cost when changing states.

        :param j: First state.
        :param l: Moving state
        :return: 0 in case we are downgrading state, the extra cost if we are upgrading.
        """
        return self.gamma * (l - j) * math.log(self.n) if j < l else 0

    def exponential_distr(self, s, t):
        """
        A method that implements the f𝑖(x) = 𝜆𝑖 * 𝑒^(−𝜆𝑖𝑥) and calculates the exponential probability density.

        :param s: The lambda value position of the state in the lambdas list.
        :param t: The interval position value in the intervals list.
        :return: The exponential probability density of the specific state.
        """
        return self.lambdas[s] * math.exp(-self.lambdas[s] * self.intervals[t])

    def viterbi(self):
        for t in range(1, self.n + 1):
            for s in range(self.K):
                lmin = 0
                cmin = self.C[t - 1][0] + self.extra_cost(0, s)

                for l in range(1, self.K):
                    c = self.C[t - 1][l] + self.extra_cost(l, s)
                    if c < cmin:
                        cmin = c
                        lmin = l

                # Calculate the ln𝑓𝑗(𝑥𝑡) and check if its 0 then the distance tends to be infinite.
                expo_dist = self.exponential_distr(s, t-1)
                if expo_dist == 0:
                    new_dist = math.inf
                else:
                    new_dist = cmin - math.log(expo_dist)

                self.C[t][s] = round(new_dist, 2)
                self.P[s][:t] = self.P[lmin][:t]
                self.P[s][t] = s

        cmin = self.C[self.n][0]
        for s in range(1, self.K):
            if self.C[self.n][s] < cmin:
                cmin = self.C[self.n][s]
                self.p_min = s

    def time_state_seq(self, optimal_path):
        """
        A method that will print out the state that the system is in the period of time we have.

        :param optimal_path: The optimal state path Viterbi calculated.
        """
        # Count the every sequence of the system state
        sequences = []
        prev_value = optimal_path[0]
        count = 1

        for i in range(1, len(optimal_path)):
            if optimal_path[i] == prev_value:
                count += 1
            else:
                sequences.append([prev_value, count])
                prev_value = optimal_path[i]
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

    def results(self, d):
        """
        A method that prints the results of the algorithm according to the parameter d.
        Because this is the BurstViterbi algo,
        the d parameter determines whether to show the cost table and the optimal path.

        :param d: The d parameter from the args that defines the output.
        """
        optimal_path = self.P[self.p_min]
        if d:
            # Print the Cost table
            for row in self.C:
                print(row)

            # Print the optimal states in a sequence
            print(len(optimal_path), optimal_path)

            # Print the optimal states according to successive emissions
            self.time_state_seq(optimal_path)
        else:
            # Print the optimal states according to successive emissions
            self.time_state_seq(optimal_path)
