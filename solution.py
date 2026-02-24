# Request 1: Import the module
import exam_text_25_07_18 as a

# Request 2: Extend the class SequencePair
class SequencePair(a.SequencePair):
    def __init__(self, seq1, seq2, sub_matrix, gap_penalty):
        super().__init__(seq1, seq2, sub_matrix, gap_penalty)
    
    # Request 3: Override the method _create_matrices
    def _create_matrices(self):
        self.F, self.T = [], []
        self.best_aln_score = 0
        self.best_aln_start = 0, 0
        
        for i in range(len(self.seq2) + 1):
            row_f = [0] * (len(self.seq1) + 1)
            row_t = [''] * (len(self.seq1) + 1)
            self.F.append(row_f)
            self.T.append(row_t)
        
        for i in range(1, len(self.seq2) + 1):
            for j in range(1, len(self.seq1) + 1):
                diagonal = self.F[i-1][j-1] + self.matrix[self.seq1[j-1], self.seq2[i-1]], 'd'
                left = self.F[i][j-1] + self.gap, 'l'
                up = self.F[i-1][j] + self.gap, 'u'
                zero = 0, ''
                
                # 3.a: This method computes the matrices F and T for the SW algorithm, saving them as attributes
                self.F[i][j], self.T[i][j] = max(diagonal, left, up, zero)
        
                # 3.b-c: We also find the best score and the starting position for the backtracking, saving them as attributes
                if self.best_aln_score < self.F[i][j]:
                    self.best_aln_score = self.F[i][j]
                    self.best_aln_start = i, j
            
# Request 4: Write a main to test the code
if __name__ == "__main__":
    sub_matrix = a.SubstitutionMatrix("PAM250.txt")
    gap_penalty = -5
    object = SequencePair("AAAAACCAACCAAAAA", "RRRRCCCCRRRR", sub_matrix, gap_penalty)
    # Thanks to the implementation of the __str__ method, we can directly print the object
    print(object)