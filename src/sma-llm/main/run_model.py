import read_input
from memory import Memory

def run_model():
    # read input -> generate -> show output -> update memory

    ### handle User: here when reading input, also handle new line after only, not before!
    memory = Memory()
    while True:

        question = read_input.read_keyboard()