from sma_llm.utils import *


def run_model():
    # NOTE: handle User: here when reading input, also handle new line after only, not before!

    memory = Memory("mlc-llm") # "mlc-llm" or "hf-torch"


    # LOOP:<-><-><-><-><-><-><->
    # 1) decide engine and upload
    # 2) read input
    # 3) update memory
    # 4) generate output + Print live
    # 5) update memory
    # STOP: check memory for max_embedding, eos, nr. senteces
    # NOTE: the strings are processed directly when read || generated
    while True:
        pass