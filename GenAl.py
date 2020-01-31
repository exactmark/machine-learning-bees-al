# Course: CS7267
# Student name: Mark Fowler
# Student ID: mfowle19
# Assignment #: #4
# Due Date: November 6, 2019
# Signature:
# Score:

import bisect
import copy
import random


class GenAlModel(object):
    def __init__(self, solution_string):
        self.solution_string = solution_string
        self.fitness = None

    def get_child(self, solution_string):
        return self.__class__(solution_string)
        # GenAlModel(solution_string)

    def get_fitness(self):
        return 0

    def mutate(self, mutation_chance):
        mutated = False
        for x in range(len(self.solution_string)):
            if random.random() < mutation_chance:
                mutated = True
                self.solution_string[x] = (self.solution_string[x] + 1) % 2
        if mutated:
            self.fitness = None

    def get_crossover_strings(self, mate):
        child_string_list = []
        crossover_point = random.randint(1, len(self.solution_string))
        child_string_list.append(
            self.solution_string[crossover_point:] + mate.solution_string[:crossover_point])
        child_string_list.append(
            self.solution_string[:crossover_point] + mate.solution_string[crossover_point:])
        return child_string_list

    def __lt__(self, other):
        return self.get_fitness() > other.get_fitness()


# a simple model to evaluate x^2
class ExampleSquaredModel(GenAlModel):
    def __init__(self, solution_string=None):
        if solution_string == None:
            solution_string = self.get_random_solution(50)
        super().__init__(solution_string)
        self.fitness = None

    def get_random_solution(self, string_size):
        solution_string = []
        for x in range(string_size):
            solution_string.append(random.randint(0, 1))
        return solution_string

    def get_fitness(self) -> int:
        if self.fitness:
            return self.fitness
        else:
            return_sum = 0
            for x in range(len(self.solution_string)):
                if self.solution_string[-1 * x - 1] == 0:
                    pass
                else:
                    return_sum += 2 ** (x)
            self.fitness = return_sum
            return return_sum


class KnapsackModel(GenAlModel):
    def __init__(self, solution_string=None):
        self.fitness = None
        self.benefit_list = [5, 8, 3, 2, 7, 9, 4]
        self.weight_list = [7, 8, 4, 10, 4, 6, 4]
        self.max_weight = 22
        if solution_string == None:
            solution_string = self.get_random_solution(len(self.benefit_list))
        super().__init__(solution_string)
        self.weight = None

    def get_random_solution(self, string_size):
        solution_string = []
        for x in range(string_size):
            # solution_string.append(random.randint(0, 1))
            solution_string.append(0)
        return solution_string

    def get_fitness(self) -> int:
        if self.fitness:
            return self.fitness
        else:
            this_benefit = 0
            this_weight = 0
            for x in range(len(self.solution_string)):
                if self.solution_string[x] == 1:
                    this_benefit += self.benefit_list[x]
                    this_weight += self.weight_list[x]
            if this_weight > self.max_weight:
                this_benefit = 0
            self.weight = this_weight
            self.fitness = this_benefit
            return this_benefit


class KnapsackModelExtended(GenAlModel):
    def __init__(self, solution_string=None):
        self.fitness = None
        self.benefit_list = [5, 8, 3, 2, 7, 9, 4]
        self.weight_list = [7, 8, 4, 10, 4, 6, 4]
        for x in range(6):
            self.benefit_list = self.benefit_list + self.benefit_list
            self.weight_list = self.weight_list + self.weight_list
        self.max_weight = 256  # Best val 448
        self.max_weight = 268  # best val 466
        self.max_weight = 22
        if solution_string == None:
            solution_string = self.get_random_solution(len(self.benefit_list))
        super().__init__(solution_string)
        self.weight = None

    def get_random_solution(self, string_size):
        solution_string = []
        for x in range(string_size):
            # solution_string.append(random.randint(0, 1))
            solution_string.append(0)
        return solution_string

    def get_fitness(self) -> int:
        if self.fitness:
            return self.fitness
        else:
            this_benefit = 0
            this_weight = 0
            for x in range(len(self.solution_string)):
                if self.solution_string[x] == 1:
                    this_benefit += self.benefit_list[x]
                    this_weight += self.weight_list[x]
            if this_weight > self.max_weight:
                this_benefit = 0
            self.weight = this_weight
            self.fitness = this_benefit
            return this_benefit


