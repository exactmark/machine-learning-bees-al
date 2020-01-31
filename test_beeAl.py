from unittest import TestCase
from TspDefinition import tsp_world, TspBeeModel
from BeeAl import BeeAl, FlowerPatch
import cProfile
import time


class TestBeeAl(TestCase):

    def make_a_bee(self, world_state=None):
        if world_state:
            return_bee = TspBeeModel(world_state=world_state)
        else:
            square_world = tsp_world().generate_square_tsp_world(4)
            return_bee = TspBeeModel(world_state=square_world)
        return return_bee

    def make_a_patch(self):
        a_bee = self.make_a_bee()
        expected_bees = 20
        return_patch = FlowerPatch(a_bee, num_bees=expected_bees, verbose=True)
        return return_patch

    def test_flower_patch_init(self):
        expected_bees = 20
        this_patch = self.make_a_patch()
        self.assertGreater(len(this_patch.patch_center), 1)
        self.assertGreater(this_patch.center_bee.get_fitness(), 0)
        self.assertGreater(this_patch.get_best_fitness(), 0)
        this_patch.set_bees_to_capacity()
        self.assertEqual(len(this_patch.bees), expected_bees)

    def test_flower_patch_process_time_step(self):
        this_patch = self.make_a_patch()
        this_patch.set_bees_to_capacity()
        this_patch.process_time_step()
        self.assertNotEqual(this_patch.bees[0].solution_string, this_patch.bees[1].solution_string)

    def test_bee_model_find_solution(self):
        a_bee = self.make_a_bee()
        bee_model = BeeAl(a_bee, neighborhood_size=500, verbose=False, fitness_invert=True)
        bee_model.find_solution()
        print(bee_model.solution_list)
        a_bee.world_state: tsp_world
        print(a_bee.world_state.get_solution_length(bee_model.solution_list[0][1]))
        a_bee.world_state.show_solution_map(bee_model.solution_list[0][1])

    def test_first_solomon_bee_al(self):
        start = time.perf_counter()
        solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_025.xml")
        a_bee = self.make_a_bee(world_state=solomon_world)

        bee_model = BeeAl(a_bee, verbose=False, fitness_invert=True,stag_limit=500, num_scouts=30, neighborhood_size=300, number_elite_sites=3, number_best_sites=6)
        bee_model.find_solution()
        print(bee_model.solution_list)
        print(a_bee.world_state.get_solution_length(bee_model.solution_list[0][1]))
        print(time.perf_counter() - start)
        a_bee.world_state.show_solution_map(bee_model.solution_list[0][1])

    def test_third_solomon_bee_al(self):
        start = time.perf_counter()
        solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_100.xml")
        a_bee = self.make_a_bee(world_state=solomon_world)

        bee_model = BeeAl(a_bee, verbose=True, fitness_invert=True,stag_limit=10000, num_scouts=1000, neighborhood_size=1000, number_elite_sites=3, number_best_sites=7)
        bee_model.find_solution()
        print(bee_model.solution_list)
        print(a_bee.world_state.get_solution_length(bee_model.solution_list[0][1]))
        print(time.perf_counter() - start)
        a_bee.world_state.show_solution_map(bee_model.solution_list[0][1])

    def test_first_solomon_bee_al_params(self):
        # (self, solution_model, num_scouts=40, number_elite_sites=5, number_best_sites=10, bees_per_elite=40,
        # bees_per_remaining_best=20, neighborhood_size=5000, stag_limit=200, stop_criteria=default_stop,
        # verbose=False, fitness_invert=False, solution_list_limit=10):
        for num_scouts in [20, 40, 100, 200]:
            for neighborhood_size in [100, 500, 5000]:
                for number_elite_sites in [1, 3, 5]:
                    for num_best_sites in [6, 10, 20]:
                        start = time.perf_counter()
                        solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_025.xml")
                        a_bee = self.make_a_bee(world_state=solomon_world)
                        bee_model = BeeAl(a_bee, num_scouts=num_scouts, neighborhood_size=neighborhood_size,
                                          number_elite_sites=number_elite_sites, number_best_sites=num_best_sites,
                                          verbose=False, fitness_invert=True)
                        bee_model.find_solution()
                        print("num_scouts %i, neighborhood_size %i, number_elite_sites %i, num_best_sites %i" % (
                            num_scouts, neighborhood_size, number_elite_sites, num_best_sites))
                        print(bee_model.solution_list)
                        print("best solution length %.4f" % a_bee.world_state.get_solution_length(
                            bee_model.solution_list[0][1]))
                        a_bee.world_state.show_solution_map(bee_model.solution_list[0][1])
                        print("time %f" % (time.perf_counter() - start))

    def test_first_simple_bee_al_params(self):
        # (self, solution_model, num_scouts=40, number_elite_sites=5, number_best_sites=10, bees_per_elite=40,
        # bees_per_remaining_best=20, neighborhood_size=5000, stag_limit=200, stop_criteria=default_stop,
        # verbose=False, fitness_invert=False, solution_list_limit=10):
        for num_scouts in [20, 40, 100, 200]:
            for neighborhood_size in [100, 500, 5000]:
                for number_elite_sites in [1, 3, 5]:
                    for num_best_sites in [6, 10, 20]:
                        for stag_limit in [10, 200, 500, 1000]:
                            start = time.perf_counter()
                            a_bee = self.make_a_bee()
                            bee_model = BeeAl(a_bee, num_scouts=num_scouts, neighborhood_size=neighborhood_size,
                                              number_elite_sites=number_elite_sites, number_best_sites=num_best_sites,
                                              stag_limit=stag_limit,
                                              verbose=False, fitness_invert=True)
                            bee_model.find_solution()
                            print(
                                "stag_limit %i, num_scouts %i, neighborhood_size %i, number_elite_sites %i, num_best_sites %i" % (
                                stag_limit,
                                num_scouts, neighborhood_size, number_elite_sites, num_best_sites))
                            print(bee_model.solution_list)
                            print("best solution length %.4f" % a_bee.world_state.get_solution_length(
                                bee_model.solution_list[0][1]))
                            a_bee.world_state.show_solution_map(bee_model.solution_list[0][1])
                            print("time %f" % (time.perf_counter() - start))
