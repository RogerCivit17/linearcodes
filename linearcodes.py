#!usr/bin/python

from extra import *
import copy
import itertools
from colorama import init, Fore, Back, Style


def compute_Gcan_and_H(generators): 
    try:
        if not (isinstance(generators, list) and generators):
            raise ValueError("Invalid input: generators must be a non-empty list of vectors")

        generators = [list(vector) for vector in generators]
        G = Matrix(generators)  # G
        rows = len(G.matrix)
        columns = len(G.matrix[0])
        combinations = list(itertools.combinations([i for i in range(columns)], rows))  # Possibles combinacions d'índexs de columnes (0,2,1,4)

        for comb in combinations:
            Gcan = Matrix(copy.deepcopy(G.matrix))  # Copiem Gcan = G però són matrius independents
            if comb != tuple([i for i in range(rows)]):  # Mira si la combinació és diferent a la predeterminada (1,2,3,4...)
                for c in range(rows):
                    Gcan.swap_columns(c, comb[c])  # Si és diferent canvia les columnes

            if Gcan.determinant(rows=rows, columns=rows) != 0:
                for index in range(rows):  # Mètode de Gauss amb pivot
                    row = index
                    pivot = index
                    pivot_r = row
                    for r in range(rows - row):
                        if Gcan.matrix[r + row][pivot] == 0:
                            pivot_r += 1
                        else:
                            break

                    if pivot_r > (rows - 1):
                        raise ValueError("Matrix is not invertible. No canonical form exists.")
                    else:
                        Gcan.swap_rows(row, pivot_r)
                        for r in range(rows - (row + 1)):  # Part triangular superior de la matriu
                            if Gcan.matrix[r + (row + 1)][pivot] != 0:
                                Gcan.sum_rows(r + (row + 1), row)
                for i in range(rows):
                    pivot = (rows - 1) - i
                    row = (rows - 1) - i
                    for r in range(rows - (i + 1)):  # Part triangular inferior de la matriu
                        if Gcan.matrix[row - (r + 1)][pivot] != 0:
                            Gcan.sum_rows(row - (r + 1), row)

                A = Matrix([[Gcan.matrix[r][c + rows] for c in range(columns - rows)] for r in range(rows)])  # Obtenim la matriu A (part dreta de la matriu Gcan)
                AT = A.transpose()  # Obtenim A Transposada AT per tal d'obtenir la matriu H
                IAn_k = Matrix([[1 if (c == r) else 0 for c in range(columns - rows)] for r in range(columns - rows)])  # Obtenim la matriu identitat resultant d'H
                H = Matrix([AT.matrix[r] + IAn_k.matrix[r] for r in range(columns - rows)])  # Obtenim Hcan que és (-AT|I) | En binari -AT = AT

                if comb != tuple([i for i in range(rows)]):  # Tornem a les columnes originals si aquesta no és la combinació
                    for c in range(rows):
                        Gcan.swap_columns((rows - 1) - c, comb[(rows - 1) - c])
                break

        return Gcan, H

    except ValueError as e:
        print(e)
        return None


def parameters(Hcan):
    n = len(Hcan.matrix[0])
    k = len(Hcan.matrix)
    size = pow(2, k)
    s=size-1 #Nº Words possibles
    delta = n
    column = k
    delta_i = 0
    while((s+1) != 0): #Fem el calcul del pes per a totes les possibles Words
        m2 = [decimal2binari(s,k)]
        m3 = Matrix(m2)
        m_table = m3.multiply(Hcan) #Possibles Words del codi Hcan*vectors
        for val in m_table.matrix[0]:
            if(val == 1): #Calculem el pes de cada Word (nº 1's)
                delta_i += 1
        if(delta_i < delta and delta_i > 0): #Ens quedem amb el pes mínim
            delta = delta_i 
        delta_i = 0
        s -= 1
        
    error_detection = delta-1
    error_correction = int(error_detection/2)
    values = (n, k, size, delta, error_detection, error_correction)
    return values


def codifying(Gcan, bits):
    n = len(Gcan.matrix)
    while (len(bits)%n != 0):#Mirem que la longitud sigui múltiple de n 
        bits = bits + [0] #Padding
        
    X = Matrix([[ bits[c+(n*r)] for c in range(n)] for r in range(int(len(bits)/n))])#Cada fila de la matriu correspon a un bloc de longitud n dels bits
    codedBitsMatrix = X.multiply(Gcan) #Y = Gcan*X
    Y = []
    for b in codedBitsMatrix.matrix: #Passem els bits en forma de matriu a una llista
        Y += b 
    return Y


