# Lance and Williams Hierarchical Clustering

## Resolution rationale
in order to solve the problem, we create a class called Cluster where we will create for each number one object at the beginning and inside it will contain a list where each number will be entered. In the process, as we will merge objects between them, we will merge their lists and sort them. First we create some lists that will help us do all the calculations, which are: <br>
1. all_clusters: A list that will store all objects of type Cluster
2. distances: A 2D list that will contain all the possible distances of the objects we made.
3. result: We will need this list for every merge of 2 object in order to track the merges we are doing and have a summary at the end.<br>

The concept goes as following:
At the beginning, we create a list that will contain all the Objects that we will make and we initially sort all the objects in it, resulting in the following list:

[1]<br>
[2]<br>
[4]<br>
[6]<br>
[7]<br>
[10]<br>
[12]<br>
[19]<br>
[20]<br>
[25]<br>

** The numbers are not random but we take them from the example.txt

Then we create the distances "table" where its dimensions will be n*n where n is the number of objects we made and we will put a very large value like 99999 in every when we initialize it. Resulting with the following table:

[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>
[99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999, 99999]<br>


Then we will update this table by putting in each cell the distance between the row number and the col number, which will be the difference of the numbers that each cluster has. But in the position that marks the distance between a cluster with itself we will leave it at 99999. Resulting with the following updated table:<br>

[99999, 1.0, 3.0, 5.0, 6.0, 9.0, 11.0, 18.0, 19.0, 24.0]<br>
[1.0, 99999, 2.0, 4.0, 5.0, 8.0, 10.0, 17.0, 18.0, 23.0]<br>
[3.0, 2.0, 99999, 2.0, 3.0, 6.0, 8.0, 15.0, 16.0, 21.0]<br>
[5.0, 4.0, 2.0, 99999, 1.0, 4.0, 6.0, 13.0, 14.0, 19.0]<br>
[6.0, 5.0, 3.0, 1.0, 99999, 3.0, 5.0, 12.0, 13.0, 18.0]<br>
[9.0, 8.0, 6.0, 4.0, 3.0, 99999, 2.0, 9.0, 10.0, 15.0]<br>
[11.0, 10.0, 8.0, 6.0, 5.0, 2.0, 99999, 7.0, 8.0, 13.0]<br>
[18.0, 17.0, 15.0, 13.0, 12.0, 9.0, 7.0, 99999, 1.0, 6.0]<br>
[19.0, 18.0, 16.0, 14.0, 13.0, 10.0, 8.0, 1.0, 99999, 5.0]<br>
[24.0, 23.0, 21.0, 19.0, 18.0, 15.0, 13.0, 6.0, 5.0, 99999]<br>

Then we will merge the two closest clusters each time until we are left with only one cluster. We will simply search and pass through the distances table the two indexes from the min value, let's call these indexes minx, miny.

This means that if the min value is distance[0][1] then we have to get all_cluster[0], all_cluster[1] from the all_clusters list and merge them. We merge them without removing the two clusters from the all_cluster list, and it is important to sort the integers they contain.

Having reserved the indexes from the clusters that we will merge, we went according to the method we tried from the input to calculate the distances with all the other clusters. The s, t of the type are all_clusters[minx], all_clusters[miny].

Then, once we have found the distances, we delete all_clusters[minx], all_clusters[miny] corresponding to more than the two indexes is larger because otherwise you will move the other one. Delete the largest first and then the smallest. We do the same in the distances table, where we delete the line and the column with the largest index and then the smallest.

And finally we go and insert the new cluster and the new distances in the position where the micro index was from the two clusters we merged. The reason is the following. If we have the following column and we want to merge the following two clusters.

[1] <--<br>
[2]<br>
[4]<br>
[6]<br>
[7]<br>
[10] <--<br>
[12]<br>
[19]<br>
[20]<br>
[25]<br>

Then the result of the merge would be [1, 10], so it would have to be placed in the position of the smaller of the two clusters to maintain the sorting. Then the result will be the following:

[1, 10]<br>
[2]<br>
[4]<br>
[6]<br>
[7]<br>
[12]<br>
[19]<br>
[20]<br>
[25]<br>

we do exactly the same in the 2D list with the distances. We delete the old distances and go to the smallest index and put the new distances but with a small difference.

Let's say that the list of new distances is as follows:<br>
dist = [1, 5, 6, 1, 2.5]

And we want to insert it at index 1. We must first go and put the element 99999 at the point that will mark the distance of the new cluster from itself. This position will obviously be the index we are going to insert, i.e. dist.insert(1, 99999). As a result, we will put the following in the table as a column and as a row:

[1, 99999, 5, 6, 1, 2.5]

We repeat the same thing until we are left with one cluster.
