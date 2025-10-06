import os
from .chat import run, run_UI
import subprocess
import multiprocessing
import sys
import signal

def exit_gracefully(_1, _2):
    """Cleanup.
    When quit, the app must remove the formatted disk image used to store audio recordings on RAM"""
    global ok
    if ok:
        subprocess.run(
            "./sma_llm/utils/io_pipeline/handle_read/speech_to_text/utils/rm_tmp.sh",
            shell = True
        )
        main_process.terminate()
        ok = False
    sys.exit(0)

if __name__ == "__main__":
    # check for internet
    if (os.WEXITSTATUS(os.system("curl --max-time 1 https://google.com > /dev/null 2>&1")) == 28):
        print("No Internet access  ✘ ✘ ✘")
    else:
        print("Internet access ✔ ✔ ✔")
        
    ok = False # only try to clean it once
    main_process = None

    signal.signal(signal.SIGINT, exit_gracefully)
    signal.signal(signal.SIGTERM, exit_gracefully)
    signal.signal(signal.SIGHUP, exit_gracefully)
    signal.signal(signal.SIGQUIT, exit_gracefully)


    subprocess.run(
        "./sma_llm/utils/io_pipeline/handle_read/speech_to_text/utils/tmp.sh",
        shell = True
    )
    ok = True
    main_process = multiprocessing.Process(target=run_UI)
    main_process.start()