def detect_and_decodifying(Gcan, C_bits):
    n = len(Gcan.matrix[0])
    k = len(Gcan.matrix)
    errors_detected=0
    Gcan, H = compute_Gcan_and_H([tuple(Gcan.matrix[r]) for r in range(k)])
    _, _, _, _, error_detection, _ = parameters(H)
    H_t = H.transpose() #Trobem HT
    C_bits_Matrix = Matrix([[ C_bits[c+(n*r)] for c in range(n)] for r in range(int(len(C_bits)/n))])# Posem els bits en una matriu, files d'n bits
    sindrome = C_bits_Matrix.multiply(H_t) #La sindrome  = C_bits * HT
    for b in range(len(sindrome.matrix)):
        if (errors_detected!=error_detection):
            if (1 in sindrome.matrix[b]): #Busquem si hi ha 1's en la sindrome --> Errors
                errors_detected+=1
                Y = C_bits_Matrix.matrix[b].copy()
                print("\nAn error has been detected in this part of the code", str(Y) + ".")
                return None

    I_kxk = Matrix([[1 if (c == r) else 0 for c in range(k)] for r in range(k)]) #Creem la matriu Identitat(kxk)
    R = Matrix([I_kxk.matrix[r]+[0 for c in range(n-k)] for r in range(k)]) #Creem la matriu  R = (I_kxk | 0's)
    X_Matrix = C_bits_Matrix.multiply(R.transpose()) #Obtenim  x = Y * R_T
    
    X = []
    for b in X_Matrix.matrix:
        X += b
    return X

def detect_and_correct(Gcan, C_bits):
    n = len(Gcan.matrix[0])
    k = len(Gcan.matrix)
    errors_detected=0
    errors_corrected=0
    Gcan, H = compute_Gcan_and_H([tuple(Gcan.matrix[r]) for r in range(k)])
    _, _, _, _, error_detection, error_correction = parameters(H)
    C_bits_Matrix = Matrix([[ C_bits[c+(n*r)] for c in range(n)] for r in range(int(len(C_bits)/n))])
    sindrome = C_bits_Matrix.multiply(H.transpose())  #La sindrome  = C_bits * HT
    for b in range(len(sindrome.matrix)):
        if (errors_detected!=error_detection):
            if (1 in sindrome.matrix[b]): #Busquem errors en el codi
                errors_detected+=1
                for h in range(len(H.transpose().matrix)):
                    if (sindrome.matrix[b] == H.transpose().matrix[h]): #Busquem el bit erroni
                        Y = C_bits_Matrix.matrix[b].copy()
                        errorMessage = "".join(Fore.RED + str(Y[i]) + Fore.RESET if (i==h) else str(Y[i]) for i in range(len(Y)))
                        if(errors_corrected!=error_correction):
                            C_bits_Matrix.matrix[b][h] ^= 1 #Corregim el codi, neguem el valor 0-->1, 1-->0
                            correctedCode = C_bits_Matrix.matrix[b].copy()
                            correctMessage = "".join(Fore.GREEN + str(correctedCode[i]) + Fore.RESET if (i==h) else str(correctedCode[i]) for i in range(len(correctedCode)))
                            print("An error has been detected in: ", Y, "in bit", str(h+1)+". Correction:", errorMessage,"--->", correctMessage)
                            break
                        else:
                            print("An error has been detected but the code cannot correct it")
                            return None

    I_kxk = Matrix([[1 if (c == r) else 0 for c in range(k)] for r in range(k)]) #Creem la matriu Identitat(kxk)
    R = Matrix([I_kxk.matrix[r]+[0 for c in range(n-k)] for r in range(k)]) #Creem la matriu  R = (I_kxk | 0's)
    X_Matrix = C_bits_Matrix.multiply(R.transpose()) #Obtenim  x = Y * R_T
    
    X = []
    for b in X_Matrix.matrix:
        X += b
    return X

