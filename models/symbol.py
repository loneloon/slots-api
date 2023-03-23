import random


class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


class Symbol:
    # __collection = ['🍇', '🍍', '🍑', '🥝', '🍉']
    __collection = ['1', '2', '3', '4', '5']
    __value_map = {k: v+1 for v, k in enumerate(__collection)}

    def __init__(self):
        self.key = random.choice(self.__collection)
        self.value = self.__value_map[self.key]
        self.isMatched = False

    def __repr__(self):
        if self.isMatched:
            return bcolors.OKGREEN + self.key + bcolors.ENDC
        else:
            return self.key