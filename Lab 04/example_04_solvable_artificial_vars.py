import logging
from saport.simplex.model import Model

def run():
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the solver use artificial variables!
    model = Model("example_04_solvable_artificial_vars")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 + x2 <= 100)
    model.add_constraint(-1*x1 + 2*x2 >= 20)

    model.maximize(2*x1 + x2)

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment == [60.0, 40.0]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
