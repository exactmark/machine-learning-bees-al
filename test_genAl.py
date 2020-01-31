# Course: CS7267
# Student name: Mark Fowler
# Student ID: mfowle19
# Assignment #: #4
# Due Date: November 6, 2019
# Signature:
# Score:

import random
from unittest import TestCase

from GenAl import ExampleSquaredModel, GenAl, KnapsackModel, GenAlMulti
from TspDefinition import tsp_world, TspGenAlModel
import time

class TestGenAl(TestCase):
    # def test___create_population(self):
    #     myGenAlModel = GenAl(ExampleSquaredModel)
    #     self.assertEqual(10, myGenAlModel.carrying_capacity)
    #     # for model in myGenAlModel.population:
    #     #     print(model.get_fitness())

    def test_find_solution(self):
        random.seed(1)
        myGenAlModel = GenAl(ExampleSquaredModel())
        # self.assertEqual(10, myGenAlModel.carrying_capacity)
        found_solution = myGenAlModel.find_solution()
        print(found_solution.get_fitness())
        print(found_solution.solution_string)

    def test_find_solution2(self):
        # for x in range(20):
        #     random.seed(x)
        myGenAlModel = GenAl(KnapsackModel())
        # self.assertEqual(10, myGenAlModel.carrying_capacity)
        found_solution = myGenAlModel.find_solution()
        print(found_solution.get_fitness())

        print(found_solution.solution_string)

    def test_find_solution3(self):
        myGenAlModel = GenAlMulti(KnapsackModel(), generations=200)
        # myGenAlModel = GenAlMulti(KnapsackModel)
        found_solution = myGenAlModel.find_solution()
        print(found_solution.get_fitness())
        print(found_solution.solution_string)

    def test_find_solution_with_timeout(self):
        for x in range(1):
            random.seed(x)
            myGenAlModel = GenAlMulti(KnapsackModel(), generations=200, mutation_chance=0.01, islands=5)
            # myGenAlModel = GenAlMulti(KnapsackModel)
            found_solution = myGenAlModel.find_solution_with_timeout()
            print("Found solution %i" % found_solution.get_fitness())
            print(len(found_solution.solution_string))
            print(found_solution.solution_string)

    def test_find_solution_with_timeout_and_bottleneck(self):
        # for x in range(1):
        #     x=4
        #     random.seed(x)
        myGenAlModel = GenAlMulti(KnapsackModel(), generations=200, mutation_chance=0.0001, islands=5)
        # myGenAlModel = GenAlMulti(KnapsackModel)
        found_solution = myGenAlModel.find_solution_with_timeout_and_bottleneck()
        print("Found solution %i" % found_solution.get_fitness())
        print(len(found_solution.solution_string))
        print(found_solution.solution_string)

    def test_simple_tsp_gen_al(self):
        start = time.perf_counter()
        square_world = tsp_world().generate_square_tsp_world(4)
        square_world.show_solution_map(square_world.get_random_solution())
        my_gen_al_model = TspGenAlModel(None, square_world)
        my_gen_al_solver = GenAlMulti(my_gen_al_model, islands=1, verbose=True, fitness_invert=True)
        my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
        print(my_gen_al_solver.solution_list)
        print("time %.4f"%(time.perf_counter()- start))
        square_world.create_gif(my_gen_al_solver.solution_list)

    def test_simple_tsp_gen_al_stacked(self):
        square_world = tsp_world().generate_square_tsp_world(4)
        my_gen_al_model = TspGenAlModel(None, square_world)
        my_gen_al_solver = GenAlMulti(my_gen_al_model, islands=5, verbose=True, fitness_invert=True)
        my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
        print(my_gen_al_solver.stacked_solution_list)
        square_world.create_stacked_gif(my_gen_al_solver.stacked_solution_list)

    def test_first_solomon_gen_al(self):
        # random.seed(0)
        start = time.perf_counter()
        solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_025.xml")
        my_gen_al_model = TspGenAlModel(None, solomon_world)
        solomon_world.show_solution_map(my_gen_al_model.solution_string)
        # print(my_gen_al_model.solution_string)
        my_gen_al_solver = GenAlMulti(my_gen_al_model, islands=1, verbose=True, fitness_invert=True)
        my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
        print(my_gen_al_solver.solution_list)
        print("time %.4f" % (time.perf_counter() - start))
        solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
        solomon_world.create_gif(my_gen_al_solver.solution_list)

    def test_second_solomon_gen_al(self):
        for x in range(10):
            solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_050.xml")
            my_gen_al_model = TspGenAlModel(None, solomon_world)
            solomon_world.show_solution_map(my_gen_al_model.solution_string)
            # print(my_gen_al_model.solution_string)
            my_gen_al_solver = GenAlMulti(my_gen_al_model, islands=1, verbose=True, fitness_invert=True)
            my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
            print(my_gen_al_solver.solution_list)
            solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
            solomon_world.create_gif(my_gen_al_solver.solution_list)

    def test_third_solomon_gen_al(self):
        solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_100.xml")
        my_gen_al_model = TspGenAlModel(None, solomon_world)
        solomon_world.show_solution_map(my_gen_al_model.solution_string)
        # print(my_gen_al_model.solution_string)
        my_gen_al_solver = GenAlMulti(my_gen_al_model, islands=1, population_size=40, verbose=True,
                                      fitness_invert=True)
        my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
        print(my_gen_al_solver.solution_list)
        solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
        solomon_world.create_gif(my_gen_al_solver.solution_list)

    def test_first_solomon_gen_al_islands(self):
        for gen_count in [10, 100, 200, 1000]:
            solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_025.xml")
            my_gen_al_model = TspGenAlModel(None, solomon_world)
            solomon_world.show_solution_map(my_gen_al_model.solution_string)
            # print(my_gen_al_model.solution_string)
            my_gen_al_solver = GenAlMulti(my_gen_al_model, generations=gen_count, islands=5, population_size=30,
                                          verbose=True, fitness_invert=True)
            my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
            print(my_gen_al_solver.stacked_solution_list)
            solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
            solomon_world.create_stacked_gif(my_gen_al_solver.stacked_solution_list,
                                             extra_file_text=("gen" + str(gen_count)))

    def test_third_solomon_gen_al_islands(self):
        for gen_count in [10, 100, 200, 1000]:
            solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_100.xml")
            my_gen_al_model = TspGenAlModel(None, solomon_world)
            solomon_world.show_solution_map(my_gen_al_model.solution_string)
            # print(my_gen_al_model.solution_string)
            my_gen_al_solver = GenAlMulti(my_gen_al_model, generations=gen_count, islands=5, population_size=30,
                                          verbose=True, fitness_invert=True)
            my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
            print(my_gen_al_solver.stacked_solution_list)
            solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
            # solomon_world.create_stacked_gif(my_gen_al_solver.stacked_solution_list,
            #                                  extra_file_text=("gen" + str(gen_count)))

    def test_third_solomon_gen_al_islands_multi10(self):
        for gen_count in [10, 10, 10, 10, 10]:
            solomon_world = tsp_world(xml_path="solomon-1987-c2/C201_100.xml")
            my_gen_al_model = TspGenAlModel(None, solomon_world)
            solomon_world.show_solution_map(my_gen_al_model.solution_string)
            # print(my_gen_al_model.solution_string)
            my_gen_al_solver = GenAlMulti(my_gen_al_model, generations=gen_count, islands=5, population_size=30,
                                          verbose=True, fitness_invert=True)
            my_gen_al_solver.find_solution_with_timeout_and_bottleneck()
            print(my_gen_al_solver.stacked_solution_list)
            solomon_world.show_solution_map(my_gen_al_solver.solution_list[-1])
            solomon_world.create_stacked_gif(my_gen_al_solver.stacked_solution_list,
                                             extra_file_text=("gen" + str(gen_count)))
