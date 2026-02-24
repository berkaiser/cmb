import b_submatrix as b

class SeqPair():
    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
    
    def _compute_matrices(self, sub_matrix, gap_penalty):
        F, T = [], []
        # We bind seq1 to the row index i ...
        for i in range(len(self.seq1) + 1):
            F.append([])
            T.append([])
            # ... and seq2 to the column index j
            for j in range(len(self.seq2) + 1):
                F[-1].append(0)
                T[-1].append('stop')
        
        for i in range(1, len(self.seq1) + 1):
            F[i][0] = i * gap_penalty
            # When changing row, we still use an 'up' arrow ...
            T[i][0] = 'up'
        
        for j in range(1, len(self.seq2) + 1):
            F[0][j] = j * gap_penalty
            # ... and when changing column, we still use a 'left' arrow
            T[0][j] = 'left'
        
        # For the for loop we use the corresponding sequences ...
        for i in range(1, len(self.seq1) + 1):
            for j in range(1, len(self.seq2) + 1):
                # ... but the behaviour of up and down does not change
                up = F[i-1][j] + gap_penalty, 'up'
                left = F[i][j-1] + gap_penalty, 'left'
                diagonal = F[i-1][j-1] + sub_matrix[self.seq1[i-1], self.seq2[j-1]], 'diagonal'
                
                F[i][j], T[i][j] = max(up, left, diagonal)
        
        return F, T
    
    def nw(self, sub_matrix, gap_penalty):
        F, T = self._compute_matrices(sub_matrix, gap_penalty)
        
        aln1, aln2, score = "", "", F[-1][-1]
        
        # For the for loop we use the corresponding sequences ...
        i, j = len(self.seq1), len(self.seq2)
        while T[i][j] != 'stop':
            if T[i][j] == 'diagonal':
                aln1 = self.seq1[i-1] + aln1
                aln2 = self.seq2[j-1] + aln2
                i -= 1
                j -= 1
            elif T[i][j] == 'left':
                aln1 = '-' + aln1
                aln2 = self.seq2[j-1] + aln2
                # ... but the behaviour of up and down does not change
                j -= 1
            else:
                aln1 = self.seq1[i-1] + aln1
                aln2 = '-' + aln2
                i -= 1
        
        return aln1, aln2, score

if __name__ == "__main__":
    seqpair = SeqPair("TCA", "TA")
    sub_matrix = b.SubstitutionMatrix("TTM.txt")
    aln1, aln2, score = seqpair.nw(sub_matrix, -2)
    print(aln1)
    print(aln2)
    print(score)
    