# Burst Period Detection using Viterbi and Bellman-Ford Algorithms


## Introduction

This project implements two algorithms, Viterbi and Bellman-Ford, to detect periods of activity in a system based on message emission timestamps. The objective is to find the optimal sequence of system states and the periods during which the system is in each activity level.


## Problem Description

Given a series of timestamps indicating when messages were emitted by a system, the task is to analyze these timestamps and determine periods of increased activity. The problem can be modeled as finding the shortest path in a trellis (lattice) graph. This can be achieved using the Viterbi algorithm or the Bellman-Ford algorithm. This approach for detecting bursts was proposed by Jon Kleinberg (2003) who tested it in his personal email correspondence. More information about the solution are in the paper [[1]](https://link.springer.com/article/10.1023/A:1024940629314)


## How to run

python bursts.py [-s S] [-g GAMMA] [-d] {viterbi,trellis} offsets_file

- **-s S:** If given, the value of the parameter 𝑠 of the algorithm. If not given, we assume 𝑠 = 2.
- **-g GAMMA:** If given, the value of the parameter g of the algorithm. If not given, we assume g = 1.
- **-d:** If given, the program will print out the diagnostic messages.
- **{viterbi,trellis}:** if the user gives viterbi, the program will execute the viterbi algorithm else if the user gives trellis, the program will execute the Bellman-Ford algorithm.
- **offsets_file:** Is the name of the file containing the time points of the message transmission times.


## Examples

```sh
python bursts.py viterbi two_states.txt
```

```sh
python bursts.py viterbi two_states.txt -d
```

```sh
python bursts.py trellis two_states.txt
```

```sh
python bursts.py trellis two_states.txt -d
```

```sh
python bursts.py viterbi three_states_1.txt
```

```sh
python bursts.py trellis three_states_1.txt
```

```sh
python bursts.py viterbi three_states_2.txt -s 3 -g 0.5
```

```sh
python bursts.py trellis three_states_2.txt -s 3 -g 0.5
```

```sh
python bursts.py viterbi four_states.txt -s 1.1 -g 0.025
```

```sh
python bursts.py trellis four_states.txt -s 1.1 -g 0.025
```


## References

1. Jon Kleinberg. “Bursty and Hierarchical Structure in Streams”. In: Data Mining and Knowledge Discovery 7.4 (2003), pp. 373–397. doi: [10.1023/A:1024940629314](https://link.springer.com/article/10.1023/A:1024940629314)