if __name__ == '__main__':
    print("LINEAR CODES TESTS: \n")

    print("TEST 1:\n")
    print("Given matrix A:")
    A=Matrix([(0, 0, 1, 0, 1), (1, 0, 0, 1, 0), (1, 1, 1, 0, 1)])
    print(A)
    Gcan, Hcan = compute_Gcan_and_H([(0, 0, 1, 0, 1), (1, 0, 0, 1, 0), (1, 1, 1, 0, 1)])
    print("\n")
    print("The Canonical Generating Matrix is:")
    print(Gcan)
    print("\n")
    print("The Control Matrix is:")
    print(Hcan)
    n, k, size, delta, error_detection, error_correction = parameters(Hcan)
    print("\n")
    print("> Length (n) ->", n)
    print("> Dimension (k) ->", k)
    print("> Size ->", size)
    print("> Delta (δ) ->", delta)
    print("> Errors detection ->", error_detection)
    print("> Errors correction ->", error_correction)
    print("\n")
    X=[0,0,0,1,0,1,1,0,1]
    print("Given the bits:")
    print(X)
    Y=codifying(Gcan,X)
    print("\nCoded bits:")
    print(Y)
    print("\nDecoded bits:")
    X=detect_and_decodifying(Gcan, Y)
    print(X)
    print("\nChanging the seventh bit of Y:\n")
    Y=[0, 0, 0, 0, 0, 1, 1, 1, 1, 1, 1, 0, 1, 1, 1]
    print(Y)
    print("\nDecoded bits:")
    X=detect_and_decodifying(Gcan, Y)
    print(X)
    print("\nTrying now to correct the errors...\n")
    X=detect_and_correct(Gcan, Y)
    print("\nThe Code corrected and decoded is:")
    print(X)


    
    print("----------------------------------------------------------------------------")

    print("\n")
    print("TEST 2:\n")
    print("Given matrix B:")
    B=Matrix([(1, 0, 1, 1, 0, 0), (1, 1, 1, 0, 0, 1), (1, 0, 0, 1, 0, 1)])
    print(B)
    Gcan, Hcan = compute_Gcan_and_H([(1, 0, 1, 1, 0, 0), (1, 1, 1, 0, 0, 1), (1, 0, 0, 1, 0, 1)])
    print("\n")
    print("The Canonical Generating Matrix is:")
    print(Gcan)
    print("\n")
    print("The Control Matrix is:")
    print(Hcan)
    n, k, size, delta, error_detection, error_correction = parameters(Hcan)
    print("\n")
    print("> Length (n) ->", n)
    print("> Dimension (k) ->", k)
    print("> Size ->", size)
    print("> Delta (δ) ->", delta)
    print("> Errors detection ->", error_detection)
    print("> Errors correction ->", error_correction)
    print("\n")
    X=[0,0,0,1,0,1,1,0,1]
    print("Given the bits:")
    print(X)
    Y=codifying(Gcan,X)
    print("\nCoded bits:")
    print(Y)
    print("\nDecoded bits:")
    X=detect_and_decodifying(Gcan, Y)
    print(X)
    print("----------------------------------------------------------------------------")
    
    print("\n")
    print("TEST 3:\n")
    print("Given matrix C:")
    C=Matrix([(0, 1, 0, 0, 1, 0, 1), (1, 0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 1, 1, 1), (0, 0, 1, 0, 0, 1, 1)])
    print(C)
    Gcan, Hcan = compute_Gcan_and_H([(0, 1, 0, 0, 1, 0, 1), (1, 0, 0, 0, 1, 1, 0), (0, 0, 0, 1, 1, 1, 1), (0, 0, 1, 0, 0, 1, 1)])
    print("\n")
    print("The Canonical Generating Matrix is:")
    print(Gcan)
    print("\n")
    print("The Control Matrix is:")
    print(Hcan)
    n, k, size, delta, error_detection, error_correction = parameters(Hcan)
    print("\n")
    print("> Length (n) ->", n)
    print("> Dimension (k) ->", k)
    print("> Size ->", size)
    print("> Delta (δ) ->", delta)
    print("> Errors detection ->", error_detection)
    print("> Errors correction ->", error_correction)
    print("\n")
    X=[0,0,0,1,0,1,1,0,1,0,1,1]
    print("Given the bits:")
    print(X)
    Y=codifying(Gcan,X)
    print("\nCoded bits:")
    print(Y)
    print("\nChanging the third bit of Y:\n")
    Y=[0, 0, 1, 1, 1, 1, 1, 0, 1, 1, 0, 1, 1, 0, 1, 0, 1, 1, 0, 1, 0]
    print(Y)
    print("\nDecoded bits:")
    X=detect_and_decodifying(Gcan, Y)
    print(X)
    print("\nTrying now to correct the errors...\n")
    X=detect_and_correct(Gcan, Y)
    print("\nThe Code corrected and decoded is:")
    print(X)
    
    