class KnapsackModelWithNItems(GenAlModel):
    def __init__(self, solution_string=None):
        self.fitness = None
        self.benefit_list = [5, 8, 3, 2, 7, 9, 4]
        self.weight_list = [7, 8, 4, 10, 4, 6, 4]
        self.max_weight = 22
        if solution_string == None:
            solution_string = self.get_random_solution(len(self.benefit_list))
        super().__init__(solution_string)
        self.weight = None

    def get_random_solution(self, string_size):
        solution_string = []
        for x in range(string_size):
            solution_string.append(0)
        return solution_string

    def get_fitness(self) -> int:
        if self.fitness:
            return self.fitness
        else:
            this_benefit = 0
            this_weight = 0
            for x in range(len(self.solution_string)):
                this_benefit += self.benefit_list[x] * self.solution_string[x]
                this_weight += self.weight_list[x] * self.solution_string[x]
            if this_weight > self.max_weight:
                this_benefit = 0
            self.weight = this_weight
            self.fitness = this_benefit
            return this_benefit

    def mutate(self, mutation_chance):
        mutated = False
        for x in range(len(self.solution_string)):
            if random.random() < mutation_chance:
                mutated = True
                if self.solution_string[x] == 0:
                    self.solution_string[x] = 1
                elif random.random() < 0.1:
                    self.solution_string[x] = self.solution_string[x] - 1
                else:
                    self.solution_string[x] = self.solution_string[x] + 1
        if mutated:
            self.fitness = None


class Organism(object):
    def __init__(self, model: GenAlModel, generation):
        self.model = model
        self.generation = generation

    def get_fitness(self):
        return self.model.get_fitness()

    def get_children(self, mate):
        child_string_list = self.model.get_crossover_strings(mate.model)
        child_list = []
        for x in child_string_list:
            child_list.append(Organism(self.model.get_child(x), self.generation + 1))
        return child_list

    def __lt__(self, other):
        return self.get_fitness() > other.get_fitness()


class Population(object):
    def __init__(self, base_solution, population_size=10,
                 crossover_chance=0.1, mutation_chance=0.0001, apex_maintenance=3):
        self.base_solution = base_solution
        self.carrying_capacity = population_size
        self.current_generation = 0
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.apex_maintenance = apex_maintenance
        self.org_list = []
        self.__create_population()

    def __create_population(self):
        self.org_list = []
        self.__set_population_to_carrying_capacity()

    def __set_population_to_carrying_capacity(self):
        if len(self.org_list) < self.carrying_capacity:
            for x in range(self.carrying_capacity - len(self.org_list)):
                self.org_list.append(Organism(self.base_solution, self.current_generation))
            self.org_list.sort()
        elif len(self.org_list) > self.carrying_capacity:
            self.org_list = self.org_list[:self.carrying_capacity]
        assert len(self.org_list) == self.carrying_capacity

    def process_generation(self):
        self.__set_population_to_carrying_capacity()
        child_list = self.__get_children_by_fitness_tournament()
        self.org_list = self.org_list[:self.apex_maintenance] + child_list
        self.org_list.sort()
        self.current_generation += 1

    def __get_children_by_fitness_tournament(self):
        child_list = []
        total_fitness = sum([x.get_fitness() for x in self.org_list])
        if total_fitness == 0:
            for x in range((self.carrying_capacity - self.apex_maintenance)):
                child_list.append(Organism(self.base_solution, self.current_generation))
        else:
            fitness_list = [x.get_fitness() / total_fitness for x in self.org_list if x.get_fitness() > 0]
            if len(fitness_list) < 2:
                for x in range((self.carrying_capacity - self.apex_maintenance)):
                    child_list.append(Organism(self.base_solution(), self.current_generation))
                child_list += self.org_list
            else:
                mating_list = []
                while len(mating_list) < (self.carrying_capacity - self.apex_maintenance):
                    for left_ptr in range(len(fitness_list)):
                        for right_ptr in range(left_ptr + 1, len(fitness_list)):
                            if random.random() < fitness_list[left_ptr] and random.random() < fitness_list[right_ptr]:
                                mating_list.append([left_ptr, right_ptr])
                for single_pair in mating_list:
                    child_list = child_list + self.org_list[single_pair[0]].get_children(self.org_list[single_pair[1]])
        for single_child in child_list:
            single_child.model.mutate(self.mutation_chance)
        return child_list


