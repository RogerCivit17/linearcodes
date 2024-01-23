#!usr/bin/python
#-*- coding:utf-8

import copy

def decimal2binari(decimal_number,k):
    bin_table = []
    steps = 0
    while(decimal_number != 0):
        module = decimal_number % 2
        quotient = decimal_number // 2
        bin_table.append(module) 
        decimal_number = quotient 
        steps+=1
    if(len(bin_table)>=k):
        bin_table=bin_table[::-1]
    while(len(bin_table)<k):
        if(steps==2):
            bin_table=bin_table[::-1]            
        bin_table.insert(0,0)
    return bin_table
    

class Matrix:
    def __init__(self, matrix):
        self.matrix = matrix

    def swap_rows(self, row1, row2):
        self.matrix[row1], self.matrix[row2] = self.matrix[row2], self.matrix[row1]

    def swap_columns(self, col1, col2):
        for row in self.matrix:
            row[col1], row[col2] = row[col2], row[col1]

    def sum_rows(self, row1, row2):
        for e in range(len(self.matrix[0])):
            self.matrix[row1][e] = self.matrix[row1][e] ^ self.matrix[row2][e]

    def transpose(self):
        transposed = [[None for i in range(len(self.matrix))] for j in range(len(self.matrix[0]))]
        for i in range(len(self.matrix)):
            for j in range(len(self.matrix[0])):
                transposed[j][i] = self.matrix[i][j]
        return Matrix(transposed)

    def multiply(self, other):
        if (len(self.matrix[0])!=len(other.matrix)):
            print("Matrices can't be multiplied\n")
        else:
            m3 = []
            for i in range(len(self.matrix)):
                #longitud de les files de la matriu
                list_a = []
                for j in range(len(other.matrix[0])):
                    #longitud de columnes matrius
                    mult= 0
                    for k in range(len(other.matrix)):
                        mult^=self.matrix[i][k]&other.matrix[k][j]
                    list_a.append(mult)
                m3.append(list_a)
            return Matrix(m3)
    
    def determinant(self, rows = None, columns = None):
        if ((rows == None) or (columns == None)):
            rows = len(self.matrix)
            columns = len(self.matrix[0])

        if (rows == columns):
            if (rows == 1):
                return self.matrix[0][0]
            elif (rows == 2): # 2x2 matrix
                return ((self.matrix[0][0] & self.matrix[1][1]) ^ (self.matrix[1][0] & self.matrix[0][1]))
            else: #Gauss reduction
                gauss = Matrix(copy.deepcopy(self.matrix))
                for i in range(rows):
                    pivot = i
                    row = i
                    pivot_row = row
                    for r in range(rows-row):
                        if (gauss.matrix[r+row][pivot] == 0):
                            pivot_row += 1
                        else:
                            break
                   
                    if (pivot_row > (rows-1)):
                        return 0
                    else:
                        gauss.swap_rows(row, pivot_row)
                        for r in range(rows-(row+1)):
                            if (gauss.matrix[r + (row+1)][pivot] != 0):
                                gauss.sum_rows(r + (row+1), row)
                det = 1
                for e in range(rows):
                    det *= gauss.matrix[e][e]
                return det
    
    def __str__(self):
        show_matrix = "\n"
        for i in self.matrix:
            show_matrix += "( "
            for j in i:
                show_matrix += str(j) + " "
            show_matrix += ")\n" 
        return show_matrix[:-1]
    

