# Elias and Fano Compression Algorithm

The purpose of the README file is to explain in a detailed way how the problem has been solved.

## Problem concept

The whole concept of the problem is not to overload the memory with the use of strings in order to handle the bits of each number in order to create the L and U bytearrays. This means that the implementation must be with the main use of bitwise operators. So by reading the way of the compression method its clear that we must found for sure a way to solve 3 problem with bitwise operations :

1. Take the first l bits of a byte.

**E.g.** 001100 - **11** (if the l = 2)

2. Take all the bits of the byte except the first l bits.

**E.g.** **001100** - 11 (if the l = 2)

3. How to handle those bits properly without losing any of them and put them in logical order to create bytes.

4. Appending those byte we have created to the byte arrays.

## Problem solutions

The solution that I conducted if the folling.

1. The first problem can be solved by using the operator AND (&) with the byte we want the a byte that we will create. The created byte will be l timed the 1. That means if we want the first 4 bits we will do (byte & 1111). E.g. if the have 10011011 and we want the first 3 we will do 10011011 & 111. and the result will be 011.

2. The second problem is way too easy cause by right swifting of the byte (>>) as many times we want we can cut as many bits we want from the right. E.g. if the have 10011011 and we want to cut the first 3 bits we just do 10011011 >> 3 and we have 10011.

3. The third problem is accually how to take tose bits and create the right appendable bytes. The whole concept to tranfer the bits is by useing the number 1 which is in binary the 00000001 and by swifting left we will append each time the new bits.
    - For the L bytearray by taking the first l bits of each number we just do l swifts in the left so the byte will have l new zeros in the right and then by using the OR (|) operator its like appending those new bits in the byte we have. E.g. After we left swift 3 bits and the bits we want to add is 011 we do 10100101000 | 11. The result will be 10100101**011**. Cause of the left swifting we secure that all the bits will be appended even if the bits starts with 0.
    - For the U bytearray after we right swift l bits and do the subtraction we end up with the new modified number. The idea here is a bit the same with the L bytearray. We take the byte 1 as the beggining in order not to lose any zeros and then we left swift l + 1 times. Why + 1? cause we need l zeros and then the number 1 so the extra zero must be converted to 1. And thats what we do by using the OR operator (|) with the number 1. 

4. Finally the last problem is how to append those bytes in the bytearrays. In both the L and U bytearray we have a byte that at the beggining was 1 and we just append bits in the right and make it bigger for every number we have read. So the idea here is the following. The byte keeps getting bigger so its structure will be like 1 + all the bits we want to append + some zeros we might add at the end. In order not to make this byte enormous we say that while the byte length is greater or equal than 9 (9 cause we have 1 bits extra and 8 we have just added) we must append a byte in order to save some space in the memory too. Now there are 2 cases.
    - One, the byte bit length to be exact 9 so we just by just using AND operator (&) with 255 we take the first 8 bits from the right and we just append this bytes and we then make the byte equal to 1 in order to add the next bits we extract.
    - Second case is if the byte length is greater than 9 so be right swifting (byte length - 9) bits we take the one extra bit we had from the start and 8 more bits that we must append. And now we follow the same step as the first case. The difference here is what the byte will be equal to. The byte structure will be 1 + the 8 bits we appended + some more bits that we must keep. So we take the number 1 again and we left swift it (byte length - 9 times) which is the number of byte we must keep and we use the OR operator (|) with the extracted bits that we must keep. In order to extract those bits we take the byte and use the AND (&) operator with a custom byte which consist of only 1 and its bit length is equal to the bits we want to extract from the byte. E.g. 
    if the byte is 1 the extra bit + 01001011 the appended bits + 01101 the extra bits we must keep,  we will do byte & 11111 in order to take the last 5 bits on the right that we must keep. So the byte in the end will 1 + the extra bits that we haven't appended and as long we read more number and we have more bits to append in the big byte we have created we will use one of this 2 case in order to append the bytes in the byte arrays.

