from unittest import TestCase

from TspDefinition import tsp_world, TspGenAlModel


class TestTspGenAlModel(TestCase):

    def create_tsp_gen_al_model(self):
        return TspGenAlModel(None, self.create_simple_tsp_world())

    def create_simple_tsp_world(self):
        return tsp_world().generate_square_tsp_world(4)

    def test_get_child(self):
        my_model = self.create_tsp_gen_al_model()
        new_child = my_model.get_child(my_model.solution_string[1:] + my_model.solution_string[0:1])
        self.assertNotEqual(my_model, new_child)
        self.assertNotEqual(my_model.solution_string, new_child.solution_string)
        self.assertEqual(my_model.world_state, new_child.world_state)

    def test_get_fitness(self):
        my_model = self.create_tsp_gen_al_model()
        my_model.solution_string = my_model.world_state.get_node_list()
        old_solution = my_model.solution_string
        new_solution = old_solution[-1:] + old_solution[1:-1] + old_solution[0:1]
        new_child = my_model.get_child(new_solution)
        self.assertGreater(my_model.get_fitness(), new_child.get_fitness())

    def test_mutate(self):
        my_model = self.create_tsp_gen_al_model()
        my_model.solution_string = my_model.world_state.get_node_list()
        original_solution = my_model.solution_string.copy()
        my_model.mutate(1)
        self.assertNotEqual(",".join(original_solution), ",".join(my_model.solution_string))

    def test_get_crossover_strings(self):
        my_model = self.create_tsp_gen_al_model()
        my_model.solution_string = my_model.world_state.get_node_list()
        original_solution = my_model.solution_string.copy()
        reversed_solution = original_solution.copy()
        reversed_solution.reverse()
        new_child = my_model.get_child(reversed_solution)
        for x in range(1):
            reproduction_strings = my_model.get_crossover_strings(new_child)
            for repro_string in reproduction_strings:
                print(repro_string)
                self.assertNotEqual(",".join(original_solution), ",".join(repro_string))
                self.assertNotEqual(",".join(reversed_solution), ",".join(repro_string))
