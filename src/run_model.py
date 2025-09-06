import read_input
from memory import Memory

def run_model():
    # read input -> generate -> show output -> update memory
    memory = Memory()
    while True:

        question = read_input.read_keyboard()