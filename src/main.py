import os

def run_model():
    # process input -> generate response
    # -> process output -> update memory
    
    pass

if __name__ == "__main__":
    # check for internet
    if (os.WEXITSTATUS(os.system("curl --max-time 3 https://google.com > /dev/null 2>&1")) == 28):
        print("No Internet access  ✔ ✔ ✔")
    else:
        print("Internet access ✘ ✘ ✘")
    run_model()