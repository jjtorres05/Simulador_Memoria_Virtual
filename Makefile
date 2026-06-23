all: simulador

simulador:
	chmod +x simulador.py
	ln -sf simulador.py simulador

clean:
	rm -f simulador correct.txt
