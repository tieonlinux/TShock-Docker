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

LAST_WORLD_LOCATION_FILE = '/var/run/tshock/last_world.txt'
TERRARIA_DIRS = ("/config", "/world", "/logs", "/plugins", "/tshock")

shell = partial(subprocess.check_call, shell=True)

def _env_text_to_bool(text, default=None, match_positive=True):
    if text is None:
        return default
    text = text.lower().strip()
    if match_positive:
        return text in ('true', 'y', 'yes', '1', 't', '+')
    return text not in ('false', 'n', 'no', '0', 'f', '-', '')

def env_bool(name, default=None, match_positive=True):
    return _env_text_to_bool(os.environ.get(name), default=default, match_positive=match_positive)


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
    parser.add_argument("-autocreate", action='store_true', default=env_bool('AUTO_CREATE_WORLD'))
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
    res = sorted(Path('/world').glob('*.wld'), key=lambda p: p.stat().st_mtime)
    if len(res) <= 0 and env_bool("DEEP_SEARCH_WORLD", True):
        res = sorted(Path('/world').glob('**/*.wld'), key=lambda p: p.stat().st_mtime)
        if len(res) > 0:
            warnings.warn("No world file found in /world folder. But a deep scan found {} worlds in sub folders".format(len(res)))
    return res


def get_last_world_location():
    p = Path(LAST_WORLD_LOCATION_FILE)
    if p.exists():
        s = p.read_text().strip()
        if Path(s).exists():
            return Path(s)
    return None

def save_last_world_location(world):
    p = Path(LAST_WORLD_LOCATION_FILE)
    if not p.parent.exists():
        p.parent.mkdir(parents=True, exist_ok=True)
        change_owner(p.parent, 'terraria:terraria')
    p.write_text(str(world))
    

def get_world_and_edit_argv():
    args = _parse_tshock_arguments()
    if args.autocreate:
        return sys.argv[:]


    if args.world:
        if not env_bool("FIX_WORLD", True):
            return sys.argv[:]
        world = fix_world_path(args.world)
        save_last_world_location(world)
        return [arg if arg != args.world else str(world) for arg in sys.argv]
    
    if env_bool("AUTO_LOAD_WORLD", True):
        world = get_last_world_location()
        if world is not None:
            return sys.argv + ['-world', str(world)]
        

        worlds = list_worlds()
        if len(worlds) >= 1:
            world = worlds[-1]
            if len(worlds) > 1:
                warnings.warn("There's {} worlds in the world folder. Choosing \"{}\" as world file".format(len(worlds), world))
            else:
                print("using world \"{}\"".format(world))
            save_last_world_location(world)
            return sys.argv + ['-world', str(world)]
        if len(worlds) == 0 and not is_in_tty():
            raise RuntimeError('''No world found. Possible solutions:
Add a world in /world volume dir
Start the container with "docker run -it ..." and generate a new world
Provide a valid world with "-world" argument''')
    return sys.argv[:]
    

def main():
    update_user_and_group_ids()
    copy_plugins()
    fix_permissions()
    flags = process_mono_flags()
    argv = get_world_and_edit_argv()
    start_terraria(flags, argv)


if __name__ == "__main__":
    main()
    
    