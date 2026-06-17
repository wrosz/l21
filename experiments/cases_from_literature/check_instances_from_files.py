import os

# set the project root to the parent directory of the src folder
from pathlib import Path
import sys
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

PATH_TO_VARISAT = "varisat.exe"  # must be in the same directory as this script, or provide the correct path to the Varisat executable
from src.utils.check_satisfiability import check_satisfiability


def main():
    sat_files = os.listdir("experiments/cases_from_literature/test_files/dimacs_formulas/sat")
    unsat_files = os.listdir("experiments/cases_from_literature/test_files/dimacs_formulas/unsat")
    results = []
    errors = []

    for sat_file in sat_files + unsat_files:
        print(f"Checking satisfiability for file: {sat_file}")

        try:
            if sat_file in sat_files:
                cnf_file_path = os.path.join("experiments/cases_from_literature/test_files/dimacs_formulas/sat", sat_file)
                should_be_satisfiable = True
            else:
                cnf_file_path = os.path.join("experiments/cases_from_literature/test_files/dimacs_formulas/unsat", sat_file)
                should_be_satisfiable = False
                
            output_file_path = os.path.join("experiments/cases_from_literature/proofs", f"{sat_file.split('.')[0]}.proof")
            satisfiable, elapsed_time = check_satisfiability(cnf_file_path, PATH_TO_VARISAT, output_file_path, timeout=120)
            results.append((sat_file, satisfiable, elapsed_time, should_be_satisfiable))
            print(f"File: {sat_file}, Satisfiable: {satisfiable}, Time taken: {elapsed_time:.4f} seconds, should be satisfiable: {should_be_satisfiable}")

        except Exception as e:
            print(f"Error occurred while checking file: {sat_file}, Error: {e}")
            errors.append((sat_file, str(e)))

    with open("experiments/cases_from_literature/satisfiability_results.csv", "w") as f:
        f.write("File, Satisfiable, Time taken (seconds), Should be Satisfiable\n")
        for sat_file, satisfiable, elapsed_time, should_be_satisfiable in results:
            f.write(f"{sat_file}, {satisfiable}, {elapsed_time:.4f}, {should_be_satisfiable}\n")
        f.close()

    if errors:
        with open("experiments/cases_from_literature/satisfiability_errors.txt", "w") as f:
            f.write("\nErrors:\n")
            for sat_file, error in errors:
                f.write(f"{sat_file}: Error: {error}\n")
        f.close()


if __name__ == "__main__":
    main()
