all: simulador

simulador:
	@echo "Simulador de Memoria Virtual"
	@echo "Uso: python3 simulador.py addresses.txt [QUADROS] [FIFO|LRU]"
	@echo ""
	@echo "Ejemplos:"
	@echo "  python3 simulador.py addresses.txt 256 FIFO"
	@echo "  python3 simulador.py addresses.txt 128 LRU"
	@echo "  python3 simulador.py addresses.txt 64 FIFO"

run-fifo:
	python3 simulador.py addresses.txt 256 FIFO

run-lru:
	python3 simulador.py addresses.txt 256 LRU

run-fifo-128:
	python3 simulador.py addresses.txt 128 FIFO

run-lru-128:
	python3 simulador.py addresses.txt 128 LRU

clean:
	rm -f correct.txt
