import exam_text_25_07_18 as exam

class SequencePair(exam.SequencePair):
    def _create_matrices(self):
        # i corresponds to seq2 (rows), j corresponds to seq1 (columns)
        n = len(self.seq2)
        m = len(self.seq1)

        # 1. Initialize matrices with dimensions (n+1) x (m+1)
        self.F = [[0 for _ in range(m + 1)] for _ in range(n + 1)]
        # Use empty string as the "stop" signal to match parent _backtracking
        self.T = [["" for _ in range(m + 1)] for _ in range(n + 1)]

        self.best_aln_score = 0
        self.best_aln_start = (0, 0)

        # 2. Fill the matrices using Smith-Waterman
        for i in range(1, n + 1):
            for j in range(1, m + 1):
                char1 = self.seq1[j-1]
                char2 = self.seq2[i-1]
                
                # Calculate possible scores
                match = self.F[i-1][j-1] + self.matrix[char1, char2]
                delete = self.F[i-1][j] + self.gap  # Up (Gap in seq1)
                insert = self.F[i][j-1] + self.gap  # Left (Gap in seq2)
                
                # Smith-Waterman: max includes 0
                score = max(0, match, delete, insert)
                self.F[i][j] = score

                # 3. Set Traceback pointers (MUST match 'd', 'l', 'u' for parent class)
                if score == 0:
                    self.T[i][j] = "" # Stop backtracking here
                elif score == match:
                    self.T[i][j] = 'd'
                elif score == insert:
                    self.T[i][j] = 'l'
                else: # score == delete
                    self.T[i][j] = 'u'

                # 4. Track the absolute best score and its coordinates
                if score >= self.best_aln_score:
                    self.best_aln_score = score
                    self.best_aln_start = (i, j)

if __name__ == "__main__":
    # a. Create SubstitutionMatrix from PAM250.txt
    try:
        sub_matrix = exam.SubstitutionMatrix("PAM250.txt")
        
        # b. Create and print SequencePair
        seq1 = "AAAAACCAACCAAAAA"
        seq2 = "RRRRCCCCRRRR"
        gap_penalty = -5

        pair = SequencePair(seq1, seq2, sub_matrix, gap_penalty)
        print(pair)
    except FileNotFoundError:
        print("Error: PAM250.txt not found. Please ensure it's in the same directory.")