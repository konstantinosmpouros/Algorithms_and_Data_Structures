# We create an object class Cluster that will have a list inside with all the number it contains in order to make easier the merge.
class Cluster:
    # Initialize method (Constructor)
    def __init__(self, x: list):
        self.clusters = x

    # Find the min distance between 2 clusters
    def single_cluster_distance(self, cluster2):
        # Just a simple search for the min distance between 2 clusters integers.
        min_dist = 99999
        for x in self.clusters:
            for y in cluster2.clusters:
                if abs(x - y) < min_dist:
                    min_dist = abs(x - y)
        return min_dist

    # Find the max distance between 2 clusters
    def complete_cluster_distance(self, cluster2):
        # Just a simple search for the max distance between 2 clusters integers.
        max_dist = 0
        for x in self.clusters:
            for y in cluster2.clusters:
                if abs(x - y) > max_dist:
                    max_dist = abs(x - y)
        return max_dist

    # Find the avg distance between 2 clusters
    def average_cluster_distance(self, cluster2):
        # Just a simple search for the avg distance between 2 clusters integers.
        total = 0
        counter = 0
        for x in self.clusters:
            for y in cluster2.clusters:
                total += abs(x - y)
                counter += 1
        return total / counter

