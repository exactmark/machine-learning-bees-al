import math
import random
from typing import List

import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.style.use('seaborn-whitegrid')
from collections import namedtuple

Place_Node = namedtuple('Place_Node', 'id x y')
MapExtent = namedtuple('MapExtent', 'max_x min_x max_y min_y')


class node(object):
    def __init__(self, node_id=None, x=None, y=None):
        self.node_id = node_id
        self.x = x
        self.y = y


class tsp_world(object):
    def __init__(self, simple_node_list=None, xml_path=None, max_solution_cache=4000):
        self.node_dict = {}
        self.map_extent = None
        self.tested_solutions = {}
        self.tested_solutions_chrono = []
        self.max_solution_cache = max_solution_cache
        if xml_path:
            from XmlReader import get_network_data
            place_node_list = get_network_data(xml_path)
            for single_node in place_node_list:
                self.node_dict[single_node.id] = node(single_node.id, single_node.x, single_node.y)
        elif simple_node_list:
            for single_node in simple_node_list:
                self.node_dict[single_node.id] = node(single_node.id, single_node.x, single_node.y)

    def get_node_list(self):
        return list(self.node_dict.keys())

    def get_random_solution(self):
        node_list = self.get_node_list()
        return random.sample(node_list, len(node_list))

    def get_map_extent(self):
        if self.map_extent:
            return self.map_extent
        max_x = max([single_node.x for single_node in self.node_dict.values()])
        min_x = min([single_node.x for single_node in self.node_dict.values()])
        max_y = max([single_node.y for single_node in self.node_dict.values()])
        min_y = min([single_node.y for single_node in self.node_dict.values()])
        self.map_extent = MapExtent(max_x, min_x, max_y, min_y)
        return self.map_extent

    def show_base_map(self):
        assert len(self.node_dict) > 0
        for single_node in self.node_dict.values():
            plt.plot(single_node.x, single_node.y, "bo", label=single_node.node_id)
        map_extent = self.get_map_extent()
        xmargin = (map_extent.max_x - map_extent.min_x) / float(10)
        ymargin = (map_extent.max_y - map_extent.min_y) / float(10)
        plt.xlim(map_extent.min_x - xmargin, map_extent.max_x + xmargin)
        plt.ylim(map_extent.min_y - ymargin, map_extent.max_y + ymargin)
        plt.show()

    def show_solution_map(self, simple_solution):
        for i in range(-1, len(simple_solution) - 1):
            node1 = self.node_dict[simple_solution[i]]
            node2 = self.node_dict[simple_solution[i + 1]]
            plt.plot([node1.x, node2.x], [node1.y, node2.y], 'bo-')
        map_extent = self.get_map_extent()
        xmargin = (map_extent.max_x - map_extent.min_x) / 10
        ymargin = (map_extent.max_y - map_extent.min_y) / 10
        plt.xlim(map_extent.min_x - xmargin, map_extent.max_x + xmargin)
        plt.ylim(map_extent.min_y - ymargin, map_extent.max_y + ymargin)
        # plt.text(0, 0.15, ",".join(simple_solution) + "\n"
        #          + "Solution length is %.2f" % (self.get_solution_length(simple_solution)))
        plt.text(0, 0.15, "Solution length is %.2f" % (self.get_solution_length(simple_solution)))
        plt.show()

    def get_node_distance(self, node1_id: str, node2_id: str) -> float:
        node1 = self.node_dict[node1_id]
        node2 = self.node_dict[node2_id]
        return math.sqrt((node1.x - node2.x) ** 2 + (node1.y - node2.y) ** 2)

    def get_solution_length(self, solution_string: List[str]) -> float:
        if len(solution_string) != len(self.node_dict.keys()):
            raise RuntimeError
        if len(set(solution_string) - set(self.node_dict.keys())) > 0:
            raise RuntimeError
        if len(set(self.node_dict.keys()) - set(solution_string)) > 0:
            raise RuntimeError
        flat_solution = ",".join(solution_string)
        if flat_solution in self.tested_solutions:
            return self.tested_solutions[flat_solution]
        solution_length = 0
        for x in range(-1, len(solution_string) - 1):
            solution_length += self.get_node_distance(solution_string[x], solution_string[x + 1])
        self.tested_solutions[flat_solution] = solution_length
        self.tested_solutions_chrono.append(flat_solution)
        if len(self.tested_solutions_chrono) > self.max_solution_cache:
            old_solution = self.tested_solutions_chrono[0]
            self.tested_solutions_chrono.remove(old_solution)
            self.tested_solutions.__delitem__(old_solution)
        return solution_length

    @staticmethod
    def generate_square_tsp_world(side_size):
        place_node_coord = []
        for x in range(side_size):
            place_node_coord.append([str(x + 1), x + 1, 1])
        for x in range(1, side_size):
            place_node_coord.append([str(x + side_size), side_size, x + 1])
        for x in range(1, side_size):
            place_node_coord.append([str(x + side_size + side_size - 1), side_size - x, side_size])
        for x in range(1, side_size - 1):
            place_node_coord.append([str(x + 3 * side_size - 2), 1, side_size - x])
        place_node_list = []
        for single_place in place_node_coord:
            place_node_list.append(Place_Node(single_place[0], single_place[1], single_place[2]))
        return tsp_world(simple_node_list=place_node_list)

    def create_gif(self, solution_list):
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)

        # Query the figure's on-screen size and DPI. Note that when saving the figure to
        # a file, we need to provide a DPI for that separately.
        print('fig size: {0} DPI, size in inches {1}'.format(
            fig.get_dpi(), fig.get_size_inches()))

        # Plot a scatter that persists (isn't redrawn) and the initial line.
        # x = np.arange(0, 20, 0.1)
        # ax.scatter(x, x + np.random.normal(0, 3.0, len(x)))
        # line, = ax.plot(x, x - 5, 'r-', linewidth=2)

        def update(simple_solution):
            frame_num = simple_solution[0]
            simple_solution = simple_solution[1]
            ax.clear()
            for i in range(-1, len(simple_solution) - 1):
                node1 = self.node_dict[simple_solution[i]]
                node2 = self.node_dict[simple_solution[i + 1]]
                ax.plot([node1.x, node2.x], [node1.y, node2.y], 'bo-')
            label = 'length %.4f, frame %i of %i' % (
                self.get_solution_length(simple_solution), frame_num, len(solution_list))
            print(label)
            # Update the line and the axes (with a new xlabel). Return a tuple of
            # "artists" that have to be redrawn for this frame.
            ax.set_xlabel(label)
            return None, ax

        numbered_solutions = [[x + 1, single_solution] for x, single_solution in enumerate(solution_list)]
        anim = FuncAnimation(fig, update, blit=False, frames=numbered_solutions, interval=500)
        anim.save(
            ('n' + str(len(self.get_node_list())) + '-len' + str(self.get_solution_length(solution_list[-1])) + '.gif'),
            dpi=80, writer='imagemagick')

    def create_stacked_gif(self, stacked_solution_list, extra_file_text=None):
        fig, ax = plt.subplots()
        fig.set_tight_layout(True)

        # Query the figure's on-screen size and DPI. Note that when saving the figure to
        # a file, we need to provide a DPI for that separately.
        print('fig size: {0} DPI, size in inches {1}'.format(
            fig.get_dpi(), fig.get_size_inches()))

        # Plot a scatter that persists (isn't redrawn) and the initial line.
        # x = np.arange(0, 20, 0.1)
        # ax.scatter(x, x + np.random.normal(0, 3.0, len(x)))
        # line, = ax.plot(x, x - 5, 'r-', linewidth=2)

        def update(stacked_solution):
            colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']
            frame_num = stacked_solution[0]
            stacked_solution = stacked_solution[1]
            ax.clear()
            best_solution_length = self.get_solution_length(stacked_solution[0])
            for color, simple_solution in enumerate(stacked_solution):
                if best_solution_length > self.get_solution_length(simple_solution):
                    best_solution_length = self.get_solution_length(simple_solution)
                for i in range(-1, len(simple_solution) - 1):
                    node1 = self.node_dict[simple_solution[i]]
                    node2 = self.node_dict[simple_solution[i + 1]]
                    ax.plot([node1.x, node2.x], [node1.y, node2.y], (colors[color] + 'o-'), alpha=0.7)
            label = 'length %.4f, frame %i of %i' % (
                best_solution_length, frame_num, len(stacked_solution_list))
            print(label)
            # Update the line and the axes (with a new xlabel). Return a tuple of
            # "artists" that have to be redrawn for this frame.
            ax.set_xlabel(label)
            return None, ax

        numbered_solutions = [[x + 1, single_solution] for x, single_solution in enumerate(stacked_solution_list)]
        anim = FuncAnimation(fig, update, blit=False, frames=numbered_solutions, interval=500)
        anim.save(
            ('n' + str(len(self.get_node_list())) + '-len' + str(
                min([self.get_solution_length(single_list) for single_list in stacked_solution_list[-1]])
            ) + str(extra_file_text) + '.gif'),
            dpi=80, writer='imagemagick')


