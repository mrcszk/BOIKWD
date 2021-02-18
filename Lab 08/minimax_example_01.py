from minimax_example import run_example
from saport.minimax.model import Equilibrium, Strategy

eq = Equilibrium(1.0, Strategy([0,1,0,0]), Strategy([0,0,1,0,0]))

# jeśli nie działa zmień ścieżkę na bezwzględną!
run_example("D:/V/BOIKWD/Lab 10/games/4_5_pure.txt", [eq], eq)