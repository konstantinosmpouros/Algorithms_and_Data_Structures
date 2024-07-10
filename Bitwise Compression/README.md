 # Elias and Fano Compression Algorithm


## Problem Description
The Elias and Fano technique is a method for compressing sequences of integers. This method is particularly effective for certain types of data, such as sparse and sorted integer sequences. The compression is done using bitwise operations. The whole concept of the problem is to avoid overloading memory by using strings to handle the bits of each number to create the L and U byte arrays. The L and U byte arrays serve distinct purposes for compressing sequences of integers. The L byte array contains the lower bits of each integer, stored in a fixed-width format. On the other hand, the U byte array holds the upper bits, encoded using unary coding to efficiently represent the more significant parts of the integers. This encoding method marks the position of each integer's higher-order bits, facilitating accurate retrieval.


So to implement this compression method its clear that we must found for sure a way to solve 3 problem with bitwise operations:

1. Take the first l bits of a byte.

**E.g.** 001100 -> **11** (if the l = 2)

2. Take all the bits of the byte except the first l bits.

**E.g.** 001100 -> **11** (if the l = 2)

3. How to handle those bits properly without losing any of them and put them in logical order to create bytes.

4. Append those byte we have created to the byte arrays.


## Solutions

The solution I have implemented is as follows.

1. The first problem can be resolved by using the operator AND (&) with the byte we want the a byte that we will create. The created byte will be l timed the 1. This means if we want the first 4 bits we will do (byte & 1111). E.g. if we have the following byte, 10011011, and we want the first 3 we will do, 10011011 & 111, and the result will be 011.

2. The second problem is easier cause by right swifting of the byte (>>) as many times we want we can cut as many bits we want from the right. E.g. if the have 10011011 and we want to cut the first 3 bits we just do 10011011 >> 3 and we have 10011.

3. The third problem is accually how to take tose bits and create the right appendable bytes. The whole concept to tranfer the bits is by useing the number 1 which is in binary the 00000001 and by swifting left we will append each time the new bits.

    - For the L bytearray by taking the first l bits of each number we just do l swifts in the left so the byte will have l new zeros in the right and then by using the OR (|) operator its like appending those new bits in the byte we have. E.g. After we left swift 3 bits (if l=3) and the bits we want to add is 011 we do 10100101000 | 011. The result will be 10100101**011**. Cause of the left swifting we secure that all the bits will be appended even if the bits starts with 0.

    - For the U bytearray after we right swift l bits and do the subtraction we end up with the new modified number. The idea here is a bit the same with the L bytearray. We take the byte 1 as the beggining in order not to lose any zeros and then we left swift l + 1 times. Why + 1? cause we need l zeros and then the number 1 so the extra zero must be converted to 1. And thats what we do by using the OR operator (|) with the number 1.

4. Finally the last problem is how to append those bytes in the bytearrays. In both the L and U bytearray we have a byte that starts with 1 and we just append bits in the right and make it bigger for every number we have read. So the idea here is the following. The byte keeps getting bigger so its structure will be like 1 + all the bits we want to append + some zeros we might add at the end to fill. In order not to make this byte enormous we say that while the byte length is greater or equal than 9 (9 cause we have 1 bits extra and 8 we have just added) we must append a byte in order to save some space in the memory too. Now there are 2 cases.

    - One, the byte length to be exact 9, so we just use the AND operator (&) with 255, we take the first 8 bits from the right and we append these bytes and then we make the byte equal to 1 to add the next bits we extract.

    - The second case is when the byte length is greater than 9, so by right swifting (byte length - 9) bits we take the one extra bit we had to begin with and 8 more bits that we need to append. And now we follow the same step as in the first case. The difference here is what the byte will be. The byte structure will be 1 + the 8 bits we appended + some more bits we need to keep. So we take the number 1 again and we left swift it by (byte length - 9 times), which is the number of bytes we have to keep, and we use the OR operator (|) with the extracted bits that we have to keep. To extract these bits, we take the byte and use the AND (&) operator with a custom byte consisting of only 1 and whose bit length is equal to the bits we want to extract from the byte.  
    E.g. If we have a byte and 1 is the extra bit + 01001011 the appended bits + 01101 the extra bits we have to keep, we will do byte & 11111 to take the last 5 bits on the right that we have to keep. So the byte at the end will be 1 + the extra bits that we haven't appended and as long as we read more number and we have more bits to append in the big byte we have created and we will use one of these 2 cases to append the bytes in the byte arrays.


## How to run

python elias_fano.py file

- **file:** The file containing the integers to be compressed.





## Examples 

```sh
python elias_fano.py example_1.txt
```


```sh
python elias_fano.py example_2.txt
```


```sh
python elias_fano.py example_3.txt
```


## References 
- Elias, Peter. 1974. “Efficient Storage and Retrieval by Content and Address of Static Files.” Journal of the ACM 21 (2): 246–60. https://doi.org/10.1145/321812.321820.

- Fano, Robert M. 1971. “On the Number of Bits Required to Implement an Associative Memory.” Computation Structures Group Memo 61, Project MAC, Massachusetts Institute of Technology.
