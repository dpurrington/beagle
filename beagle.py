from numpy import random as npr
import logging
import itertools

MUTATION_PROBABILITY=0.001

class Beagle:
    def __init__(self, fitness_function):
        self.fitness_function = fitness_function

    def score_round(self, data):
        # compute scores based on fitness function
        total = 0
        for d in data:
            d["score"] = self.fitness_function(d["population"])
            total = total + d["score"]

        # weigh them
        for d in data:
            d["weighted"] = d["score"]/total
        
        return data

    def select_winners(self, data, num):
        probs = [d["weighted"] for d in data]
        choices = npr.choice(len(data), num, p = probs)
        return [data[i] for i in choices]

    def reproduce(self, data):
        # pair (randomly -- just taking the pairs as they are because they were created randomly
        pairs = list(zip(data[::2], data[1::2]))

        # crossover the random pairs, don't reuse the same dictionaries
        new_data = self.crossover(pairs)
        # mutate
        new_data = self.mutate(new_data)
        return new_data

    def crossover(self, pairs):
        # crossover the pairs 
        pop_len = len(pairs[0][0]['population'])

        new_data = []
        for p in pairs:
            #new crossover point every pair
            crossover_point = npr.randint(0, pop_len)
            #don't reuse the same dictionaries, make new ones
            #do the crossover
            x_pop = p[0]['population'][:crossover_point] + p[1]['population'][crossover_point:] 
            y_pop = p[1]['population'][:crossover_point] + p[0]['population'][crossover_point:]
            x = { 'population': x_pop }
            y = { 'population': y_pop }
            new_data.append(x)
            new_data.append(y)
        return new_data

    def mutate(self, data):
        # mutation probability is 0.1 %
        for d in data:
            for p in d['population']:
                # this is O(n^^2), which sucks
                if npr.random_sample() <= MUTATION_PROBABILITY: 
                    #mutate 
                    p = npr.randint(0, 101)
        return data 

    def get_high_score(self, data):
        return max(data, key=lambda x:x['score'])

    def do_rounds(self, input, generations = 1):
        data = [{ 'population': d} for d in input]

        for i in range(0, generations + 1):
            if i > 0:
                winners = self.select_winners(data, len(data))
                data = self.reproduce(winners)
                logging.debug(f"new data: {[d['population'] for d in data]}")
            data = self.score_round(data)
            high_score = self.get_high_score(data)
            logging.info(f"best: {i}: {high_score['population']} {high_score['score']}") 

            if high_score['score'] == 1.0: 
                logging.info("ideal value found")
                return True, i, high_score 
        
        return False, i, high_score 