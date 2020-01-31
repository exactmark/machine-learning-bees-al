from typing import List
from statistics import mean

class Bee_Solution_Model(object):
    # This is a sample bee! Make your own bee like in TspDefinition,
    # and make sure it has the following functions...
    def __init__(self):
        self.fitness = 0

    def get_random_solution(self):
        pass

    def get_fitness(self):
        return self.fitness

    def move_bee(self, moves: int, mutation_chance=0.01):
        pass

    def __lt__(self, other):
        return self.get_fitness() > other.get_fitness()

    def get_new_bee(self):
        return Bee_Solution_Model()


class FlowerPatch(object):
    def __init__(self, starting_bee, patch_center=None, num_bees=50, init_search_radius=50, verbose=False):
        self.verbose = verbose
        self.center_bee = starting_bee
        if patch_center:
            self.patch_center = patch_center
        else:
            self.patch_center = self.center_bee.get_random_solution()
        self.search_radius = init_search_radius
        self.num_bees = num_bees
        self.bees: List[Bee_Solution_Model]
        self.bees = [starting_bee.get_new_bee(solution_string=starting_bee.solution_string)]
        self.last_best = self.center_bee.get_fitness()

    def get_best_fitness(self):
        return self.center_bee.get_fitness()

    def add_bees(self, number_of_bees: int):
        for x in range(number_of_bees):
            self.bees.append(self.center_bee.get_new_bee())

    def set_bees_to_capacity(self):
        if len(self.bees) > self.num_bees:
            self.bees = self.bees[:self.num_bees]
        elif len(self.bees) < self.num_bees:
            self.add_bees(self.num_bees - len(self.bees))

    def process_time_step(self):
        for single_bee in self.bees:
            single_bee: Bee_Solution_Model
            single_bee.solution_string = self.patch_center.copy()
            single_bee.move_bee(self.search_radius)
        best_bee = max(self.bees)
        if best_bee.get_fitness() > self.center_bee.get_fitness():
            if self.verbose:
                print("Moving flower patch. Old fitness %.4f, new fitness %.4f" % (
                    self.center_bee.get_fitness(), best_bee.get_fitness()))
            self.center_bee = best_bee
            self.bees.remove(best_bee)
        else:
            if self.verbose:
                print("Reducing flower patch, old size %i, new size %i" % (
                    self.search_radius, self.search_radius // 5 * 4))
            self.search_radius = self.search_radius // 5 * 4

    def __lt__(self, other):
        return self.get_best_fitness() > other.get_best_fitness()


def default_stop(num_cycles):
    return num_cycles < 10000


class BeeAl(object):
    def __init__(self, solution_model, num_scouts=40, number_elite_sites=5, number_best_sites=10, bees_per_elite=40,
                 bees_per_remaining_best=20, neighborhood_size=5000, stag_limit=200, stop_criteria=default_stop,
                 verbose=False, fitness_invert=False, solution_list_limit=10):
        self.solution_model = solution_model
        self.num_scouts = num_scouts
        self.number_elite_sites = number_elite_sites
        self.number_best_sites = number_best_sites
        self.bees_per_elite = bees_per_elite
        self.bees_per_remaining_best = bees_per_remaining_best
        self.neighborhood_size = neighborhood_size
        self.stag_limit = stag_limit
        self.stop_criteria = stop_criteria
        self.verbose = verbose
        self.fitness_invert = fitness_invert
        self.flower_patches: List[FlowerPatch]
        self.flower_patches = []
        self.solution_list = []
        self.solution_list_limit = solution_list_limit
        self.dead_patches = 0
        self.best_patch_fitness = 0

    def find_solution(self):
        self.scout_new_patches()
        self.solution_list.append([0,self.flower_patches[0].center_bee.solution_string])
        while self.dead_patches<self.stag_limit:
            # print(current_iteration)
            self.handle_bee_patch_interaction()
            for single_patch in self.flower_patches:
                self.process_patch(single_patch)
            if self.verbose:
                print("Number of active patches: %i" % len(self.flower_patches))
        while len(self.flower_patches) > 0:
            for single_patch in self.flower_patches:
                self.process_patch(single_patch)
        self.solution_list.sort(reverse=True)
        self.trim_solution_list()

    def process_patch(self, single_patch: FlowerPatch):
        single_patch.process_time_step()
        if single_patch.search_radius <= 0:
            if self.verbose:
                print("Patch stagnation, storing solution for fitness %.4f" % single_patch.get_best_fitness())
            self.flower_patches.remove(single_patch)
            if single_patch.get_best_fitness() > self.best_patch_fitness:
                self.dead_patches = 0
                self.best_patch_fitness = single_patch.get_best_fitness()
                if self.verbose or True:
                    if self.fitness_invert:
                        print_fit = 1.0/self.best_patch_fitness
                    else:
                        print_fit=self.best_patch_fitness
                    print("found better patch %.4f"%print_fit)
            else:
                self.dead_patches+=1
                if self.verbose:
                    if len(self.flower_patches)>0:
                        print("stalling- %i, average patch size %.4f"%(self.dead_patches, mean([single_patch.search_radius for single_patch in self.flower_patches])))
            self.solution_list.append([single_patch.get_best_fitness(), single_patch.center_bee.solution_string])
            self.trim_solution_list()

    def trim_solution_list(self):
        if len(self.solution_list) > (self.solution_list_limit * 2):
            self.solution_list.sort(reverse=True)
            if self.verbose:
                print(self.solution_list[0], self.solution_list[-1])
            self.solution_list = self.solution_list[:self.solution_list_limit]

    def handle_bee_patch_interaction(self):
        self.scout_new_patches()
        self.flower_patches.sort()
        self.remove_bad_patches()
        self.send_bees_to_patches()

    def scout_new_patches(self):
        for x in range(self.num_scouts - len(self.flower_patches)):
            self.flower_patches.append(
                FlowerPatch(starting_bee=self.solution_model.get_new_bee(), init_search_radius=self.neighborhood_size,
                            verbose=self.verbose))

    def remove_bad_patches(self):
        self.flower_patches = self.flower_patches[:self.number_best_sites]

    def send_bees_to_patches(self):
        for single_patch in self.flower_patches[0:self.number_elite_sites]:
            single_patch.num_bees = self.bees_per_elite
            single_patch.set_bees_to_capacity()
        for single_patch in self.flower_patches[self.number_elite_sites:]:
            single_patch.num_bees = self.bees_per_remaining_best
            single_patch.set_bees_to_capacity()
        if self.verbose:
            print([(single_patch.get_best_fitness(), single_patch.num_bees) for single_patch in self.flower_patches])
