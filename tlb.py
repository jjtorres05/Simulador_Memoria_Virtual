class TLB:
    def __init__(self, size, replacement_algorithm):
        self.size = size
        self.algorithm = replacement_algorithm
        self.pages = [-1] * size
        self.frames = [-1] * size
        self.valid = [False] * size

    def lookup(self, page):
        for i in range(self.size):
            if self.valid[i] and self.pages[i] == page:
                self.algorithm.access(i)
                return self.frames[i]
        return -1

    def update(self, page, frame):
        # Si ya esta, actualizar
        for i in range(self.size):
            if self.valid[i] and self.pages[i] == page:
                self.frames[i] = frame
                self.algorithm.access(i)
                return

        # Buscar entrada libre
        for i in range(self.size):
            if not self.valid[i]:
                self._set_entry(i, page, frame)
                return

        # Llena: reemplazar
        victim = self.algorithm.choose_victim(self.valid)
        self._set_entry(victim, page, frame)

    def invalidate_page(self, page):
        for i in range(self.size):
            if self.valid[i] and self.pages[i] == page:
                self.valid[i] = False

    def _set_entry(self, index, page, frame):
        self.pages[index] = page
        self.frames[index] = frame
        self.valid[index] = True
        self.algorithm.access(index)

    def dump(self):
        lines = ["**************"]
        for i in range(self.size):
            if self.valid[i]:
                lines.append(f"Pagina {self.pages[i]} - Quadro: {self.frames[i]} - Bit Validade: 1")
            else:
                lines.append(f"Pagina - - Quadro: - - Bit Validade: 0")
        lines.append("**************")
        return "\n".join(lines)
