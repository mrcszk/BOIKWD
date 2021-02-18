import logging
from saport.simplex.model import Model


def run():
    model = Model("example_01_solvable")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")
    x3 = model.create_variable("x3")

    model.add_constraint(-1*x1 - 2*x2 - 1*x3 >= -5)
    model.add_constraint(-1*x1 - 1*x2 - 1*x3 >= -4)
    model.add_constraint(0*x1 + 1*x2 + 2*x3 <= 1)

    model.minimize(-1*x1 - 3*x2 - 2*x3)

    try:
        solution = model.solve()
    except:
        raise AssertionError("This problem has a solution and your algorithm hasn't found it!")

    logging.info(solution)

    assert (solution.assignment == [3.0, 1.0, 0.0, 0.0, 0.0, 0.0]), "Your algorithm found an incorrect solution!"

    logging.info("Congratulations! This solution seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()

