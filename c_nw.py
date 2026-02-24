import b_submatrix as b

class SeqPair:
    def __init__(self, seq1, seq2):
        self.seq1 = seq1
        self.seq2 = seq2
    
    def _compute_matrices(self, sub_matrix, gap_penalty):
        '''
        This is a hidden method (i.e. it should not be called by users of the class, only internally by other methods of the class), denoted by the convention of starting its name with a '_' character.
        This method initializes and fills two matrices F and T to store the values and the directions for the NW algorithm.
        We decide to link the first sequence to the columns of the matrices (i.e. the number of columns depends on the length of the first sequence), and to link the second sequence to the rows.
        
        In the matrix F, we store integers. In the matrix T, we store the following values:
            top-left cell: 'stop'
            value coming from left: 'left'
            value coming from above: 'up'
            value coming from diagonal: 'diagonal'
        '''
        
        # First, we initialize the matrices F and T, giving them the correct shape
        # As filler values, we use the value that we would have to store in the top-left cell, to avoid having to manually initialize it later
        
        # Option 1: Using two nested for loops to append values and rows
        '''
        F = []
        for i in range(len(self.seq2) + 1):
            row = []
            for j in range(len(self.seq1) + 1):
                row.append(0)
            F.append(row)
        '''
        
        # Option 2: Using list and integer multiplication to create the row without the inner for loop
        '''
        F = []
        for i in range(len(self.seq2) + 1):
            F.append([0] * (len(self.seq1) + 1))
        '''
        
        # Option 3: Using a nested list comprehension
        F = [[0 for j in range(len(self.seq1) + 1)] for i in range(len(self.seq2) + 1)]
        T = [['stop' for j in range(len(self.seq1) + 1)] for i in range(len(self.seq2) + 1)]
        
        # Next, we initialize the first row ...
        for j in range(1, len(F[0])):
            F[0][j] = gap_penalty * j
            T[0][j] = 'left'
        
        # ... and the first column of both matrices
        for i in range(1, len(F)):
            F[i][0] = gap_penalty * i
            T[i][0] = 'up'
        
        # Finally, we use a nested loop to fill the rest of the cells
        for i in range(1, len(F)):
            for j in range(1, len(F[i])):
                
                # Option 1: Use three variables to store the choices for the values, then use an if elif else to get the correct direction
                '''
                up = F[i-1][j] + gap_penalty
                left = F[i][j-1] + gap_penalty
                diagonal = F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]]
                F[i][j] = max(up, left, diagonal)
                if F[i][j] == diagonal:
                    T[i][j] = 'diagonal'
                elif F[i][j] == left:
                    T[i][j] = 'left'
                else: #F[i][j] == up
                    T[i][j] = 'up'
                '''
                # The order in which we wrote the if elif else conditions will prioritize 'diagonal' over 'left' over 'up' in case of equal values, since the first condition to be True will be selected
                
                # Option 2: Use a list to store the choices for the values, then use an if elif else to get the correct direction
                '''
                choice = []
                choice.append(
                    F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]]
                )
                choice.append(
                    F[i][j-1] + gap_penalty
                )
                choice.append(
                    F[i-1][j] + gap_penalty
                )
                F[i][j] = max(choice)
                if F[i][j] == choice[0]:
                    T[i][j] = 'diagonal'
                elif F[i][j] == choice[1]:
                    T[i][j] = 'left'
                else:
                    T[i][j] = 'up'
                '''
                # The order in which we wrote the if elif else conditions will prioritize 'diagonal' over 'left' over 'up' in case of equal values. However, we need to make sure that we append values in the correct order in the choice list
                
                # Option 3: Use a list to store the choices for the values, then use the function index to access a second list and get the correct direction
                '''
                choice = []
                directions = ['diagonal','up','left']
                choice.append(
                    F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]]
                )
                choice.append(
                    F[i-1][j] + gap_penalty
                )
                choice.append(
                    F[i][j-1] + gap_penalty
                )
                F[i][j] = max(choice)
                
                index = choice.index(F[i][j])
                T[i][j] = directions[index]
                '''
                # The order in which we append values in the choice list will prioritize 'diagonal' over 'left' over 'up', since the index function will return the index of the first occurrance of the value in the choice list. However, we need to make sure that the order of the element in the directions list is correct
                
                # Option 4: Use a dictionary to map the values to the corresponding directions, then use the max key to get the correct direction
                '''
                choice = {}
                choice[F[i-1][j] + gap_penalty] = 'up'
                choice[F[i][j-1] + gap_penalty] = 'left'
                choice[F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]]] = 'diagonal'
                
                F[i][j] = max(choice.keys())
                T[i][j] = choice[F[i][j]]
                '''
                # The order in which we store values in the dictionary will prioritize 'diagonal' over 'left' over 'up', since in case of equal values the last item to be added will overwrite the previous ones
                
                # Option 5: Use tuples to link values and directions, then use the max function to get the best tuple
                up = F[i-1][j] + gap_penalty, 1, 'up'
                left = F[i][j-1] + gap_penalty, 2, 'left'
                diagonal = F[i-1][j-1] + sub_matrix[self.seq1[j-1], self.seq2[i-1]], 3, 'diagonal'
                
                F[i][j], _, T[i][j] = max(up, left, diagonal)
                # The order in which we store values in the dictionary will prioritize 'diagonal' over 'left' over 'up', thanks to the middle hardcoded values we put in the second position of the tuples
                
        return F, T

    def nw(self, sub_matrix, gap_penalty):
        '''
        This method is called by users of the class to perform the nw algorithm, obtaining as result the two aligned (i.e. gapped) sequences and the corresponding score.
        '''
        # First, we call the hidden method to compute the matrices
        F, T = self._compute_matrices(sub_matrix, gap_penalty)
        
        # The final score is extracted from the final cell of the matrix F
        score = F[-1][-1]
        
        # For the backtracking, we do not know a priori the number of steps needed. For this reason, we need a while loop
        
        # We start the iteration from the final cell of the matrix T
        i = len(T)-1
        j = len(T[0])-1
        # Either we use the shape of the matrix of the shape of the sequences
        #i = len(self.seq2)
        #j = len(self.seq1)
        
        aln1, aln2 = "", ""
        
        # The while guard can be implemented in different ways.
        #while (i, j) != (0, 0):
        #while i != 0 or j != 0:
        #while not(i == 0 and j == 0):
        while T[i][j] != 'stop':
            if T[i][j] == 'diagonal':
                aln2 = self.seq2[i - 1] + aln2
                aln1 = self.seq1[j - 1] + aln1
                i -= 1
                j -= 1
            elif T[i][j] == 'up':
                aln1 = '-' + aln1
                aln2 = self.seq2[i - 1] + aln2
                i -= 1
            else:# T[i][j] == 'left':
                aln1 = self.seq1[j - 1] + aln1
                aln2 = '-' + aln2
                j -= 1
                
        return aln1, aln2, score
        

if __name__ == "__main__":
    test1 = SeqPair("TCA", "TA")
    sub_matrix = b.SubstitutionMatrix("TTM.txt")
    gap_penalty = -2
    aln1, aln2, score = test1.nw(sub_matrix, gap_penalty)
    print(aln1)
    print(aln2)
    print(score)