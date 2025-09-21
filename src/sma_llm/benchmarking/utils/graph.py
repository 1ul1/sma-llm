"""Draw Graphs.
https://stackoverflow.com/questions/70007610/how-do-i-make-a-graph-diagram-from-a-csv-file-in-python"""

import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore

def both_in_one():
    plt.figure()
    plt.grid(False)

    dataframe = pd.read_csv('memory_mlc.cvs')
    plt.plot(dataframe["time"] - 5, dataframe["used_ram"] - 6.8,color="blue", label="MLC-LLM")
    dataframe = pd.read_csv('memory_py.cvs')
    plt.plot(dataframe["time"], dataframe["used_ram"] + 1,color="red", label="PyTorch")

    # lines for better visualization
    plt.axvline(x=5.4, color='lightblue', linestyle='-', label="Upload MLC")
    plt.axvline(x=7.32, color='pink', linestyle='-', label="Upload PyTorch")
    plt.axvline(x=14.6, color='lightblue', linestyle='--', label="Generation MLC")
    plt.axvline(x=35.3, color='pink', linestyle='--', label="Generation PyTorch")


    plt.xlabel("Time - seconds")
    plt.ylabel("Used RAM - Gb")
    plt.title("Used Ram Comparison between engines on Apple metal")
    plt.legend()

    plt.show()


if __name__ == "__main__":
    match input("what engine: mlc or py?\n"):
        case "mlc":
            filename = 'memory_mlc.cvs'
        case "py":
            filename = 'memory_py.cvs'
        case _:
            both_in_one()
            exit(0)
        
    dataframe = pd.read_csv(filename)

    dataframe.plot(x="time", y="used_ram", kind="line", marker="o")
    plt.xlabel("Time (s)")
    plt.ylabel("Used RAM (GB)")
    plt.title("RAM usage over time")
    plt.show()