class TspGenAlModel(object):
    def __init__(self, solution_string, world_state=None):
        self.world_state: tsp_world
        self.world_state = world_state
        if solution_string is None:
            self.solution_string = world_state.get_random_solution()
        else:
            self.solution_string = solution_string
        self.fitness = None

    def show_solution_map(self):
        self.world_state.show_solution_map(self.solution_string)

    def get_child(self, solution_string):
        returnedchild = self.__class__(solution_string, self.world_state)
        return returnedchild

    def get_fitness(self):
        self.fitness = 1.0 / self.world_state.get_solution_length(self.solution_string)
        return self.fitness

    def mutate(self, mutation_chance):
        mutated = False
        for x in range(0, len(self.solution_string)):
            if random.random() < mutation_chance:
                mutated = True
                swapper = random.randint(0, len(self.solution_string) - 1)
                self.solution_string[x], self.solution_string[swapper] = self.solution_string[swapper], \
                                                                         self.solution_string[x]
        if mutated:
            self.fitness = None

    def mutate_orig(self, mutation_chance):
        mutated = False
        for x in range(-1, len(self.solution_string) - 1):
            if random.random() < mutation_chance:
                mutated = True
                self.solution_string[x], self.solution_string[x + 1] = self.solution_string[x + 1], \
                                                                       self.solution_string[x]
        if mutated:
            self.fitness = None

    def __remove_duplicates(self, solution_string):
        return_string = []
        for this_point in solution_string:
            if this_point not in return_string:
                return_string.append(this_point)
        return return_string

    def get_crossover_strings(self, mate):
        child_string_list = []
        crossover_point = random.randint(1, len(self.solution_string) - 2)
        child_string_list.append(
            self.solution_string[crossover_point:] +
            mate.solution_string +
            self.solution_string[:crossover_point])
        child_string_list.append(
            mate.solution_string[crossover_point:] +
            self.solution_string +
            mate.solution_string[:crossover_point])
        child_string_list.append(
            self.solution_string[:crossover_point] +
            mate.solution_string +
            self.solution_string[crossover_point:])
        child_string_list.append(
            mate.solution_string[:crossover_point] +
            self.solution_string +
            mate.solution_string[crossover_point:])
        return_string_list = []
        for single_string in child_string_list:
            return_string_list.append(self.__remove_duplicates(single_string))
        return return_string_list

    def __lt__(self, other):
        return self.get_fitness() > other.get_fitness()


