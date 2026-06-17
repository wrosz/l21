import subprocess
import time

def check_satisfiability(cnf_file, path_to_varisat, output_file=None, timeout=None):
    if output_file is None:
        command = [path_to_varisat, cnf_file]
    else:
        command = [path_to_varisat, '--proof', output_file, '--proof-format', 'DRAT', cnf_file]

    time_start = time.time()

    try:
        result = subprocess.run(
            command,
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