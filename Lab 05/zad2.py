from saport.simplex.model import Model
from saport.simplex.analyser import Analyser

model = Model("zad2")

x1 = model.create_variable("x1")  # Ławka
x2 = model.create_variable("x2")  # Stół
x3 = model.create_variable("x3")  # Krzesło

model.add_constraint(8 * x1 + 6 * x2 + 1 * x3 <= 960)
model.add_constraint(8 * x1 + 4 * x2 + 3 * x3 <= 800)
model.add_constraint(4 * x1 + 3 * x2 + 1 * x3 <= 320)

model.maximize(60 * x1 + 30 * x2 + 20 * x3)

print("******************MODEL PRIMAL******************")
print(model)

dual = model.dual()
print("******************MODEL DUAL******************")
print(dual)

solution = model.solve()
print("******************SOLUTION******************")
print(solution)

print("******************ANALYSIS******************")
analyser = Analyser()
analysis_results = analyser.analyse(solution)
analyser.interpret_results(solution, analysis_results)
