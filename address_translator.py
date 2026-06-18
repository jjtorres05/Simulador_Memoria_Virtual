PAGE_SIZE = 256


class AddressTranslator:
    def __init__(self, tlb, page_table, physical_memory, backing_store):
        self.tlb = tlb
        self.page_table = page_table
        self.physical_memory = physical_memory
        self.backing_store = backing_store
        self.total_accesses = 0
        self.tlb_hits = 0
        self.page_faults = 0

    def translate(self, logical_address):
        logical_address = logical_address & 0xFFFF
        page = (logical_address >> 8) & 0xFF
        offset = logical_address & 0xFF

        self.total_accesses += 1

        # 1. Buscar en TLB
        frame = self.tlb.lookup(page)
        if frame >= 0:
            self.tlb_hits += 1
            self.physical_memory.access_frame(frame)
        else:
            # 2. Buscar en Page Table
            frame = self.page_table.lookup(page)
            if frame >= 0:
                self.physical_memory.access_frame(frame)
                self.tlb.update(page, frame)
            else:
                # 3. Page Fault
                frame = self._handle_page_fault(page)
                self.tlb.update(page, frame)

        physical_address = frame * PAGE_SIZE + offset
        value = self.physical_memory.read_byte(frame, offset)

        return physical_address, value

    def _handle_page_fault(self, page):
        self.page_faults += 1

        # Leer pagina del BACKING_STORE
        self.backing_store.seek(page * PAGE_SIZE)
        page_data = self.backing_store.read(PAGE_SIZE)

        frame, old_page = self.physical_memory.allocate_frame(page, page_data)

        # Invalidar pagina anterior si habia una
        if old_page >= 0:
            self.page_table.invalidate(old_page)
            self.tlb.invalidate_page(old_page)

        self.page_table.set_entry(page, frame)

        return frame

    def get_stats(self):
        if self.total_accesses == 0:
            return 0.0, 0.0
        pf_rate = (self.page_faults / self.total_accesses) * 100
        tlb_rate = (self.tlb_hits / self.total_accesses) * 100
        return pf_rate, tlb_rate
