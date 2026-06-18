class FIFO:
    def __init__(self, size):
        self.size = size
        self.pointer = 0

    def choose_victim(self, entries):
        victim = self.pointer
        self.pointer = (self.pointer + 1) % self.size
        return victim

    def access(self, index):
        pass
