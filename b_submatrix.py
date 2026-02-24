import a_hamming as a

class SubstitutionMatrix:
    def __init__(self, filename):
        '''
        We decide to internally save the values of the matrix in a dictionary:
            key: 'AA' (string obtained by concatenating the two characters)
            value: 2 (value corresponding to the substitution)
        '''
        self.matrix = {}
        with open(filename, 'r') as file:
            # The first line of the file is different, we need to read it separately and save the keys it contains
            keys_1 = file.readline().split()
            
            for line in file:
                # For each other line, we separate the row key in the first position from the values in the other positions
                splitted_line = line.split()
                key_2 = splitted_line[0]
                values = splitted_line[1:]
                
                for key_1, value in zip(keys_1, values):
                    # For each matched pair of column key / corresponding value, build the combined key (col + row) and save the value in the dictionary
                    key = key_1 + key_2
                    self.matrix[key] = int(value)
                    
                '''
                The function zip is just one possible syntax to loop over matched lists. It is possible to do so using an index which we use to access both lists:
                
                for i in range(len(keys_1)):
                    key_1 = keys_1[i]
                    value = values[i]
                
                Or to use the enumerate function to have the index (to access the second list elements) and the elements of the first list:
                
                for i, key_1 in enumerate(keys_1):
                    value = values[i]
                '''
    def __getitem__(self, key):
        '''
        We decide that users will access our data structure with a tuple containing a pair of characters. Internally, the __getitem__ method will build the proper key (based on the chosen internal representation of the data) and return the corresponding value.
        '''
        a, b = key
        k = a + b
        # Just like the __init__ method, it is possible to increment the level of control of this function with custom error messages
        if not k in self.matrix:
            raise KeyError(f"Key {key} not in the Substitution Matrix")
        return self.matrix[k]

class AlnSeq(a.AlnSeq):
    '''
    This class 'extends' the old one defined in the file a_hamming.py using the inheritance mechanism. It is now possible to develop additional methods for the new class, while keeping all the old ones.
    '''
    pass
    # Try to implement a method to compute a hamming similarity based on a substitution matrix

if __name__ == "__main__":
    sm = SubstitutionMatrix("TTM.txt")
    print(sm["A","T"])
    old_alnseq = a.AlnSeq("ATC","AGC")
    print(old_alnseq.str1)
    new_alnseq = AlnSeq("ATC","AGC")
    print(new_alnseq.str1)