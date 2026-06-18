PAGE_TABLE_SIZE = 256


class PageTable:
    def __init__(self):
        self.frames = [-1] * PAGE_TABLE_SIZE
        self.valid = [False] * PAGE_TABLE_SIZE

    def lookup(self, page):
        if self.valid[page]:
            return self.frames[page]
        return -1

    def set_entry(self, page, frame):
        self.frames[page] = frame
        self.valid[page] = True

    def invalidate(self, page):
        self.valid[page] = False

    def dump(self):
        lines = ["############"]
        for i in range(PAGE_TABLE_SIZE):
            if self.valid[i]:
                lines.append(f"Pagina {i} - Quadro: {self.frames[i]} - Bit Validade: 1")
            else:
                lines.append(f"Pagina {i} - Quadro: - - Bit Validade: 0")
        lines.append("############")
        return "\n".join(lines)
