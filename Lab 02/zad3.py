from saport.simplex.model import Model

model = Model("zad3")

x1 = model.create_variable("x1")
x2 = model.create_variable("x2")

model.add_constraint(5 * x1 + 15 * x2 >= 50)
model.add_constraint(20 * x1 + 5*x2 >= 40)
model.add_constraint(15 * x1 + 2 * x2 <= 60)

model.minimize(8*x1 + 4*x2)

print("Before solving:")
print(model)
solution = model.solve()
print("Solution: ")
print(solution)
