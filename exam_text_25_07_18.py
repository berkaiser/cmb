'''
Read carefully the provided module "A_exam_text.py" and write a new script to implement the following requests:
1. Import the module;

2. Extend the definition of the class SequencePair;

3. Override the method called "_create_matrices" such that:
    a. It correctly computes the matrices F and T needed for the Smith-Waterman algorithm
    b. It correctly identifies the score of the best local alignment
    c. It correctly identifies the starting position for the backtracking part of the Smith-Waterman algorithm

4. Write a small main in your script to test your code. Specifically, the main should:
	a. Create an object of type SubstitutionMatrix, reading from the file "PAM250.txt" (provided together with the module);
	b. Create and print an object of type SequencePair (you can test with these two sequences "AAAAACCAACCAAAAA", "RRRRCCCCRRRR" and a gap penalty of -5);

Suggestion: Try to understand how the class SequencePair works as it is before overriding the method needed to make it work properly.
'''

class SubstitutionMatrix:
    def __init__(self, filename):
        '''Read matrix from a txt file and create a dictionary'''
        with open(filename) as reader:
            characters = reader.readline().split()
            self.values = {}
            
            for line in reader:
                line = line.split()
                char1 = line[0]
                for char2,val in zip(characters, line[1:]):
                    self.values[char1, char2] = int(val)

    def __getitem__(self, key):
        '''Access the matrix with a key in the form (char1, char2)'''
        return self.values[key]

class SequencePair:
    def __init__(self, seq1, seq2, matrix, gap):
        '''Initialize object'''
        # Set attributes from parameters
        self.seq1 = seq1
        self.seq2 = seq2
        self.matrix = matrix
        self.gap = gap
        
        # Compute local alignment
        self._create_matrices()
        self._backtracking()
    
    def _backtracking(self):
        '''Find local alignment from a given starting position'''
        i, j = self.best_aln_start
        self.aln1, self.aln2 = "", ""
        while self.T[i][j] != '':
            if self.T[i][j] == 'd':
                self.aln1 = self.seq1[j - 1] + self.aln1
                self.aln2 = self.seq2[i - 1] + self.aln2
                i = i - 1
                j = j - 1
            elif self.T[i][j] == 'l':
                self.aln1 = self.seq1[j - 1] + self.aln1
                self.aln2 = "-" + self.aln2
                j = j - 1
            else: # self.T[i][j] == 'u'
                self.aln1 = "-" + self.aln1
                self.aln2 = self.seq2[i - 1] + self.aln2
                i = i - 1
    
    def _create_matrices(self):
        '''Method to be overridden'''
        # Create temporary empty attributes needed only to avoid errors
        self.F, self.T = [[0]], [[""]]
        self.best_aln_score = 0
        self.best_aln_start = 0, 0
    
    def __str__(self):
        '''Print nicely a sequence pair with its alignment'''
        s = "Seq 1: " + self.seq1 + "\n"
        s += "Seq 2: " + self.seq2 + "\n\n"
        s += "Best local alignment:" + "\n"
        s += "\tAln 1: " + self.aln1 + "\n"
        s += "\tAln 2: " + self.aln2 + "\n"
        s += "\tScore: " + str(self.best_aln_score) + "\n"
        return s