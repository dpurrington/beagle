import sys
import logging
from beagle import Beagle
import string
import random

POPSIZE = 5000
TARGET = "methinks it is like a weasel"
TARGET_LEN = len(TARGET)
STRING_DOMAIN = string.ascii_lowercase + string.punctuation + " "
STRING_DOMAIN_LEN = len(STRING_DOMAIN)

def get_random_string(size):
    return ''.join(random.SystemRandom().choice(STRING_DOMAIN) for _ in range(size))

def fitness_calc(s):
    # fitness is the percentage of chars in the right position
    return len([i for idx, i in enumerate(s) if s[idx] == TARGET[idx]])/TARGET_LEN

def main(population_size = POPSIZE, generations = 300):
    logging.getLogger().setLevel(logging.INFO)
    b = Beagle( fitness_calc )
    result = b.do_rounds([get_random_string(TARGET_LEN) for _ in range(population_size)], generations)
    logging.getLogger().info(result)

if __name__ == '__main__':
    main(*[int(x) for x in sys.argv[1:]])
