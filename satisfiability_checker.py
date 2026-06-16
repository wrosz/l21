PATH_TO_VARISAT = "varisat.exe"  # must be in the same directory as this script, or provide the correct path to the Varisat executable
import subprocess
import os
import time

import subprocess
import time

def check_satisfiability(cnf_file, output_file=None, timeout=None):
    if output_file is None:
        output_file = f"{cnf_file}.proof"

    time_start = time.time()

    try:
        result = subprocess.run(
            [
                PATH_TO_VARISAT,
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


def main():
    sat_files = os.listdir("test_files/dimacs_formulas/sat")
    unsat_files = os.listdir("test_files/dimacs_formulas/unsat")
    results = []
    errors = []
    for sat_file in sat_files + unsat_files:
        print(f"Checking satisfiability for file: {sat_file}")
        try:
            if sat_file in sat_files:
                cnf_file_path = os.path.join("test_files/dimacs_formulas/sat", sat_file)
                output_file_path = os.path.join("proofs", f"sat_{sat_file}.proof")
                should_be_satisfiable = True
            else:
                cnf_file_path = os.path.join("test_files/dimacs_formulas/unsat", sat_file)
                output_file_path = os.path.join("proofs", f"unsat_{sat_file}.proof")
                should_be_satisfiable = False
            satisfiable, elapsed_time = check_satisfiability(cnf_file_path, output_file_path, timeout=5)
            results.append((sat_file, satisfiable, elapsed_time, should_be_satisfiable))
            print(f"File: {sat_file}, Satisfiable: {satisfiable}, Time taken: {elapsed_time:.4f} seconds")
        except Exception as e:
            print(f"Error occurred while checking file: {sat_file}, Error: {e}")
            errors.append((sat_file, str(e)))
    with open("satisfiability_results.csv", "w") as f:
        f.write("File, Satisfiable, Time taken (seconds), Should be Satisfiable\n")
        for sat_file, satisfiable, elapsed_time, should_be_satisfiable in results:
            f.write(f"{sat_file}, {satisfiable}, {elapsed_time:.4f}, {should_be_satisfiable}\n")
        f.close()
    if errors:
        with open("satisfiability_errors.txt", "w") as f:
            f.write("\nErrors:\n")
            for sat_file, error in errors:
                f.write(f"{sat_file}: Error: {error}\n")
        f.close()


if __name__ == "__main__":
    main()
    

