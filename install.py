#!/usr/bin/python3

import os
import shutil
import sys
import json

"""
    Installs the IDAAutoLibcFlags plugin into your IDA plugins user directory :
    On Windows: %APPDATA%/Hex-Rays/IDA Pro
    On Linux and Mac: $HOME/.idapro

    Install: $ python3 install.py
"""


ROOT_DIR = os.path.abspath(os.path.dirname(__file__))
INSTALL = ["autolibcflags.py"]
CACHE_FILES = ["functions.json", "enum" ]

def install(where: str) -> int:
    # Remove old files
    for file in INSTALL:
        base = os.path.basename(file)
        if os.path.exists(os.path.join(where, base)):
            dst = os.path.join(where, os.path.basename(file))
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
            
    # install
    for file in INSTALL:
        src = os.path.abspath(os.path.join(ROOT_DIR, file))
        dst = os.path.join(where, os.path.basename(file))

        print(f'[install.py] Creating "{dst}"')
        is_dir = os.path.isdir(src)
        if is_dir:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy(src, dst)

    return 0


def install_cache(cache_dir : str) -> int:

    for file in CACHE_FILES:
        base = os.path.basename(file)
        if os.path.exists(os.path.join(cache_dir, base)):
            dst = os.path.join(cache_dir, os.path.basename(file))
            if os.path.isdir(dst):
                shutil.rmtree(dst)
            else:
                os.remove(dst)
            
    # install
    for file in CACHE_FILES:
        src = os.path.abspath(os.path.join(ROOT_DIR, file))
        dst = os.path.join(cache_dir, os.path.basename(file))

        print(f'[install.py] Creating "{dst}"')
        is_dir = os.path.isdir(src)
        if is_dir:
            shutil.copytree(src, dst, dirs_exist_ok=True)
        else:
            shutil.copy(src, dst)

    return 0

def main():
    # find IDA installation
    if os.name == "posix":
        ida_plugins_dir = os.path.expandvars("/$HOME/.idapro/plugins")
        cache_dir = os.path.expandvars("/$HOME/.idalibcflags/")
    elif os.name == "nt":
        ida_plugins_dir = os.path.expandvars("%APPDATA%/Hex-Rays/IDA Pro/plugins")
        cache_dir = os.path.expandvars("%APPDATA%/IdaAutoLibcFlags/")
    else:
        print(f"[install.py] Could not retrieve IDA install folder on OS {os.name}")
        exit(1)

    # make sure the "plugins" dir exists
    os.makedirs(ida_plugins_dir, exist_ok=True)
    # make sur cache folder exit
    os.makedirs(cache_dir, exist_ok=True)

    ret = install_cache(cache_dir)
    if ret == 0:
        print("[install.py] Done installed cache folder at %s" % cache_dir)
    else:
        print("[install.py] Failed to install cache : %s", cache_dir)
        sys.exit(1)
     
    ret = install(ida_plugins_dir)
    if ret == 0:
        print("[install.py] Done Installing Plugin")
    else:
        print("[install.py] Error installing")


    

if __name__ == "__main__":
    main()