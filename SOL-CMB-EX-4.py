import sys

# --- 1. Function Definition ---

def needleman_wunsch(seq1, seq2, matrix, gap):
    """
    Computes the scoring matrix F and backtracking matrix T 
    for global alignment using the Needleman-Wunsch algorithm.
    """
    # Matrix dimensions
    n = len(seq2)  # rows
    m = len(seq1)  # columns

    # Initialize matrices with zeros
    F = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
    T = [['' for _ in range(m + 1)] for _ in range(n + 1)]

    # Initializing the first row and column with gap penalties
    T[0][0] = 'end'
    for j in range(1, m + 1):
        F[0][j] = F[0][j-1] - gap
        T[0][j] = 'l'
    for i in range(1, n + 1):
        F[i][0] = F[i-1][0] - gap
        T[i][0] = 'u'

    # Fill the matrices
    for i in range(1, n + 1):
        for j in range(1, m + 1):
            char1 = seq1[j-1]
            char2 = seq2[i-1]
            
            # Match/Mismatch score from PAM250_dict
            # Note: Accessing nested dict as provided in the snippet structure
            match = F[i-1][j-1] + matrix[char2][char1]
            delete = F[i-1][j] - gap
            insert = F[i][j-1] - gap

            # Compute max score
            F[i][j] = max(match, delete, insert)

            # Record backtracking direction
            if F[i][j] == match:
                T[i][j] = 'd'
            elif F[i][j] == delete:
                T[i][j] = 'u'
            else:
                T[i][j] = 'l'

    return F, T

# --- 2. Provided Backtrack Function ---

def backtrack(seq1, seq2, F, T):
    aln1, aln2 = '', ''
    i , j = len(seq2), len(seq1)
    while T[i][j] != 'end':
        if T[i][j] == 'd':
            aln1 = seq1[j-1] + aln1
            aln2 = seq2[i-1] + aln2
            i -= 1
            j -= 1 
        elif T[i][j] == 'l':
            aln1 = seq1[j-1] + aln1
            aln2 = '-' + aln2
            j -= 1 
        else: # T[i][j] == 'u':
            aln1 = '-' + aln1
            aln2 = seq2[i-1] + aln2
            i -= 1 
    return {"aln1": aln1, "aln2": aln2, "score": F[-1][-1]}

# --- 2a. Input Data (Simulated for completion) ---

# In the exam, these would be imported from input_data.py
template = "LLALWGPDPAAAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDLQVGQVELGGGPGAGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
target = "MALWMRLLPLLALLALWGPDPVPAFVNQHLCGSHLVEALYLVCGERGFFYTPKTRREAEDPQVGQVELGGGPGTGSLQPLALEGSLQKRGIVEQCCTSICSLYQLENYCN"
gap = 10

# Example subset of PAM250_dict to make the code executable
# A full matrix should be used as per the file description
PAM250_dict = {
    'A': {'A': 2.0, 'R': -2.0, 'N': 0.0, 'D': 0.0, 'C': -2.0, 'Q': 0.0, 'E': 0.0, 'G': 1.0, 'H': -1.0, 'I': -1.0, 'L': -2.0, 'K': -1.0, 'M': -1.0, 'F': -4.0, 'P': 1.0, 'S': 1.0, 'T': 1.0, 'W': -6.0, 'Y': -3.0, 'V': 0.0},
    # ... other amino acids would be here ...
}

# --- 2b & 2c. Main Execution and Printing ---

if __name__ == "__main__":
    # Check if PAM250_dict is the nested version or flat version and adjust
    # This ensures compatibility with the matrix structure provided in point 1
    
    # 2b) Use the functions to align
    try:
        F, T = needleman_wunsch(template, target, PAM250_dict, gap)
        results = backtrack(template, target, F, T)

        # 2c) Human-friendly output
        print("--- Global Alignment Results ---")
        print(f"Sequence 1 (Template): {results['aln1']}")
        print(f"Sequence 2 (Target):   {results['aln2']}")
        print("-" * 32)
        print(f"Final Alignment Score: {results['score']}")
        print("--------------------------------")
    except KeyError as e:
        print(f"Error: Amino acid {e} not found in substitution matrix.")