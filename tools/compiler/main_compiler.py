import subprocess
import os
import sys

# ====================================================================
# MASTER COMPILER ORCHESTRATOR (main_compiler.py)
# Purpose: Executes the ChronoForge compilation pipeline sequentially.
# ====================================================================

def run_compiler_pipeline():
    """
    Orchestrates the two-step compilation process.
    """
    
    # Define the base directory (where this script lives)
    tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    
    # 1. Define the component script paths
    # These must match the exact file names in your /tools directory
    stage_folder_script = os.path.join(tools_path, "compiler/source_stage_to_json_compiler.py")
    bit_packer_script = os.path.join(tools_path, "compiler/json_to_mem_compiler.py")

    print("=====================================================")
    print("     CHRONOFORGE MASTER COMPILER STARTING")
    print("=====================================================\n")

    # --- STEP 1: FOLDING STAGE DATA ---
    print(">>>STEP 1: FOLDING STAGE DATA (source_stage_to_json_compiler.py)")
    print("Reading individual stage files and unifying them into 3 JSON sources...")
    
    try:
        # Execute the Stage Folder script
        # sys.executable ensures we use the same Python interpreter currently running this script
        result = subprocess.run([sys.executable, stage_folder_script], check=True, capture_output=True, text=True)
        
        # Print the output from the subprocess for visibility
        print("\n" + result.stdout)
        
        if result.stderr:
            print("--- STAGE 1 WARNINGS/ERRORS ---\n" + result.stderr)
            
    except subprocess.CalledProcessError as e:
        print("\nCRITICAL FAILURE in STAGE 1: Stage Folding failed.")
        print(f"Error Code: {e.returncode}")
        print("--- STAGE 1 ERROR OUTPUT ---\n" + e.stderr)
        return # Stop the pipeline on failure
    except FileNotFoundError:
        print(f"\nCRITICAL FAILURE: Could not find script at {stage_folder_script}")
        return

    # --- STEP 2: BIT-PACKING AND ROM GENERATION ---
    print("")
    print(">>>STEP 2: BIT-PACKING (json_to_mem_compiler.py)")
    print("Encoding unified JSON sources into fixed-width .mem files...")

    try:
        # Execute the Bit Packer script
        result = subprocess.run([sys.executable, bit_packer_script], check=True, capture_output=True, text=True)
        
        # Print the output from the subprocess
        print("\n" + result.stdout)
        
        if result.stderr:
            print("--- STAGE 2 WARNINGS/ERRORS ---\n" + result.stderr)
            
    except subprocess.CalledProcessError as e:
        print("\nCRITICAL FAILURE in STAGE 2: Bit-Packing failed.")
        print(f"Error Code: {e.returncode}")
        print("--- STAGE 2 ERROR OUTPUT ---\n" + e.stderr)
        return
    except FileNotFoundError:
        print(f"\nCRITICAL FAILURE: Could not find script at {bit_packer_script}")
        return

    print("\n=====================================================")
    print("COMPILATION PIPELINE SUCCESSFUL!")
    print("The memory files are ready in your /mem directory.")
    print("=====================================================")

# ----------------------------
# Execution
# ----------------------------
if __name__ == "__main__":
    run_compiler_pipeline()