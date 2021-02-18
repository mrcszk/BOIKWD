from saport.simplex.model import Model
from saport.simplex.analyser import Analyser

model = Model("zad1")

x1 = model.create_variable("x1")  # model SS
x2 = model.create_variable("x2")  # model S
x3 = model.create_variable("x3")  # model O

model.add_constraint(2 * x1 + 2 * x2 + 5 * x3 <= 40)
model.add_constraint(1 * x1 + 3 * x2 + 2 * x3 <= 30)
model.add_constraint(3 * x1 + 1 * x2 + 3 * x3 <= 30)

model.maximize(32 * x1 + 24 * x2 + 48 * x3)
print("******************MODEL PRIMAL******************")
print(model)

dual = model.dual()
print("******************MODEL DUAL******************")
print(dual)

solution = model.solve()
print("******************SOLUTION******************")
print(solution)

print("******************ANALYSIS******************")
dual_solution = dual.solve()
analyser = Analyser()
analysis_results = analyser.analyse(solution)
analyser.interpret_results(solution, analysis_results)
