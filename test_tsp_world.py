from collections import namedtuple
from unittest import TestCase

from TspDefinition import tsp_world

Place_Node = namedtuple('Place_Node', 'id x y')


class TestTsp_world(TestCase):

    def generate_simple_tsp_world(self):
        place_node_coord = [["1", 1, 1], ["2", 2, 1], ["3", 3, 1], ["4", 3, 2], ["5", 2, 2], ["6", 1, 2]]
        place_node_list = []
        for single_place in place_node_coord:
            place_node_list.append(Place_Node(single_place[0], single_place[1], single_place[2]))
        return tsp_world(simple_node_list=place_node_list)

    def test_get_solution_length_larger_world(self):
        square_size = 5
        square_world = tsp_world().generate_square_tsp_world(square_size)
        # square_world.show_base_map()
        self.assertAlmostEqual(((square_size - 1) * 4), square_world.get_solution_length(square_world.get_node_list()))
        # other_solution = square_world.get_random_solution()
        # print(square_world.get_solution_length(other_solution))
        # square_world.show_solution_map(other_solution)

    def test_get_solution_length_basics(self):
        simple_world = self.generate_simple_tsp_world()
        simple_solution = simple_world.get_node_list()
        self.assertAlmostEqual(6, simple_world.get_solution_length(simple_solution))
        try:
            simple_world.get_solution_length(simple_solution[0:-2])
            self.fail("Allowed solution without all nodes")
        except:
            pass
        try:
            simple_solution.append("1")
            simple_world.get_solution_length(simple_solution)
            self.fail("Allowed solution with revisited node")
        except:
            pass
        for x in range(1000):
            simple_solution = simple_world.get_random_solution()
            self.assertLessEqual(6, simple_world.get_solution_length(simple_solution))

    def test_get_solution_length_caching(self):
        simple_world = self.generate_simple_tsp_world()
        simple_world.max_solution_cache = 4
        self.assertEqual(0, len(simple_world.tested_solutions_chrono))
        simple_solution = simple_world.get_node_list()
        simple_world.get_solution_length(simple_solution)
        self.assertEqual(1, len(simple_world.tested_solutions_chrono))
        simple_world.get_solution_length(simple_solution)
        self.assertEqual(1, len(simple_world.tested_solutions_chrono))
        for x in range(10):
            simple_solution = simple_solution[1:] + simple_solution[0:1]
            simple_world.get_solution_length(simple_solution)
            self.assertLessEqual(len(simple_world.tested_solutions_chrono), 4)
            self.assertLessEqual(len(simple_world.tested_solutions.keys()), 4)
            self.assertAlmostEqual(0,
                                   len(set(simple_world.tested_solutions) - set(simple_world.tested_solutions_chrono)))
            self.assertAlmostEqual(0,
                                   len(set(simple_world.tested_solutions_chrono) - set(simple_world.tested_solutions)))

    def test_show_base_map(self):

        # simple_world = self.generate_simple_tsp_world()
        # simple_world.show_base_map()
        pass

    def test_show_solution_map(self):
        # simple_world = self.generate_simple_tsp_world()
        # simple_solution = simple_world.get_node_list()
        # simple_world.show_solution_map(simple_solution)
        # simple_world.show_solution_map(simple_world.get_random_solution())
        # difficult_world = tsp_world(xml_path="solomon-1987-c2/C202_025.xml")
        # difficult_world.show_solution_map(difficult_world.get_random_solution())
        pass

    def test_find_simple_solution_with_gen_al(self):
        square_model = tsp_world().generate_square_tsp_world(4)
        pass
