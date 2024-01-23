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

How to Use:

    Clone the repository:

        git clone https://github.com/RogerCivit17/linearcodes.git

    In the file "linearcodes.py" are all these functions that we have explained bellow.

    So you only have to execute this file if you want to see the results of the different tests or import it to another file if you want to use the functions.

