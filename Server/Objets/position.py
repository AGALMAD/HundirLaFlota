class Position:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.touched = False

    def __eq__(self, __value):
        return self.x == __value.x and self.y == __value.y

