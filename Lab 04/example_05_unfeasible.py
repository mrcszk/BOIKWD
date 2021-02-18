import logging
from saport.simplex.model import Model 

def run():
    #TODO:
    # fill missing test based on the example_01_solvable.py
    # to make the test a bit more interesting:
    # * make the model unfeasible in a way detectable by the 2-phase simplex
    # 
    model = Model("example_05_unfeasible")

    x1 = model.create_variable("x1")
    x2 = model.create_variable("x2")

    model.add_constraint(x1 >= 50)
    model.add_constraint(x2 >= 50)
    model.add_constraint(x1 + x2 <= 60)

    model.minimize(x1 + x2)

    try:
        model.solve()
        raise AssertionError("Your algorithm found a solution to an unfeasible problem. This shouldn't happen...")
    except:
        logging.info("Congratulations! This problem is unfeasible and your algorithm has found that :)")


if __name__ == '__main__':
    logging.basicConfig(level=logging.INFO, format='%(message)s')
    run()
