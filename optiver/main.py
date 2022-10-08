from solver import Solver

def main():

    question_1_boundary = [(-2,2), (-1,2), (0,2), (1,2), (2,2), 
             (-2,1), (2,1), (-2,0), (2,0), (-2,-1), (2, -1),
             (-2,-2), (-1,-2), (0,-2), (1,-2), (2,-2)]

    # values are normalized such that the speed of the ant is 1cm/s
    question_3_function_params = [0.25, 3, 0.25, 4, 1]

    solver_1 = Solver(question_1_boundary)
    solver_3 = Solver(question_3_function_params, given_boundary_nodes=False)

    expected_number_of_steps_1 = solver_1.expected_number_of_steps(None)
    expected_number_of_steps_3 = solver_3.expected_number_of_steps(None)

    print("====================")
    print(expected_number_of_steps_1)
    print("====================")
    print(expected_number_of_steps_3)
    print("====================")

if __name__ == "__main__":
    main()
