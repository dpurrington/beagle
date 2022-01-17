import logging
from beagle import Beagle
import string
from numpy import random as npr
import bitarray.util as bau
import bitarray

POPSIZE = 5000
TARGET = "whatchu talking bout willis?"
TARGET_LEN = len(TARGET)
STRING_DOMAIN = string.ascii_lowercase + string.punctuation + " "
STRING_DOMAIN_LEN = len(STRING_DOMAIN)

def get_random_string(size):
    retval = ""
    for c in range(size):
        retval += STRING_DOMAIN[npr.randint(0, STRING_DOMAIN_LEN)]
    return retval

def fitness_calc(s):
    #fitness is the inverse of 1 + sum of distance of each char from the target
    #target ideal value is 1 (identity)
    #return 1/(1 + sum([abs( ord(s[i]) - ord(TARGET[i])) for i in range(TARGET_LEN)] ))
    return sum([1 for i in range(TARGET_LEN) if s[i] == TARGET[i]])/TARGET_LEN

def main(population_size = POPSIZE, generations = 300):
    logging.getLogger().setLevel(logging.INFO)
    b = Beagle( fitness_calc )
    result = b.do_rounds([get_random_string(TARGET_LEN) for _ in range(population_size)], generations)
    logging.getLogger().info(result)

if __name__ == '__main__':
    main()