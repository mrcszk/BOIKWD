import evm

c = [evm.fill_comparison_matrix_from_upper_triangular([[0, 1 / 5, 2, 4], [0, 0, 1/7, 1/9], [0, 0, 0, 2], [0, 0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 1, 1/6, 1/3], [0, 0, 1/6, 1/3], [0, 0, 0, 3], [0, 0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 4, 1/6, 1/8], [0, 0, 1/7, 1/9], [0, 0, 0, 1/2], [0, 0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 1/6, 1, 1/6], [0, 0, 6, 1], [0, 0, 0, 1/6], [0, 0, 0, 0]])]

cp = evm.fill_comparison_matrix_from_upper_triangular([[0, 5, 3, 4], [0, 0, 4, 1], [0, 0, 0, 2], [0, 0, 0, 0]])

cv = []
for i in range(len(c)):
    cv.append(evm.evm(c[i]))

cpv = evm.evm(cp)

hotels = [0, 0, 0, 0]
for h in range(len(hotels)):
    for i in range(0,len(cpv)):
        hotels[h] += cv[i][h] * cpv[i]

for i in range(len(hotels)):
    print("Hotel", i + 1, ":", hotels[i])

# Ranking hoteli
# Hotel 3 > Hotel 4 >> Hotel 2 > Hotel 1