class GenAl(object):
    def __init__(self, question_model, population_size=10, generations=1000,
                 crossover_chance=0.1, mutation_chance=0.0001, apex_maintenance=3):
        self.model = question_model
        self.carrying_capacity = population_size
        self.current_generation = 0
        self.generation_max = generations
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.apex_maintenance = apex_maintenance
        self.population = Population(question_model, population_size, crossover_chance, mutation_chance,
                                     apex_maintenance)

    def find_solution(self):
        while self.population.current_generation < self.generation_max:
            self.population.process_generation()
        print(self.population.org_list[0].generation)
        return self.population.org_list[0].model


class GenAlMulti(object):
    def __init__(self, question_model, population_size=10, generations=1000,
                 crossover_chance=0.1, mutation_chance=0.0001, apex_maintenance=3, islands=5, verbose=False,
                 fitness_invert=False):
        self.model = question_model
        self.carrying_capacity = population_size
        self.current_generation = 0
        self.time_point = 0
        self.generation_max = generations
        self.crossover_chance = crossover_chance
        self.mutation_chance = mutation_chance
        self.apex_maintenance = apex_maintenance
        self.solution_list = []
        self.stacked_solution_list = []
        self.islands = []
        self.verbose = verbose
        self.fitness_invert = fitness_invert
        for x in range(islands):
            self.islands.append(Population(question_model, population_size, crossover_chance, mutation_chance,
                                           apex_maintenance))

    def find_solution(self):
        while self.time_point < self.generation_max:
            best_model = sorted([single_pop.org_list[0].model for single_pop in self.islands])[0]
            for single_pop in self.islands:
                bisect.insort_left(single_pop.org_list, Organism(best_model, self.time_point))
                single_pop.process_generation()
            self.time_point += 1

        # for single_pop in self.islands:
        #     for org in single_pop.org_list:
        #         print(org.model.weight, org.model.get_fitness())
        #     print(single_pop.org_list[0].generation)
        print([single_pop.org_list[0].model.get_fitness() for single_pop in self.islands])
        best_model = sorted([single_pop.org_list[0].model for single_pop in self.islands])[0]
        return best_model

    def find_solution_with_timeout(self):
        stalled = 0
        best_fitness = 0
        while stalled < self.generation_max:
            best_model = sorted([single_pop.org_list[0].model for single_pop in self.islands])[0]
            if best_model.get_fitness() <= best_fitness:
                stalled += 1
            else:
                best_fitness = best_model.get_fitness()
                print("new fitness %.4f after %i steps" % (best_model.get_fitness(), stalled))
                stalled = 0
            for single_pop in self.islands:
                single_pop.process_generation()
            self.time_point += 1

        print([single_pop.org_list[0].model.get_fitness() for single_pop in self.islands])
        print(self.time_point)
        best_model = sorted([single_pop.org_list[0].model for single_pop in self.islands])[0]
        return best_model

    def find_solution_with_timeout_and_bottleneck(self):
        stalled = 0
        best_fitness = 0
        bottle_neck = False
        while stalled < self.generation_max:
            best_model = sorted([single_pop.org_list[0].model for single_pop in self.islands])[0]
            if best_model.get_fitness() <= best_fitness:
                stalled += 1
                if stalled == self.generation_max and not bottle_neck:
                    bottle_neck = True
                    stalled = 0
                    apex = [single_pop.org_list[0].model for single_pop in self.islands]
                    if self.verbose:
                        print("Bottleneck! Populations after apex additions:")
                    for single_pop in self.islands:
                        for apex_entry in apex:
                            single_pop.org_list.append(Organism(copy.deepcopy(apex_entry), self.time_point))
                        single_pop.org_list.sort()
                        if self.verbose:
                            print([this_model.get_fitness() for this_model in single_pop.org_list])
            else:
                best_fitness = best_model.get_fitness()
                if self.verbose:
                    if self.fitness_invert:
                        best_out_fitness = 1 / best_model.get_fitness()
                    else:
                        best_out_fitness = best_model.get_fitness()
                    print("new fitness %.4f after %i steps" % (best_out_fitness, stalled))
                self.solution_list.append(best_model.solution_string)
                self.stacked_solution_list.append([single_model.solution_string for single_model in sorted(
                    [single_pop.org_list[0].model for single_pop in self.islands])])
                stalled = 0
                bottle_neck = False

            for single_pop in self.islands:
                single_pop.process_generation()
            self.time_point += 1

        print("apex per island at finish:")
        print([single_pop.org_list[0].model.get_fitness() for single_pop in self.islands])
        print("after %i generations" % self.time_point)
        best_org = sorted([single_pop.org_list[0] for single_pop in self.islands])[0]
        print("best fitness %i was generated with generation stamp %i" % (best_org.get_fitness(), best_org.generation))
        best_model = best_org.model

        return best_model
