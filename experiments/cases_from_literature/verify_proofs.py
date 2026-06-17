import os
import subprocess

# set the project root to the parent directory of the src folder
from pathlib import Path
import sys
import time
PROJECT_ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(PROJECT_ROOT))

PATH_TO_DRAT_TRIM = r"C:\msys64\home\17ros\drat-trim"
PATH_TO_UNSAT_FILES = "experiments/cases_from_literature/test_files/dimacs_formulas/unsat"
PATH_TO_PROOFS = "experiments/cases_from_literature/proofs"


def to_msys_path(path):
    path = os.path.abspath(path)
    path = path.replace("\\", "/")
    return f"/{path[0].lower()}{path[2:]}"

def verify_proof(cnf_file, proof_file, timeout=120):
    '''Verifies the proof for the given CNF file using drat-trim. Returns True if the proof is correct, False otherwise.'''
    start_time = time.time()
    path_to_drat_trim = to_msys_path(PATH_TO_DRAT_TRIM)
    
    try:
        cnf_file = to_msys_path(cnf_file)
        proof_file = to_msys_path(proof_file)
        
        result = subprocess.run(
            [
                r"C:\msys64\usr\bin\bash.exe",
                "-lc",
                f'cd {path_to_drat_trim} && ./drat-trim.exe "{cnf_file}" "{proof_file}"'
            ],
            capture_output=True,
            text=True,
            timeout=timeout
        )
    except subprocess.TimeoutExpired:
        elapsed_time = time.time() - start_time
        return None, elapsed_time


    output = result.stdout
    end_time = time.time()
    elapsed_time = end_time - start_time
    if "s VERIFIED" in output:
        return True, elapsed_time
    elif "s NOT VERIFIED" in output:
        return False, elapsed_time
    else:
        raise Exception(f"Unexpected output from drat-trim: {output}")


def main():
    with open("experiments/cases_from_literature/proof_verification_results.csv", "w") as f:
        f.write("File, Is satisfied, Proof Verified, Time taken (seconds), Did time out\n")
        f.close()
    
    for cnf_file in os.listdir(PATH_TO_UNSAT_FILES):
        print(f"Verifying proof for file: {cnf_file}")
        try:
            cnf_file_path = os.path.join(PATH_TO_UNSAT_FILES, cnf_file)
            proof_file_path = os.path.join(PATH_TO_PROOFS, f"{cnf_file.split('.')[0]}.proof")
            proof_verified, elapsed_time = verify_proof(cnf_file_path, proof_file_path, timeout=120)
            with open("experiments/cases_from_literature/proof_verification_results.csv", "a") as f:
                f.write(f"{cnf_file}, {proof_verified}, {elapsed_time:.4f}, {proof_verified is None}\n")
                f.close()
            print(f"File: {cnf_file}, Proof Verified: {proof_verified}, Time taken: {elapsed_time:.4f} seconds, Did time out: {proof_verified is None}")

        except Exception as e:
            print(f"Error occurred while verifying proof for file: {cnf_file}, Error: {e}")
            with open("experiments/cases_from_literature/proof_verification_errors.txt", "a") as f:
                f.write(f"{cnf_file}: Error: {str(e)}\n")
                f.close()


if __name__ == "__main__":
    main()
