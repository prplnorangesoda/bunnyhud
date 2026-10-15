# Building utility script.
# Lightly based on https://github.com/Predi-i/Deadlock-Mod-Compiler

import os,subprocess,sys,shutil
from pathlib import Path

MOD_NAME = "bunhud"
INPUT_DIR = "./mod"
OUTPUT_DIR = os.environ.get("BUNHUD_OUTPUT_DIR", "dist")
VPK = os.environ.get("BUNHUD_OUTPUT_VPK", "pak67_dir.vpk")

CSDK12_ROOT=os.environ.get("CSDK12_ROOT", "CSDK12")
RESOURCECOMPILER_PATH = os.path.join(CSDK12_ROOT, "game/bin_cs2/win64/resourcecompiler.exe")
MOD_BUILD_PATH = os.path.join(CSDK12_ROOT, "content/citadel_addons", MOD_NAME)
MOD_COMPILED_PATH = os.path.join(CSDK12_ROOT, "game/citadel_addons", MOD_NAME)

def fatal(message: str, code: int = 1):
    print("")
    print("!!!! building FATAL ERROR: !!!!")
    print("")
    print("")
    print(message)
    if code != 1:
        print("error code" + str(code))
    print("")
    
    exit(code or 1)

def main():
    print("BUILD [1/2] Compiling files")
    
    if Path(MOD_BUILD_PATH).is_dir():
        shutil.rmtree(MOD_BUILD_PATH)
    elif Path(MOD_BUILD_PATH).is_file():
        os.remove(MOD_BUILD_PATH)

    shutil.copytree(INPUT_DIR, MOD_BUILD_PATH)

    compile_command: list[str] = []

    if sys.platform == "linux":
        compile_command.append("wine")

    compile_command.append(RESOURCECOMPILER_PATH)

    for file_path in Path(MOD_BUILD_PATH).rglob("*"):
        if not file_path.is_file():
            continue

        compile_command.append("-i")
        if sys.platform == "linux":
            compile_command.append("Z:" + file_path.as_posix())
        else:
            compile_command.append(file_path.as_posix())
        print(file_path)

    print("using", str(compile_command))
    proc = subprocess.run(compile_command, env={**os.environ, "WINEDEBUG": "fixme-all"})
    if proc.returncode != -9:
        fatal("compilation failed.")

    print("BUILD [2/2] Creating VPK")
    subprocess.run(["Source2Viewer-CLI", "-i", MOD_COMPILED_PATH, "--vpk_create", os.path.join(OUTPUT_DIR, VPK)])

if __name__ == "__main__":
    main()