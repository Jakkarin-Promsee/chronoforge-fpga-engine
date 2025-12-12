import json
import tkinter as tk
from tkinter import filedialog, ttk


# ======================
# Load JSON file
# ======================
def load_json():
    path = filedialog.askopenfilename(
        title="Select stageXX.json",
        filetypes=(("JSON Files", "*.json"), ("All Files", "*.*"))
    )
    if not path:
        return
    
    global data, gm, attack_objects, platform_objects
    with open(path, "r") as f:
        data = json.load(f)

    gm = data["game_manger"]
    attack_objects = data["attack_object"]
    platform_objects = data["platform_object"]

    draw_stage()
    update_list()


# ======================
# Draw everything
# ======================
def draw_stage():
    canvas.delete("all")

    # Draw Display Area
    x1 = gm["display_pos_x1"]
    y1 = gm["display_pos_y1"]
    x2 = gm["display_pos_x2"]
    y2 = gm["display_pos_y2"]

    canvas.create_rectangle(x1, y1, x2, y2, outline="yellow", width=2)
    canvas.create_text(x1, y1 - 10, text="Display Area", fill="yellow", anchor="sw")

    # Draw Attack Objects
    for i, obj in enumerate(attack_objects):
        canvas.create_rectangle(
            obj["pos_x"],
            obj["pos_y"],
            obj["pos_x"] + obj["w"],
            obj["pos_y"] + obj["h"],
            outline="red"
        )

    # Draw Platform Objects
    for i, obj in enumerate(platform_objects):
        canvas.create_rectangle(
            obj["pos_x"],
            obj["pos_y"],
            obj["pos_x"] + obj["w"],
            obj["pos_y"] + obj["h"],
            outline="cyan"
        )


# ======================
# Highlight selected object
# ======================
def highlight(event=None):
    canvas.delete("highlight")

    index = listbox.curselection()
    if not index:
        return

    idx = index[0]

    # Attack objects first
    if idx < len(attack_objects):
        obj = attack_objects[idx]
    else:
        obj = platform_objects[idx - len(attack_objects)]

    canvas.create_rectangle(
        obj["pos_x"],
        obj["pos_y"],
        obj["pos_x"] + obj["w"],
        obj["pos_y"] + obj["h"],
        outline="white",
        width=3,
        tags="highlight"
    )


# ======================
# Update object list
# ======================
def update_list():
    listbox.delete(0, tk.END)

    # Attack objects
    for i, obj in enumerate(attack_objects):
        listbox.insert(tk.END, f"Attack {i}: type={obj['type']} at ({obj['pos_x']},{obj['pos_y']})")

    # Platforms
    for i, obj in enumerate(platform_objects):
        listbox.insert(tk.END, f"Platform {i}: ({obj['pos_x']},{obj['pos_y']})")


# ======================
# GUI Setup
# ======================
root = tk.Tk()
root.title("ChronoForge Stage Viewer")
root.geometry("1000x600")

# Canvas for drawing
canvas = tk.Canvas(root, bg="black", width=640, height=480)
canvas.pack(side="left", padx=10, pady=10)

# Right panel
right_frame = tk.Frame(root)
right_frame.pack(side="right", fill="y")

# Load button
load_btn = tk.Button(right_frame, text="Load stageXX.json", command=load_json)
load_btn.pack(pady=5)

# Listbox for objects
listbox = tk.Listbox(right_frame, width=40, height=30)
listbox.pack(pady=10)
listbox.bind("<<ListboxSelect>>", highlight)


root.mainloop()