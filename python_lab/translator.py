import json
import os

# ----------------------------
# Bit pack helper
# ----------------------------
def pack_bits(value, width):
    """Convert integer `value` into a binary string with fixed bit width."""
    return format(value, '0{}b'.format(width))


# ----------------------------
# Encode Game Manager Data
# ----------------------------
def encode_game_manager(entry):
    bits = ""
    bits += pack_bits(entry["stage"], 8)
    bits += pack_bits(entry["attack_combo"], 10)
    bits += pack_bits(entry["ground_type"], 4)
    bits += pack_bits(entry["wait_time"], 8)
    bits += pack_bits(entry["free(unused)"], 2)
    return bits


# ----------------------------
# Encode Attack Object Data
# ----------------------------
def encode_attack(entry):
    bits = ""
    bits += pack_bits(entry["type"], 5)
    bits += pack_bits(entry["colider_type"], 2)
    bits += pack_bits(entry["movement_direction"], 3)
    bits += pack_bits(entry["speed"], 2)
    bits += pack_bits(entry["pos_x"], 8)
    bits += pack_bits(entry["pos_y"], 8)
    bits += pack_bits(entry["w"], 8)
    bits += pack_bits(entry["h"], 8)
    bits += pack_bits(entry["time"], 8)
    bits += pack_bits(entry["free(unused)"], 3)
    return bits


# ----------------------------
# Convert binary string → hex (optional)
# ----------------------------
def bin_to_hex(bitstring):
    return format(int(bitstring, 2), '08X')  # 32-bit fixed hex


# ----------------------------
# Main builder
# ----------------------------
def build_mem(input_json_path, output_mem_path, encoder, hex_output=False):
    with open(input_json_path, "r") as f:
        data = json.load(f)["decimal_data"]

    lines = []
    for entry in data:
        bitstring = encoder(entry)
        if hex_output:
            line = bin_to_hex(bitstring)
        else:
            line = bitstring
        lines.append(line)

    with open(output_mem_path, "w") as f:
        f.write("\n".join(lines))

    print(f"Written {len(lines)} entries → {output_mem_path}")


# ----------------------------
# Usage
# ----------------------------
if __name__ == "__main__":
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

    isHex = 0

    # Build Game Manager .mem (binary)
    build_mem(
        os.path.join(BASE_DIR, "data", "game_manager.json"),
        os.path.join(BASE_DIR, "output", "game_manager.mem"),
        encode_game_manager,
        hex_output=isHex
    )

    # Build Attack Objects .mem (binary)
    build_mem(
        os.path.join(BASE_DIR, "data", "attack_object.json"),
        os.path.join(BASE_DIR, "output", "attack_object.mem"),
        encode_attack,
        hex_output=isHex
    )
