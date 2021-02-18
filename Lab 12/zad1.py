import evm

c = [evm.fill_comparison_matrix_from_upper_triangular([[0, 1 / 7, 1 / 5], [0, 0, 3], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 5, 9], [0, 0, 4], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 4, 1 / 5], [0, 0, 1 / 9], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 9, 4], [0, 0, 1 / 4], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 1, 1], [0, 0, 1], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 6, 4], [0, 0, 1 / 3], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 9, 6], [0, 0, 1 / 3], [0, 0, 0]]),
     evm.fill_comparison_matrix_from_upper_triangular([[0, 1 / 2, 1 / 2], [0, 0, 1], [0, 0, 0]])]

cv = []
for i in range(len(c)):
    cv.append(evm.evm(c[i]))

cp = evm.fill_comparison_matrix_from_upper_triangular([[0, 4, 7, 5, 8, 6, 6, 2],
                                                       [0, 0, 5, 3, 7, 6, 6, 1/3],
                                                       [0, 0, 0, 1/3, 5, 3, 3, 1/5],
                                                       [0, 0, 0, 0, 6, 3, 4, 1/2],
                                                       [0, 0, 0, 0, 0, 1/3, 1/4, 1/7],
                                                       [0, 0, 0, 0, 0, 0, 1/2, 1/5],
                                                       [0, 0, 0, 0, 0, 0, 0, 1/5],
                                                       [0, 0, 0, 0, 0, 0, 0, 0]])

cpv = evm.evm(cp)

houses = [0, 0, 0]
for h in range(len(houses)):
    for i in range(0,len(cpv)):
        houses[h] += cv[i][h] * cpv[i]

for i in range(len(houses)):
    print("Dom", i + 1, ":", houses[i])

# Ranking domow:
# Dom 2 > Dom 1 > Dom 3

