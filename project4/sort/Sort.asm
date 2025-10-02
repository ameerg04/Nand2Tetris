// This file is part of nand2tetris, as taught in The Hebrew University,
// and was written by Aviv Yaish, and is published under the Creative 
// Common Attribution-NonCommercial-ShareAlike 3.0 Unported License 
// https://creativecommons.org/licenses/by-nc-sa/3.0/

// An implementation of a sorting algorithm. 
// An array is given in R14 and R15, where R14 contains the start address of the 
// array, and R15 contains the length of the array. 
// You are not allowed to change R14, R15.
// The program should sort the array in-place and in descending order - 
// the largest number at the head of the array.
// You can assume that each array value x is between -16384 < x < 16384.
// You can assume that the address in R14 is at least >= 2048, and that 
// R14 + R15 <= 16383. 
// No other assumptions can be made about the length of the array.
// You can implement any sorting algorithm as long as its runtime complexity is 
// at most C*O(N^2), like bubble-sort. 

// Put your code here.

@i //first loop counter 
M=0
(LOOP) 
@i
D=M
@R15
D=D-M
D=D+1
@END
D;JEQ

// second loop
@j
M=0
(INNER_LOOP)
@j
D=M 
@R15
D=D-M 
@i
D=D+M 
D=D+1
@INCREACE_I // End of the second loop and going back to the iteration in the first loop
D;JEQ

@j // taking the value of arr[j]
D=M 
@R14
A=M+D 
D=M 
@first_elem 
M=D 

@j // taking the value of arr[j+1]
D=M 
@R14
A=M+D
A=A+1 
D=M 
@second_elem 
M=D 

@first_elem
D=D-M // checking arr[j] - arr[j+1] to swap 

@SWAP 
D;JGT

@j // going to the next iteration if we don't swap
M=M+1
@INNER_LOOP
0;JMP

// Swaping the values of arr[j] and arr[j+1]
(SWAP)
@j // getting the address of arr[j]
D=M 
@R14
A=M+D 
D=A 
@first_address
M=D 

@j // getting the address of arr[j+1] 
D=M 
@R14
A=M+D 
A=A+1
D=A 
@second_address
M=D 

@second_elem
D=M 
@first_address
A=M 
M=D 

@first_elem
D=M 
@second_address
A=M 
M=D 

@j 
M=M+1

@INNER_LOOP
0;JMP

// Increasing i and moving to the next iteration in the second loop
(INCREACE_I)
@i
M=M+1
@LOOP
0;JMP

// End of the program
(END)
@END
0;JMP
