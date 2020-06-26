#!/usr/bin/env python3

# tshock startup script

# this script is meant to be ran as root in a docker container
# need python3.5 compat to run within official docker hub mono image :(

import argparse
import os
import sys
import subprocess
import shlex
import tempfile
import shutil
import warnings
from pathlib import Path
from functools import partial

PUID=int(os.environ.get("PUID", 1001))
PGID=int(os.environ.get("PGID", 1001))

TERRARIA_DIRS = ("/config", "/world", "/logs", "/plugins", "/tshock")

shell = partial(subprocess.check_call, shell=True)

def is_in_tty():
    return sys.__stdin__.isatty()

def update_user_and_group_ids():
    shell("usermod -u {} terraria".format(PUID))
    shell("groupmod -g {} terraria".format(PGID))

def change_owner(file, user="terraria"):
    return shell('chown -R {} "{}"'.format(user, Path(file).absolute()))

def fix_permissions():
    for d in map(Path, TERRARIA_DIRS):
        if d.stat().st_uid != PUID:
            print("chown terraria {}/* ...".format(d))
            change_owner(d)


def copy_plugins(source_folder="/tshock/ServerPlugins"):
    source_folder = Path(source_folder).absolute()
    with tempfile.TemporaryDirectory() as tmp:
        tmp = Path(tmp).absolute()
        shell('''rsync -a "{}/" "{}/" '''.format(source_folder, tmp))
        shell('''rsync -a --delete --exclude='*TShockAPI.dll*' --exclude=".*" /plugins/ "{}" '''.format(source_folder))
        shell('''rsync -a "{}/" "{}/" '''.format(tmp, source_folder))
        change_owner(source_folder)

def process_mono_flags():
    flags="--desktop"
    mem_bytes = os.sysconf('SC_PAGE_SIZE') * os.sysconf('SC_PHYS_PAGES')
    if mem_bytes > 2 * 1024 * 1024:
        flags="--server"
    return flags

def start_terraria(flags, argv):
    cmd = '''gosu terraria:terraria mono TerrariaServer.exe --gc=sgen -O=all {} -configpath /config -logpath /logs -worldpath /world'''
    cmd = cmd.format(flags)
    
    cmd = shlex.split(cmd)
    if len(argv) > 1:
        cmd += argv[1:]
    return os.execvp(cmd[0], cmd)

def _parse_tshock_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-autocreate", nargs='?', default=os.environ.get('AUTO_CREATE_WORLD'))
    parser.add_argument("-world", nargs='?', default=os.environ.get('WORLD_PATH'))
    args, _ = parser.parse_known_args()
    return args

def fix_world_path(world: str):
    # some tryhard to find a valid world path
    world_path = Path(world)
    if not world_path.exists():
        if not world_path.suffix:
            world_path = Path(world + '.wld')
        if len(world_path.parents) == 0:
            world_path = Path("/world", world_path.name)
        if not world_path.exists():
            world_path = Path("/world", world_path.name)
            if not world_path.exists():
                world_path = Path(world)
                warnings.warn("World file {} not found".format(world_path))
            else:
                warnings.warn("Using world file \"{}\" instead of \"{}\"".format(world_path.absolute(), world))
    return world_path


def list_worlds():
    return sorted(Path('/world').glob('**/*.wld'), key=lambda p: p.stat().st_mtime)

def get_world_and_edit_argv():
    args = _parse_tshock_arguments()
    if args.autocreate:
        return sys.argv[:]


    if args.world:
        world = fix_world_path(args.world)
        return [arg if arg != args.world else str(world) for arg in sys.argv]
    
    worlds = list_worlds()
    if len(worlds) >= 1:
        world = worlds[-1]
        if len(worlds) > 1:
            warnings.warn("There's {} worlds in the world folder. Choosing \"{}\" as world file".format(len(worlds), world))
        else:
            print("using world \"{}\"".format(world))
        
        return sys.argv + ['-world', str(world)]
    if len(worlds) == 0 and not is_in_tty():
        raise RuntimeError("Provide a world with \"-world\" argument !")
    return sys.argv[:]
    

if __name__ == "__main__":
    update_user_and_group_ids()
    copy_plugins()
    fix_permissions()
    flags = process_mono_flags()
    argv = get_world_and_edit_argv()
    start_terraria(flags, argv)
    
    