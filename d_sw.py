import c_nw as c
import b_submatrix as b

# We extend the definition of the class SeqPair using inheritance
class SeqPair(c.SeqPair):
    def __init__(self, seq1, seq2):
        '''
        We overwrite the __init__ method of the old class by defining a new one. However, the new one simply calls the __init__ of the super class and does nothing else.
        '''
        super().__init__(seq1, seq2)
        
    def _compute_local_matrices(self, sub_matrix, gap_penalty):
        # Initialize the matrices
        F, T = [], []
        for i in range(len(self.seq2) + 1):
            row_f = [0] * (len(self.seq1) + 1)
            F.append(row_f)
            row_t = ['stop'] * (len(self.seq1) + 1)
            T.append(row_t)
        
        # Since the matrices are initialized with 0 and 'stop', we do not have to do anything else for the first row and first column
        
        # Fill the rest of the matrices
        for i in range(1, len(F)):
            for j in range(1, len(F[0])):
                
                diagonal = F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]], 0, 'diagonal'
                up = F[i-1][j] + gap_penalty, 0, 'up'
                left = F[i][j-1] + gap_penalty, 0, 'left'
                zero = 0, 1, 'stop' # If all values are negative, we put a 0 and a 'stop' in the cell
                
                F[i][j], _, T[i][j] = max(diagonal, left, up, zero)
        
        return F, T
    
    def sw(self, sub_matrix, gap_penalty):
        F, T = self._compute_local_matrices(sub_matrix, gap_penalty)
        
        # We start by looping over the matrix F to find the cell with the highest value, storing both the score and its indices, which are needed to start the backtracking loop
        score = F[1][1]
        start_i, start_j = 1, 1
        for i in range(1, len(self.seq2) + 1):
            for j in range(1, len(self.seq1) + 1):
                if F[i][j] > score:
                    score = F[i][j]
                    start_i, start_j = i, j
        i = start_i
        j = start_j
        
        # This part of the algorithm is identical to the NW
        aln1, aln2 = "", ""
        while not(T[i][j] == 'stop'): # Only correct condition for stopping
            if T[i][j] == 'diagonal':
                aln1 = self.seq1[j-1] + aln1
                aln2 = self.seq2[i-1] + aln2
                i -= 1
                j -= 1
            elif T[i][j] == 'up':
                aln1 = '-' + aln1
                aln2 = self.seq2[i-1] + aln2
                i -= 1
            else:
                aln1 = self.seq1[j-1] + aln1
                aln2 = '-' + aln2
                j -= 1
        
        
        return aln1, aln2, score
        

if __name__ == "__main__":
    test = SeqPair("TGA", "GA")
    sub_matrix = b.SubstitutionMatrix("TTM.txt")
    gap_penalty = -2
    aln1, aln2, score = test.nw(sub_matrix, gap_penalty)
    print("Global alignment")
    print(aln1)
    print(aln2)
    print(score)
    aln1, aln2, score = test.sw(sub_matrix, gap_penalty)
    print("Local alignment")
    print(aln1)
    print(aln2)
    print(score)
    