import json
import os
import glob

# ====================================================================
# UI STAGE FOLDER SCRIPT
# Purpose: Fold stage_ui_XX.json into unified UI + Character JSON files
# ====================================================================

# tools/main/
TOOLS_PATH = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Input
STAGE_DATA_DIR = os.path.join(TOOLS_PATH, "json_stage_ui_source")
STAGE_FILE_PATTERN = "stage_ui_*.json"

# Output
UNIFIED_JSON_DIR = os.path.join(TOOLS_PATH, "json-source-decode")

GAME_UI_OUT = os.path.join(UNIFIED_JSON_DIR, "game_ui.json")
CHARACTER_OUT = os.path.join(UNIFIED_JSON_DIR, "character_object.json")


# --------------------------------------------------------------------
# Core Folding Logic
# --------------------------------------------------------------------
def fold_stages_to_json():
    print(f"--- Starting UI Stage Folding Process ---")

    # Master streams
    game_ui_master = []
    character_master = []

    # Find & sort stage files
    stage_files = glob.glob(os.path.join(STAGE_DATA_DIR, STAGE_FILE_PATTERN))
    stage_files.sort()

    if not stage_files:
        print(f"ERROR: No UI stage files found in {STAGE_DATA_DIR}")
        return False

    print(f"[Found {len(stage_files)} UI stages]")

    # Process each stage
    for idx, filepath in enumerate(stage_files):
        filename = os.path.basename(filepath)

        try:
            with open(filepath, "r") as f:
                stage_data = json.load(f)
        except json.JSONDecodeError as e:
            print(f"CRITICAL ERROR: Invalid JSON in {filename}: {e}")
            continue

        # ---- game_ui (exactly ONE per stage) ----
        if "game_ui" not in stage_data:
            print(f"WARNING: {filename} missing 'game_ui'")
        else:
            game_ui_master.append(stage_data["game_ui"])

        # ---- character_object (0..N per stage) ----
        if "character_object" in stage_data:
            if isinstance(stage_data["character_object"], list):
                character_master.extend(stage_data["character_object"])
            else:
                print(f"WARNING: 'character_object' is not a list in {filename}")

    # Write outputs
    os.makedirs(UNIFIED_JSON_DIR, exist_ok=True)

    with open(GAME_UI_OUT, "w") as f:
        json.dump({"decimal_data": game_ui_master}, f, indent=4)

    with open(CHARACTER_OUT, "w") as f:
        json.dump({"decimal_data": character_master}, f, indent=4)

    print("\n--- Writing Unified UI JSON Sources ---")
    print(f"Wrote {len(game_ui_master):>4} entries -> {os.path.basename(GAME_UI_OUT)}")
    print(f"Wrote {len(character_master):>4} entries -> {os.path.basename(CHARACTER_OUT)}")
    print("--- Folding Complete! ---")

    return True


# --------------------------------------------------------------------
# Execution
# --------------------------------------------------------------------
if __name__ == "__main__":
    if fold_stages_to_json():
        print("\nNext Step: Run 'json_to_mem_compiler.py' to generate the final .mem files.")
