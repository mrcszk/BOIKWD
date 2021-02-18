import saport.simplex.model as m

model = m.Model("zad4")

# tylko te 5 zmiennych jest wystarczające, bo reszta jest nieoptymalna i nie ma sensu ich używać
# 1*105cm + 1*75cm + 0*35cm => odpad: 20
# 1*105cm + 0*75cm + 2*35cm => odpad: 25
# 0*105cm + 2*75cm + 1*35cm => odpad: 15
# 0*105cm + 1*75cm + 3*35cm => odpad: 20
# 0*105cm + 0*75cm + 5*35cm => odpad: 25

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")
x5 = model.create_variable("x5")


model.add_constraint(x1 + x2 == 150)
model.add_constraint(x1 + 2*x3 + x4 == 200)
model.add_constraint(2 * x2 + x3 + 3 * x4 + 5 * x5 == 150)

model.minimize(20*x1 + 25*x2 + 15*x3 + 20 * x4 + 25 * x5)

print("Before solving:")
print(model)
solution = model.solve()
print("Solution: ")
print(solution)
