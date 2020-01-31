from TspDefinition import tsp_world, TspBeeModel
from BeeAl import BeeAl
import cProfile

square_world = tsp_world().generate_square_tsp_world(4)
a_bee = TspBeeModel(world_state=square_world)

bee_model = BeeAl(a_bee)

cProfile.run("bee_model.find_solution()")
