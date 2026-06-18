PAGE_SIZE = 256


class PhysicalMemory:
    def __init__(self, num_frames, replacement_algorithm):
        self.num_frames = num_frames
        self.algorithm = replacement_algorithm
        self.memory = bytearray(num_frames * PAGE_SIZE)
        self.frame_to_page = [-1] * num_frames
        self.next_free = 0

    def has_free_frame(self):
        return self.next_free < self.num_frames

    def allocate_frame(self, page, page_data):
        if self.has_free_frame():
            frame = self.next_free
            self.next_free += 1
        else:
            frame = self.algorithm.choose_victim(
                [True] * self.num_frames
            )

        old_page = self.frame_to_page[frame]

        # Cargar datos en memoria
        start = frame * PAGE_SIZE
        for i in range(PAGE_SIZE):
            self.memory[start + i] = page_data[i]

        self.frame_to_page[frame] = page
        self.algorithm.access(frame)

        return frame, old_page

    def access_frame(self, frame):
        self.algorithm.access(frame)

    def read_byte(self, frame, offset):
        value = self.memory[frame * PAGE_SIZE + offset]
        # Convertir a signed byte (-128 a 127)
        if value > 127:
            value -= 256
        return value
