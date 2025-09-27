"""Draw Graphs.
https://stackoverflow.com/questions/70007610/how-do-i-make-a-graph-diagram-from-a-csv-file-in-python"""

import pandas as pd #type: ignore
import matplotlib.pyplot as plt #type: ignore

def both_in_one():
    """Representation for:
    Engine Type: pytorch-hf
        Model Upload Time: 7.326171791000888
        Time to First Token: 0.2508186670002033
        Throughput: 13.027325669074818
        total_generation_time: 27.759474292000024
    Engine Type: mlc-llm
        Model Upload Time: 6.997572916999957
        Time to First Token: 0.2184226670001408
        Throughput: 34.3108765101116
        total_generation_time: 5.712474292000024"""
    plt.figure()
    plt.grid(False)

    dataframe = pd.read_csv('memory_mlc.cvs')
    plt.plot(dataframe["time"] + 1.1, dataframe["used_ram"] - 4.8,color="blue", label="MLC-LLM")
    dataframe = pd.read_csv('memory_py.cvs')
    plt.plot(dataframe["time"], dataframe["used_ram"] + 1,color="red", label="PyTorch")

    # lines for better visualization
    plt.axvline(x=7, color='lightblue', linestyle='-', label="Upload MLC")
    plt.axvline(x=7.32, color='pink', linestyle='-', label="Upload PyTorch")
    plt.axvline(x=7+5.7+0.22, color='lightblue', linestyle='--', label="Generation MLC")
    plt.axvline(x=7.32+0.22+27.76, color='pink', linestyle='--', label="Generation PyTorch")

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