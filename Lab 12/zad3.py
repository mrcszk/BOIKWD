import evm

price = [evm.fill_comparison_matrix_from_upper_triangular([[0, 1 / 5, 3], [0, 0, 8], [0, 0, 0]]),
         evm.fill_comparison_matrix_from_upper_triangular([[0, 3, 1 / 5], [0, 0, 1 / 8], [0, 0, 0]])]
price_p_v = [0.6, 0.4]

space = [evm.fill_comparison_matrix_from_upper_triangular([[0, 5, 4], [0, 0, 2], [0, 0, 0]]),
         evm.fill_comparison_matrix_from_upper_triangular([[0, 1, 6], [0, 0, 6], [0, 0, 0]])]
space_p_v = [0.3, 0.7]

safety = evm.fill_comparison_matrix_from_upper_triangular([[0, 3, 1/6], [0, 0, 1/7], [0, 0, 0]])

price_v = []
space_v = []

for i in range(2):
    price_v.append(evm.evm(price[i]))
    space_v.append(evm.evm(space[i]))

price_criterion = [0]*len(price_v[0])
space_criterion = [0]*len(space_v[0])
for i in range(0, len(price_v[0])):
    price_criterion[i] = price_v[0][i]*price_p_v[0] + price_v[1][i]*price_p_v[1]
    space_criterion[i] = space_v[0][i]*space_p_v[0] + space_v[1][i]*space_p_v[1]
safety_criterion = evm.evm(safety)
criterion = [price_criterion, safety_criterion, space_criterion]

print("Kryterium ceny: ", price_criterion)
print("Kryterium bezpieczenstwa: ", safety_criterion)
print("Kryterium pojemnosci: ", space_criterion)

cp = evm.fill_comparison_matrix_from_upper_triangular([[0, 6, 2], [0, 0, 4], [0, 0, 0]])
cpv = evm.evm(cp)

cars = [0, 0, 0]
for c in range(len(cars)):
    for i in range(0,len(cpv)):
        cars[c] += criterion[i][c] * cpv[i]

for i in range(len(cars)):
    print("Samochod", i + 1, ":", cars[i])

# Ranking samochodow
# Samochod 3 > Samochod 2 > Samochod 1
