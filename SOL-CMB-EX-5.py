import sys

# Assume these are imported or defined in exam_test.py as per instructions
class SubstitutionMatrix:
    def __init__(self, filename: str = "TTM.txt") -> None:
        # Implementation provided during exam
        self.data = {} 
    def __getitem__(self, key: tuple[str,str]) -> int:
        # Implementation provided during exam
        return self.data.get(key, 0)

class AlnSeq():
    def __init__(self, s1: str, s2: str, score: int) -> None:
        if len(s1) != len(s2):
            raise ValueError("Length of the two strings must be the same")
        self.s1, self.s2, self.score = s1, s2, score
    def __str__(self) -> str:
        return f"Score: {self.score}\n{self.s1}\n{self.s2}"

class SeqPair:
    def __init__(self, s1: str, s2: str) -> None:
        self.s1, self.s2 = s1, s2

    def _local_matrices(self, matrix: SubstitutionMatrix, gap: int) -> (list,list):
        F = [[ 0 for col in range(len(self.s2)+1)] for row in range(len(self.s1)+1)]
        T = [['' for col in range(len(self.s2)+1)] for row in range(len(self.s1)+1)]
        for row in range(1, len(self.s1)+1):
            for col in range(1, len(self.s2)+1):
                # The prompt provided logic for matrices
                su = F[row-1][col]   + gap , '|'
                sl = F[row]  [col-1] + gap , '-'
                sd = F[row-1][col-1] + matrix[self.s1[row-1], self.s2[col-1]] , '\\'
                s0 = 0, ''
                F[row][col] , T[row][col] = max(su, sl, sd, s0)
        return F, T

    # --- 2. Extending the definition of SeqPair ---
    def smith_waterman(self, matrix: SubstitutionMatrix, gap: int, threshold: int) -> list:
        F, T = self._local_matrices(matrix, gap)
        alignments = []

        # Iterate through F to find scores >= threshold
        for row in range(1, len(self.s1) + 1):
            for col in range(1, len(self.s2) + 1):
                if F[row][col] >= threshold:
                    # Perform backtrack for this specific end-point
                    curr_score = F[row][col]
                    aln1, aln2 = "", ""
                    i, j = row, col
                    
                    while i > 0 and j > 0 and T[i][j] != '':
                        if T[i][j] == '\\':
                            aln1 = self.s1[i-1] + aln1
                            aln2 = self.s2[j-1] + aln2
                            i -= 1
                            j -= 1
                        elif T[i][j] == '|':
                            aln1 = self.s1[i-1] + aln1
                            aln2 = '-' + aln2
                            i -= 1
                        elif T[i][j] == '-':
                            aln1 = '-' + aln1
                            aln2 = self.s2[j-1] + aln2
                            j -= 1
                    
                    alignments.append(AlnSeq(aln1, aln2, curr_score))
        
        return alignments

# --- 3. Test Main Script ---
def main():
    # 3. Read threshold from command line
    if len(sys.argv) != 2:
        print("Usage: python script.py <threshold>")
        sys.exit(1)
    
    try:
        threshold = int(sys.argv[1])
    except ValueError:
        print("Threshold must be an integer.")
        sys.exit(1)

    # 3a-b. Sequences
    s1 = "IFYNAVWSA"
    s2 = "IFYNAVWSAWWWVYYHAIWPG"
    
    # 3c-d. Parameters
    # Note: In the actual exam, provide the correct path to the PAM250 file
    sub_matrix = SubstitutionMatrix("PAM250.txt") 
    gap_penalty = -5 # Gap penalties are usually negative in these contexts

    pair = SeqPair(s1, s2)
    results = pair.smith_waterman(sub_matrix, gap_penalty, threshold)

    # Print all found alignments
    if not results:
        print(f"No local alignments found with score >= {threshold}")
    else:
        for aln in results:
            print(aln)
            print("-" * 20)

if __name__ == "__main__":
    main()