class TspBeeModel(object):
    # This is a bee!
    # Note that scouts don't need to be passed a string, they'll just find
    # a solution.
    # Note that a bee has to know its world state so it knows the fitness
    # of the solution it's on.
    def __init__(self, solution_string=None, world_state=None):
        self.world_state: tsp_world
        self.world_state = world_state
        if solution_string is None:
            self.solution_string = world_state.get_random_solution()
        else:
            self.solution_string = solution_string
        self.move_indices = list(range(len(self.solution_string)))
        self.fitness = None

    def show_solution_map(self):
        self.world_state.show_solution_map(self.solution_string)

    def get_fitness(self,solution_string=None):
        if solution_string:
            return 1.0 / self.world_state.get_solution_length(solution_string)
        if self.fitness:
            return self.fitness
        self.fitness = 1.0 / self.world_state.get_solution_length(self.solution_string)
        return self.fitness

    def move_bee(self, moves: int):
        # move_sequence = random.choices(list(range(len(self.solution_string))), k=moves * 2)
        move_sequence = random.choices(self.move_indices, k=moves * 2)
        for x in range(0, moves * 2, 2):
            swapper_left = move_sequence[x]
            swapper_right = move_sequence[x + 1]
            if swapper_left != swapper_right:
                self.solution_string[swapper_left], self.solution_string[swapper_right] = self.solution_string[
                                                                                              swapper_right], \
                                                                                          self.solution_string[
                                                                                              swapper_left]
        self.fitness = None

    def get_random_solution(self):
        return self.world_state.get_random_solution()

    def get_new_bee(self, solution_string=None):
        if solution_string:
            new_bee_solution = solution_string.copy()
        else:
            new_bee_solution = None
        return TspBeeModel(world_state=self.world_state, solution_string=new_bee_solution)

    def __lt__(self, other):
        return self.get_fitness() < other.get_fitness()
