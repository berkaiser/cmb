class AlnSeq:
    def __init__(self, str1, str2):
        # We check all possible errors before doing the initialization
        # If one condition is True, the raise will stop the execution, so the next part of the code do not need an else
        if (type(str1) != str):
            raise TypeError("str1 not string")
        
        if (type(str2) != str):
            raise TypeError("str2 not string")
        
        if len(str1) != len(str2):
            raise ValueError("strings of different length")
        
        # We want to initialize all possible attributes in the __init__ for readability
        self.str1 = str1
        self.str2 = str2
        self.distance = None
    
    def compute_hamming_distance(self):
        # We decide to save the distance as an attribute to avoid computing it twice
        # If we do this, it would make sense to check if we already computed the value at the start of this function
        self.distance = 0
        
        for i in range(len(self.str1)):
            # We need the index to access the corresponding position in both sequences at the same time
            # We cannot do "for el in self.str1"
            if self.str1[i] != self.str2[i]:
                self.distance += 1
            
        return self.distance
    
    def compute_hamming_similarity(self):
        # We compute the similarity by subtracting twice the distance from the total length
        # An alternative would be to do a new loop, and for each character either summing +1 or -1
        if self.distance is None:
            self.compute_hamming_distance()
        
        self.similarity = len(self.str1) - 2*self.distance
        
        return self.similarity
            
            

if __name__ == "__main__":
    # This syntax is used to define the main part of the script
    # During the coding part, use this part to keep testing every function and class that you write. At the end, you can keep only the important parts to solve the exercise / satisfy the requirements.
    test1 = AlnSeq("ACT", "AGT")
    print(test1.compute_hamming_distance()) # Expected: 1
    print(test1.compute_hamming_similarity()) # Expected: 1