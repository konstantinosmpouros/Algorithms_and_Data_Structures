import sys
from Cluster import Cluster


# read the arguments from the command line.
def read_args():
    # check if the method, the file name and the number of the arguments given are correct
    try:
        if len(sys.argv) > 3:
            raise Exception('You have given more arguments than you should!')
        if len(sys.argv) < 3:
            raise Exception('You have given less arguments than you should!')
        if sys.argv[1] not in ['single', 'complete', 'average', 'ward']:
            raise Exception('The method you enter is not in the assignment!')
        if sys.argv[2] != 'example.txt':
            raise Exception('Wrong file name!')
    except Exception as e:
        print(e)
        exit(0)


# Read the example txt and create one cluster for every object we read and append them all in a list.
def create_all_cluster():
    try:
        # Try read the file and split every space to a new line
        with open(sys.argv[2], 'r') as file:
            file = file.readline().split()
            # Append all the number to a list so every number is a new row so its like we have a new cluster. One cluster per row
            all_clusters = []
            for number in file:
                all_clusters.append(Cluster([int(number)]))
            return all_clusters
    except Exception as e:
        print(e)
        exit(0)


# Lance and Williams method
def lance_williams(all_clusters):
    results = []    # A list with every merge we will do

    # Sort the clusters
    all_clusters.sort(key=lambda x: x.clusters)

    # Create a 2D array for all the possible distances. The size will be n*n that n is all the cluster we have
    # We give a very big value at the beginning and we will change it with the original value when we will calculate it. Quite like Dijkstra.
    distances = [[99999 for _ in range(0, len(all_clusters))] for _ in range(0, len(all_clusters))]

    # Calculate the first distances by taking the abs of the subtraction of all clusters integers.
    calculate_first_distances(all_clusters, distances)

    # Find the 2 closest clusters, pop and merge them, delete the popped cluster distances, calculate and insert the new distances and the new cluster.
    while len(all_clusters) > 1:
        # Find the 2 closest cluster that we can merge
        c1, c2 = closest_clusters(all_clusters, distances, results)

        # Merge those 2 clusters
        new_cluster = Cluster(all_clusters[c1].clusters + all_clusters[c2].clusters)
        new_cluster.clusters.sort(key=lambda x: x)

        s, t = all_clusters[c1], all_clusters[c2]   # The 2 cluster we merged in order to be more easy to understand.

        # According to the input method use the right method to calculate the distances with all the other clusters
        if sys.argv[1] == 'single':
            # Calculate single method distances
            new_distances = single_method(s, t, all_clusters, c1, c2)

        elif sys.argv[1] == 'complete':
            # Calculate complete method distances
            new_distances = complete_method(s, t, all_clusters, c1, c2)

        elif sys.argv[1] == 'average':
            # Calculate average method distances
            new_distances = average_method(s, t, all_clusters, c1, c2)
        else:
            # Calculate ward method distances
            new_distances = ward_method(s, t, all_clusters, distances, c1, c2)

        # Delete the old distances and the 2 clusters we merged
        insert_index = delete_clusters(c1, c2, distances, all_clusters)
        # Insert the new cluster and the new distances
        insert_cluster(new_cluster, all_clusters, new_distances, distances, insert_index)

    # Print the results
    for r in results:
        print(r)


# Perform the first distances calculation which is the |i-j|.
def calculate_first_distances(all_clusters: list, distances: list):
    # For every other cluster except itself. Calculate the abs of the subtraction
    for i in range(len(all_clusters)):
        for j in range(len(all_clusters)):
            if i != j:
                distances[i][j] = float(abs(all_clusters[i].clusters[0] - all_clusters[j].clusters[0]))


# Search for the 2 closest clusters to combine.
def closest_clusters(all_clusters: list, distances: list, results: list):
    # Searching for the first min distance in the distance table that we will find
    min_dist = distances[0][0]
    min_x = 0
    min_y = 0

    # just a simple searching for the first min value we can find
    for i in range(0, len(distances)):
        for j in range(0, len(distances[i])):
            if distances[i][j] < min_dist:
                min_dist = distances[i][j]
                min_x = i
                min_y = j

    # If the 2 indexes are equal that means that we have problem...
    # Maybe this will not happen very easy cause the distance for a cluster to itself is huge.
    if min_x == min_y:
        try:
            raise Exception('The algorithm says that you must merge a cluster with itself...')
        except Exception as e:
            print(e)
            exit(0)

    # Because the 2 closest cluster are those that we will merge we append the result to a list and in the end we just print the result list
    results.append(str(all_clusters[min_x].clusters) + " " +
                   str(all_clusters[min_y].clusters) + " " +
                   str(distances[min_x][min_y]) + " " +
                   str(len(all_clusters[min_x].clusters) + len(all_clusters[min_y].clusters)))

    # Return the indexes of the min distance that are also the 2 clusters we will merge
    return [min_x, min_y]


