import logging
from saport.simplex.model import Model


def run():
    model = Model("example_03_unbounded ")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(-0.3*x1 - 0.4 * x2 <= 240)
    model.add_constraint(-0.2*x1 - 0.1 * x2 <= 100)
    model.add_constraint(0.5*x1 + 0.3 * x2 >= -290)

    model.maximize(160 * x1 + 120 * x2)

    try:
        solution = model.solve()
    except Exception as e:
        logging.info("Solver throw an Exception: " + e.__str__())
        assert (e.__eq__("Linear programming model is unbounded")), \
            "Your Exception -> \"Linear programming model is unbounded\""

    logging.info("Congratulations! This exception seems to be alright :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
