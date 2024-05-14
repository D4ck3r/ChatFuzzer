from pyradamsa import Radamsa

class MutationStrategy:
    def __init__(self) -> None:
        self.rad = Radamsa()

    
    def str_mutator(self, data):
        res = []
        res.append(data)
        res.append(data * 100)
        res.append(data * 200)
        return res

    def num_mutator(self, data):
        res = []
        res.append("1")
        res.append("65535")
        return res
    
    def radamsa_mutator(self, data, times):
        mutated_variants = [self.rad.fuzz(data) for _ in range(times)]
        return mutated_variants


    def mutator(self, data, dtype):
        res = None
        if dtype == "num":
            res = self.num_mutator(data)
        elif dtype == "str":
            res = self.str_mutator(data)
        else:
            pass

        return res