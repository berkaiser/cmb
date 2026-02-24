import sys

def glob_matrices(s1, s2, matrix, gap):
    '''Function to create the matrices F and P'''
    F = [ [ 0 for col in range(len(s2)+1) ] for row in range(len(s1)+1) ]
    P = [ ['' for col in range(len(s2)+1) ] for row in range(len(s1)+1) ]
    for i in range(1,len(s1)+1):
        F[i][0], P[i][0] = gap * i, 'u'
    for j in range(1,len(s2)+1):
        F[0][j], P[0][j] = gap * j, 'l'
    for i in range(1,len(s1)+1):
        for j in range(1,len(s2)+1):
            su = F[i-1][j] + gap , 'u'
            sl = F[i][j-1] + gap , 'l'
            sd = F[i-1][j-1] + matrix[s1[i-1]+s2[j-1]] , 'd'
            F[i][j] , P[i][j] = max(su,sl,sd)
    return F, P
# -----------------------------------------------

# 1. Backtracking fonksiyonu (İstenen çıktı: en iyi hizalama ve skor)
def get_best_alignment(seq1, seq2, F, P):
    aln1, aln2 = "", ""
    i, j = len(seq1), len(seq2)
    score = F[i][j] # Küresel hizalamada en iyi skor sağ alttadır.

    while i > 0 or j > 0:
        if P[i][j] == 'd':
            aln1 = seq1[i-1] + aln1
            aln2 = seq2[j-1] + aln2
            i -= 1; j -= 1
        elif P[i][j] == 'u':
            aln1 = seq1[i-1] + aln1
            aln2 = "-" + aln2
            i -= 1
        elif P[i][j] == 'l':
            aln1 = "-" + aln1
            aln2 = seq2[j-1] + aln2
            j -= 1
        else: break
    return aln1, aln2, score

# 4. Veri Importu (Sınavdaki dosya ismine göre ayarla)
try:
    from input_data_07_02_2023 import template, targets, g, PAM250_dict, BLOSUM62_dict
except ImportError:
    # Eğer dosya yoksa kodun içinde tanımlananları kullanır
    from __main__ import template, targets, g, PAM250_dict, BLOSUM62_dict

# 5. Kullanıcı Seçimi (Klavye girişi)
choice = input("Matris seçin (PAM veya BLOSUM): ").upper().strip()

if "PAM" in choice:
    sub_matrix = PAM250_dict
    matrix_label = "PAM250"
elif "BLOSUM" in choice:
    sub_matrix = BLOSUM62_dict
    matrix_label = "BLOSUM62"
else:
    print("Geçersiz seçim.")
    sys.exit()

# 2, 3 ve 4. Maddeler: Hizalamaları yap ve yazdır
results = []
for target in targets:
    F, P = glob_matrices(template, target, sub_matrix, g)
    a1, a2, s = get_best_alignment(template, target, F, P)
    results.append((a1, a2, s))

# Çıktılar
print(f"\nKullanılan Matris: {matrix_label}")
for idx, (a1, a2, s) in enumerate(results, 1):
    print(f"\nTarget {idx} Hizalaması:")
    print(f"Seq1: {a1}")
    print(f"Seq2: {a2}")
    print(f"Skor: {s}")

# En iyi skorlu olanı bul (Madde 4'ün sorusu)
best_score = max([r[2] for r in results])
print(f"\n{matrix_label} için en iyi skor: {best_score}")