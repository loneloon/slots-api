from models.symbol import Symbol


class Reel:
    def __init__(self, height):
        self.keys = [Symbol() for k in range(height)]

    def __repr__(self):
        return str(self.keys)