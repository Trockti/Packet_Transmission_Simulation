.PHONY: all install question1 question3 question4 question6

all: install question1 question3 question4 question6

# Install pip and Python dependencies
install:
	python3 -m pip install -r requirements.txt

# Specify the command to run the simulation
question1: Lab1.py
	python3 Lab1.py question1
question3: Lab1.py
	python3 Lab1.py question3
question4: Lab1.py
	python3 Lab1.py question4
question6: Lab1.py
	python3 Lab1.py question6