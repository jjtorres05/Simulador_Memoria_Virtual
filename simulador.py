import sys
from fifo import FIFO
from lru import LRU
from tlb import TLB
from page_table import PageTable
from physical_memory import PhysicalMemory
from address_translator import AddressTranslator

TLB_SIZE = 16


def create_algorithm(name, size):
    if name == "FIFO":
        return FIFO(size)
    return LRU(size)


def main():
    if len(sys.argv) != 4:
        print("Uso: python simulador.py addresses.txt [QUADROS] [FIFO|LRU]")
        sys.exit(1)

    address_file = sys.argv[1]
    num_frames = int(sys.argv[2])
    algorithm_name = sys.argv[3].upper()

    if algorithm_name not in ("FIFO", "LRU"):
        print("Algoritmo debe ser FIFO o LRU")
        sys.exit(1)

    if num_frames <= 0 or (num_frames & (num_frames - 1)) != 0:
        print("QUADROS debe ser potencia de 2 (2, 4, 8, 16, 32, ...)")
        sys.exit(1)

    # Crear algoritmos independientes para TLB y memoria fisica
    tlb_algorithm = create_algorithm(algorithm_name, TLB_SIZE)
    mem_algorithm = create_algorithm(algorithm_name, num_frames)

    # Crear componentes
    tlb = TLB(TLB_SIZE, tlb_algorithm)
    page_table = PageTable()
    phys_mem = PhysicalMemory(num_frames, mem_algorithm)

    try:
        backing_store = open("BACKING_STORE.bin", "rb")
    except FileNotFoundError:
        print("Error: BACKING_STORE.bin no encontrado")
        sys.exit(1)

    translator = AddressTranslator(tlb, page_table, phys_mem, backing_store)

    # Procesar archivo de direcciones
    output_lines = []

    with open(address_file, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            if line == "PageTable":
                result = page_table.dump()
                output_lines.append(result)
                print(result)
                continue

            if line == "TLB":
                result = tlb.dump()
                output_lines.append(result)
                print(result)
                continue

            logical_address = int(line)
            physical_address, value = translator.translate(logical_address)

            result = f"Endereco Virtual: {logical_address} Endereco Fisico: {physical_address} Conteudo: {value}"
            output_lines.append(result)
            print(result)

    # Estadisticas
    pf_rate, tlb_rate = translator.get_stats()
    stats = f"\nTaxa de Page-Fault: {pf_rate:.2f}%\nTaxa de TLB Hit: {tlb_rate:.2f}%"
    output_lines.append(stats)
    print(stats)

    # Escribir correct.txt
    with open("correct.txt", "w") as f:
        f.write("\n".join(output_lines) + "\n")

    backing_store.close()


if __name__ == "__main__":
    main()
