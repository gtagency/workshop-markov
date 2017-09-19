from collections import defaultdict
import random

def tokenizer(raw_data):
    ends = set(' .?!\n')
    no_yield = set(' \n')
    current_token = []
    for char in raw_data:
        if char in ends and len(current_token) != 0:
            yield ''.join(current_token)
            if char not in no_yield:
                yield char
            current_token = []
        else:
            if char not in no_yield:
                current_token.append(char)

def walker(graph):
    current = tuple(random.choice(list(graph.keys())))
    yield current[0]
    while True:
        try:
            current = tuple([random.choice(graph[current])])
        except IndexError:
            raise StopIteration
        yield current[0]

class Chain:
    def __init__(self, raw_data):
        tokens = tokenizer(raw_data)
        self.train(tokens, 1)

    def train(self, tokens, ngrams):
        chain = defaultdict(list)
        prev = [next(tokens) for _ in range(ngrams)]
        for word in tokens:
            chain[tuple(prev)].append(word)
            prev = prev[1:]
            prev.append(word)
        self.chain = chain

    def walk(self, n):
        return [token for token, _ in zip(walker(self.chain), range(n))]

if __name__ == "__main__":
    with open('datasets/rickle_in_time.txt', 'r') as f:
        raw_data = f.read()

    c = Chain(raw_data)
    print(' '.join(c.walk(50)))



