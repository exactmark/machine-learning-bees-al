from GenAl import GenAlMulti
from TspDefinition import tsp_world, TspGenAlModel

if __name__ == "__main__":
    square_world = tsp_world().generate_square_tsp_world(4)
    my_gen_al_model = TspGenAlModel(None, square_world)
    my_gen_al_solver = GenAlMulti(my_gen_al_model, verbose=True)
    my_gen_al_solver.find_solution_with_timeout()
