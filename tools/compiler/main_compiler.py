import subprocess
import os
import sys

# ====================================================================
# MASTER COMPILER ORCHESTRATOR (main_compiler.py)
# Purpose: Executes the ChronoForge compilation pipeline sequentially.
# ====================================================================

def run_compiler_pipeline():
    """
    Orchestrates the multi-step compilation process.
    """

    # Base tools directory
    tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    # Compiler scripts
    stage_gameplay_script = os.path.join(
        tools_path, "compiler/source_stage_to_json_compiler.py"
    )

    stage_ui_script = os.path.join(
        tools_path, "compiler/source_stage_ui_to_json_compiler.py"
    )

    bit_packer_script = os.path.join(
        tools_path, "compiler/json_to_mem_compiler.py"
    )

    print("=====================================================")
    print("     CHRONOFORGE MASTER COMPILER STARTING")
    print("=====================================================\n")

    # --------------------------------------------------
    # STEP 1: GAMEPLAY STAGE FOLDING
    # --------------------------------------------------
    print(">>> STEP 1: FOLDING GAMEPLAY STAGES")
    print("Running source_stage_to_json_compiler.py ...")

    if not run_step(stage_gameplay_script, "STAGE 1"):
        return

    # --------------------------------------------------
    # STEP 2: UI STAGE FOLDING
    # --------------------------------------------------
    print("\n>>> STEP 2: FOLDING UI STAGES")
    print("Running source_stage_ui_to_json_compiler.py ...")

    if not run_step(stage_ui_script, "STAGE 2"):
        return

    # --------------------------------------------------
    # STEP 3: BIT PACKING
    # --------------------------------------------------
    print("\n>>> STEP 3: BIT PACKING & ROM GENERATION")
    print("Running json_to_mem_compiler.py ...")

    if not run_step(bit_packer_script, "STAGE 3"):
        return

    print("\n=====================================================")
    print("COMPILATION PIPELINE SUCCESSFUL!")
    print("The memory files are ready in your /mem directory.")
    print("=====================================================")


# --------------------------------------------------------------------
# Helper to run one compiler step
# --------------------------------------------------------------------
def run_step(script_path: str, stage_name: str) -> bool:
    try:
        result = subprocess.run(
            [sys.executable, script_path],
            check=True,
            capture_output=True,
            text=True
        )

        print("\n" + result.stdout)

        if result.stderr:
            print(f"--- {stage_name} WARNINGS/ERRORS ---\n{result.stderr}")

        return True

    except subprocess.CalledProcessError as e:
        print(f"\nCRITICAL FAILURE in {stage_name}")
        print(f"Error Code: {e.returncode}")
        print(f"--- {stage_name} ERROR OUTPUT ---\n{e.stderr}")
        return False

    except FileNotFoundError:
        print(f"\nCRITICAL FAILURE: Script not found → {script_path}")
        return False


# --------------------------------------------------------------------
# Execution
# --------------------------------------------------------------------
if __name__ == "__main__":
    run_compiler_pipeline()
