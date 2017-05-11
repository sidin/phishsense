import subprocess
import sc_localsettings

def run_sample_loop():
    subprocess.call(['python', sc_localsettings.SCHEDULER_SCRIPT1])

if __name__ == "__main__":
    run_sample_loop()


