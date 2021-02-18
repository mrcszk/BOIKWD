from saport.simplex.model import Model

model = Model("zad4")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")
x3 = model.create_variable("x3")
x4 = model.create_variable("x4")
x5 = model.create_variable("x5")


model.add_constraint(x1 + x2 + 0 * x3 + 0 * x4 + 0 * x5 >= 150)
model.add_constraint(x1 + 0 * x2 + 2*x3 + x4 + 0 * x5 >= 200)
model.add_constraint(0 * x1 + 2 * x2 + x3 + 3 * x4 + 5 * x5 >= 150)

model.minimize(20*x1 + 25*x2 + 15*x3 + 20 * x4 + 25 * x5)

print("Before solving:")
print(model)
solution = model.solve()
print("Solution: ")
print(solution)
