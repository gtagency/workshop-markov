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
    for token in current:
        yield token
    while True:
        try:
            new_token = random.choice(graph[current])
            current = tuple(list(current[1:]) + [new_token])
            yield new_token
        except IndexError:
            raise StopIteration

class Chain:
    def __init__(self, raw_data, ngrams = 1):
        tokens = tokenizer(raw_data)
        self.train(tokens, ngrams)

    def train(self, tokens, ngrams):
        chain = defaultdict(list)
        prev = [next(tokens) for _ in range(ngrams)]
        for word in tokens:
            chain[tuple(prev)].append(word)
            prev = prev[1:]
            prev.append(word)
        self.chain = chain

    def walk(self, n):
        # for token, _ in zip(walker(self.chain), range(n)):
            # print(token)
        return [token for token, _ in zip(walker(self.chain), range(n))]

def load_multiple(files):
    datasets = []
    for file_name in files:
        with open('datasets/' + file_name + '.txt', 'r') as f:
            datasets.append(f.read())
    return '\n'.join(datasets)

if __name__ == "__main__":
    raw_data = load_multiple(['aliens', 'agency', 'agency'])
    c = Chain(raw_data, 1)
    print(' '.join(c.walk(100)))
