all: install run

install:
	pip install -r requirements.txt

run:
	python3 src/main_mso.py

clean:
	rm results/*