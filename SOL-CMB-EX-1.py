import sys

def create_matrices(seq1, seq2, substitution_matrix, gap_penalty):
    #Initialize the matrix with all 0s
    F = [ [ 0 for col in range(len(seq2) + 1) ] for row in range(len(seq1) + 1) ]
    T = [ ['' for col in range(len(seq2) + 1) ] for row in range(len(seq1) + 1) ]
    #Fill the matrix
    for i in range(1, len(seq1) + 1):
        for j in range(1, len(seq2) + 1):
            su = F[i-1][j] + gap_penalty, 'u'
            sl = F[i][j-1] + gap_penalty, 'l'
            sd = F[i-1][j-1] + substitution_matrix[seq1[i-1]+seq2[j-1]], 'd'
            s0 = 0, ''
            F[i][j], T[i][j] = max(su,sl,sd,s0)
    return F, T

# 1. Backtracking
def get_alignments(seq1, seq2, F, T, threshold):
    alignments = []
    for i in range(len(F)):
        for j in range(len(F[0])):
            if F[i][j] >= threshold:
                score = F[i][j]
                aln1 = ""
                aln2 = ""
                curr_i, curr_j = i, j
                
                # Skor 0 olana kadar geri git
                while curr_i > 0 and curr_j > 0 and F[curr_i][curr_j] > 0:
                    direction = T[curr_i][curr_j]
                    if direction == 'd':
                        aln1 = seq1[curr_i-1] + aln1
                        aln2 = seq2[curr_j-1] + aln2
                        curr_i -= 1
                        curr_j -= 1
                    elif direction == 'u':
                        aln1 = seq1[curr_i-1] + aln1
                        aln2 = "-" + aln2
                        curr_i -= 1
                    elif direction == 'l':
                        aln1 = "-" + aln1
                        aln2 = seq2[curr_j-1] + aln2
                        curr_j -= 1
                    else:
                        break
                alignments.append((aln1, aln2, score))
    return alignments

# 2. Main Script
if __name__ == "__main__":
    # b) Argüman kontrolü
    if len(sys.argv) < 2:
        print("Error: No threshold provided. Usage: python script.py <threshold>")
        sys.exit(1)
    
    threshold = int(sys.argv[1])
    print(f"User specified threshold: {threshold}")

    # a) input_data.py file)
    try:
        from input_data import create_matrices, template, target
    except ImportError:
        print("input_data.py not found, using dummy sequences for demo.")
        template = "LLALW"
        target = "MALW"


    from input_data import PAM250_dict, gap # Bunların input_data içinde olduğu varsayılıyor
    F, T = create_matrices(template, target, PAM250_dict, gap)
    results = get_alignments(template, target, F, T, threshold)

    if not results:
        print("No alignments found with scores higher than or equal to the threshold.")
    else:
        for aln1, aln2, score in results:
            print(f"Alignment 1: {aln1}")
            print(f"Alignment 2: {aln2}")
            print(f"Score: {score}\n")