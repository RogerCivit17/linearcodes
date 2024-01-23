PROGRAM: Linear Codes in action by Imad Salmi & Roger Miquel

A linear code is a type of error-correcting code used in information theory and coding theory. It is characterized by its linearity property, which means that the sum of any two codewords in the code is also a codeword. Linear codes are widely employed in communication systems to detect and correct errors that may occur during data transmission.

Linear codes are associated with two important matrices – the generator matrix (G) and the parity-check matrix (H). The generator matrix defines the linear transformation used to encode the information, while the parity-check matrix is utilized for error detection and correction.

The parameters of a linear code are typically denoted as (n, k, δ), where:
n is the length of the codeword.
k is the dimension of the code, representing the number of information bits.
δ is the minimum Hamming distance between any two distinct codewords, indicating the error-detecting and error-correcting capabilities of the code.
To encode a message using a linear code, the information bits are multiplied by the generator matrix (G), resulting in a codeword. Mathematically, the encoding process can be expressed as c = m * G, where 'c' is the codeword and 'm' is the vector of information bits.

Decoding involves the use of the parity-check matrix (H) to identify and correct errors. The received codeword is multiplied by the transpose of the parity-check matrix (HT). If the result is a zero vector, no errors are detected. Otherwise, the non-zero syndrome obtained is used to locate and correct errors.

Linear codes can detect errors when the minimum Hamming distance (d) is greater than one. If errors are detected, the code can correct errors if the minimum Hamming distance is such that (d-1)/2 errors or fewer have occurred. This property is crucial for maintaining data integrity in the presence of noise during transmission.
In summary, linear codes play a vital role in ensuring reliable communication by providing mechanisms for encoding, decoding, and error detection/correction. Their mathematical structure, involving generator and parity-check matrices, enables efficient and effective handling of errors in various communication systems.

The functions of our code are the following ones:

def compute_Gcan_and_H(generators):
    # Computes the Canonical Generating Matrix (Gcan) and Control Matrix (H) from given generators
    # Handles errors and returns None if invalid input or matrix is not invertible
    # Returns Gcan, H if successful, else None

def parameters(Hcan):
    # Computes various parameters (length, dimension, size, delta, error detection, error correction)
    # from the given Control Matrix (Hcan)
    # Returns a tuple with the computed values

def codifying(Gcan, bits):
    # Codifies a list of bits using the Canonical Generating Matrix (Gcan)
    # Returns the coded bits as a list

def detect_and_decodifying(Gcan, C_bits):
    # Detects errors and decodes the given coded bits using Gcan
    # Returns the decoded bits if successful, else None

def detect_and_correct(Gcan, C_bits):
    # Detects and corrects errors in the coded bits using Gcan
    # Returns the corrected and decoded bits if successful, else None

Finally, in the main of the program, we provide some examples and tests of the functions.
