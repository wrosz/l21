PATH_TO_VARISAT = "varisat.exe"  # must be in the same directory as this script, or provide the correct path to the Varisat executable
import subprocess
import time

def check_satisfiability(cnf_file, path_to_varisat, output_file=None, timeout=None):
    if output_file is None:
        output_file = f"{cnf_file}.proof"

    time_start = time.time()

    try:
        result = subprocess.run(
            [
                path_to_varisat,
                '--proof', output_file,
                '--proof-format', 'DRAT',
                cnf_file
            ],
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - time_start
        return None, elapsed_time

    if "s SATISFIABLE" in result.stdout:
        satisfiable = True
    elif "s UNSATISFIABLE" in result.stdout:
        satisfiable = False
    else:
        raise Exception(
            f"Unexpected output from Varisat:\n{result.stdout}\n{result.stderr}"
        )

    elapsed_time = time.time() - time_start
    return satisfiable, elapsed_time