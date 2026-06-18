class LRU:
    def __init__(self, size):
        self.size = size
        self.last_used = [0] * size
        self.counter = 0

    def choose_victim(self, entries):
        victim = 0
        min_time = self.last_used[0]
        for i in range(1, self.size):
            if self.last_used[i] < min_time:
                min_time = self.last_used[i]
                victim = i
        return victim

    def access(self, index):
        self.counter += 1
        self.last_used[index] = self.counter
