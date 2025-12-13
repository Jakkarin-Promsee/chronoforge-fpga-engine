import os, sys, subprocess

tools_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
game_engine_path = os.path.join(tools_path, "compiler", "main_compiler.py")

subprocess.run([
    sys.executable,
    game_engine_path
])