# Insert the cluster and its distances in the right place in order not to lose the sorting
def insert_cluster(new_cluster: Cluster, all_cluster: list, new_distances: list, distances: list, insert_index):
    # The new cluster we created instead of append them in all_cluster list we will insert it to the right place in order not to destroy the sorting
    # The same we will do with the distance table too by keeping the insertion index.
    all_cluster.insert(insert_index, new_cluster)

    # Append distance to itself
    new_distances.insert(insert_index, 99999)
    # Append the new row
    distances.insert(insert_index, new_distances)

    # Append the new column
    for i in range(0, len(distances)):
        if i != insert_index:
            distances[i].insert(insert_index, new_distances[i])


# Delete the distances of the clusters we merged and the cluster in all cluster list according to which index is greater
def delete_clusters(c1: int, c2: int, distances: list, all_clusters: list):
    if c1 > c2:
        del all_clusters[c1], all_clusters[c2]
        del distances[c1], distances[c2]
        for i in range(0, len(distances)):
            del distances[i][c1], distances[i][c2]
        return c2
    else:
        del all_clusters[c2], all_clusters[c1]
        del distances[c2], distances[c1]
        for i in range(0, len(distances)):
            del distances[i][c2], distances[i][c1]
        return c1


# Lance-Williams single method
def single_method(s: Cluster, t: Cluster, all_clusters: list, c1: int, c2: int):
    dist = []   # The new distances we will calculate

    # For every cluster except the 2 cluster we merged calculate the distance according to the single method parameters
    for i in range(0, len(all_clusters)):
        if i not in [c1, c2]:
            dist_s_u = s.single_cluster_distance(all_clusters[i])
            dist_t_u = t.single_cluster_distance(all_clusters[i])
            dist.append(0.5 * dist_s_u + 0.5 * dist_t_u - 0.5 * abs(dist_s_u - dist_t_u))

    return dist


# Lance-Williams complete method
def complete_method(s: Cluster, t: Cluster, all_clusters: list, c1: int, c2: int):
    dist = []   # The new distances we will calculate

    # For every cluster except the 2 cluster we merged calculate the distance according to the complete method parameters
    for i in range(0, len(all_clusters)):
        if i not in [c1, c2]:
            dist_s_u = s.complete_cluster_distance(all_clusters[i])
            dist_t_u = t.complete_cluster_distance(all_clusters[i])
            dist.append(0.5 * dist_s_u + 0.5 * dist_t_u + 0.5 * abs(dist_s_u - dist_t_u))

    return dist


# Lance-Williams average method
def average_method(s: Cluster, t: Cluster, all_clusters: list, c1: int, c2: int):
    dist = []   # The new distances we will calculate

    # Calculating the parameters for the mathematical formula.
    ai = len(s.clusters) / (len(s.clusters) + len(t.clusters))
    aj = len(t.clusters) / (len(s.clusters) + len(t.clusters))

    # For every cluster except the 2 cluster we merged calculate the distance according to the average method parameters.
    for i in range(0, len(all_clusters)):
        if i not in [c1, c2]:
            dist_s_u = s.average_cluster_distance(all_clusters[i])
            dist_t_u = t.average_cluster_distance(all_clusters[i])
            dist.append(round((ai * dist_s_u + aj * dist_t_u), 2))

    return dist


# Lance-Williams ward method
def ward_method(s: Cluster, t: Cluster, all_clusters: list, distances: list, c1: int, c2: int):
    dist = []   # The new distances we will calculate
    dist_s_t = distances[c1][c2]    # Distance between the 2 clusters we will merge

    # For every cluster except the 2 cluster we merged calculate the distance according to the ward method parameters.
    for i in range(0, len(all_clusters)):
        if i not in [c1, c2]:
            # Calculating the parameters for the mathematical formula.
            ai = (len(s.clusters) + len(all_clusters[i].clusters)) / (
                        len(s.clusters) + len(t.clusters) + len(all_clusters[i].clusters))
            aj = (len(t.clusters) + len(all_clusters[i].clusters)) / (
                        len(s.clusters) + len(t.clusters) + len(all_clusters[i].clusters))
            b = len(all_clusters[i].clusters) / (
                        len(s.clusters) + len(t.clusters) + len(all_clusters[i].clusters))

            # Calculate the distance with the cluster
            dist_s_u = distances[c1][i]
            dist_t_u = distances[c2][i]
            dist.append(round((ai * dist_s_u + aj * dist_t_u - b * dist_s_t), 2))

    return dist


# The main method
if __name__ == "__main__":
    # Start by reading the args and make sure the input are ok!
    read_args()

    # Create a list with all the cluster object inside
    all_clusters = create_all_cluster()

    # Perform the lance williams method
    lance_williams(all_clusters)

