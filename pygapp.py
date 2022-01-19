import sys
import logging
import string
from numpy import random as npr
import pygad

POPSIZE = 5000
TARGET = "methinks it is like a weasel"
TARGET_LEN = len(TARGET)
STRING_DOMAIN = list(string.ascii_lowercase + string.punctuation + " ")
STRING_DOMAIN_LEN = len(STRING_DOMAIN)

desired_output = 1
target_ords = [ord(c) for c in TARGET]

def fitness_calc(solution, solution_idx):
    #fitness is percent of list values that are correct (right value, right place)
    retval = len([i for i in range(TARGET_LEN) if solution[i] == target_ords[i]])/TARGET_LEN
    return retval

def func_generation(instance):
    print(f"gen {instance.generations_completed} winner: {''.join([chr(c) for c in instance.best_solution()[0]])} : {instance.best_solution()[1]}")

def main(population_size = POPSIZE, generations = 300):
    logging.getLogger().setLevel(logging.DEBUG)
    ga_instance = pygad.GA(num_generations = generations,
                           sol_per_pop = population_size,
                           num_genes = TARGET_LEN,
                           num_parents_mating = 2,
                           fitness_func = fitness_calc,
                           gene_type=int,
                           gene_space=[ord(c) for c in STRING_DOMAIN],
                           stop_criteria=["reach_1"],
                           crossover_probability=1,
                           on_generation=func_generation)
    ga_instance.run()
    sol = ga_instance.best_solution()
    sol_str = [chr(c) for c in sol[0]]
    print(''.join(sol_str))
    ga_instance.plot_fitness()

if __name__ == '__main__':
    main(*[int(x) for x in sys.argv[1:]])
