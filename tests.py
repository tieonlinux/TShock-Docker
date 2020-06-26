import unittest
import random
import subprocess
import os
import sys
from pathlib import Path
import urllib.request
import zipfile
import io
import shutil
import shlex
import re
import time
import json
import requests
from typing import Optional, Union, Collection, Set, Callable, Dict
from datetime import timedelta
import tempfile
import asyncio
import hashlib
import threading
import getpass
import traceback


try:
    from pwd import getpwnam
except ImportError:
    def getpwnam(*args, **kwargs):
        raise NotImplementedError()
import warnings

OptionalPath = Union[None, Path, str]
PUID = 1756 # aka container user id
try:
    _user_name = getpass.getuser()
    if _user_name != 'root':
        uid = getpwnam(_user_name).pw_uid
        if uid != 0:
            PUID = uid
except:
    warnings.warn("Unable to find current username\n" + traceback.format_exc())

def download_map(url=r"https://github.com/TEdit/Terraria-Map-Editor/raw/5c4afae20b/tests/World%20Files%201.4.0.3/SM_Classic.wld", dest: OptionalPath=None):
    if dest is None:
        dest = "/data/terraria/worlds"
    dest: Path = Path(dest)
    target_file_name = f'world_{random.randint(0, 2 ** 32)}.wld'
    target = Path(dest, target_file_name)
    with urllib.request.urlopen(url) as response, target.open('wb') as f:
        shutil.copyfileobj(response, f)
    return target


def download_plugin(url=r"https://github.com/tieonlinux/TDiffBackup/releases/download/v1.1.0/DiffBackup.dll", dest: OptionalPath=None):
    if dest is None:
        dest = "/data/terraria/plugins"
    dest: Path = Path(dest)
    target_file_name = f'DiffBackup.dll'
    target = Path(dest, target_file_name)
    with urllib.request.urlopen(url) as response, target.open('wb') as f:
        shutil.copyfileobj(response, f)
    return target


def hash_bytes(b: bytes) -> int:
    m = hashlib.sha256()
    m.update(b)
    return int.from_bytes(m.digest(), "big")


class PopenBuffer(threading.Thread):
    def __init__(self, popen, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = threading.Event()
        self.popen: subprocess.Popen = popen
        self.buff = io.BytesIO()
        self.setDaemon(True)
        self.start()
        self._condition = threading.Condition()
        self._condition_listener_counter = 0

    def run(self, *args, **kwargs):
        while not self.event.is_set():
            try:
                line = self.popen.stdout.readline()
            except:
                if self.popen.returncode is not None:
                    break
                else:
                    raise
            else:
                self.buff.write(line)
                if self._condition_listener_counter > 0:
                    with self._condition:
                        if self._condition_listener_counter > 0:
                            self._condition.notify_all()

    def wait_for_new_line(self, timeout=None):
        with self._condition:
            self._condition_listener_counter += 1
            try:
                return self._condition.wait(timeout=timeout)
            finally:
                self._condition_listener_counter -= 1

    def wait_for_new_line_with_pred(self, predicate, timeout=None):
        with self._condition:
            self._condition_listener_counter += 1
            try:
                return self._condition.wait_for(predicate, timeout=timeout)
            finally:
                self._condition_listener_counter -= 1

    def read(self) -> bytes:
        return self.buff.getvalue()

    def clear(self):
        self.buff = io.BytesIO()

    def stop(self):
        self.event.set()

def setup_tshock(world_path: Path, cwd: OptionalPath=None):
    if cwd is None:
        cwd = './'
    cwd = Path(cwd)
    path_mapping = dict()
    for p in ('config', 'logs', 'world', 'plugins'):
        path = Path(cwd, p)
        path.mkdir(parents=True, exist_ok=True)
        path_mapping[p] = path.absolute()
    shutil.copy2(str(world_path), str(Path(cwd, 'world').absolute()))

    download_plugin(dest=path_mapping['plugins'])

    start = time.monotonic()
    docker_create = f"""docker run -d -p 7777:7777 -p 7878:7878 -e PUID={PUID} -v {path_mapping['config']}:/config -v {path_mapping['logs']}:/logs -v {path_mapping['world']}:/world -v {path_mapping['plugins']}:/plugins --name="terraria" tshock_testing -world "/world/{world_path.name}" --stats-optout -lang english"""
    print("using cmd", docker_create)
    subprocess.check_call(docker_create, shell=True, text=True, cwd=str(cwd.absolute()))
    try:
        while not Path(path_mapping['config'], "config.json").exists():
            time.sleep(5)
            if time.monotonic() - start > timedelta(minutes=2).total_seconds():
                raise TimeoutError("unable to get TShock ready")
        else:
            time.sleep(15)
    finally:
        subprocess.check_call("docker stop terraria", shell=True, text=True)
            
    json_config_path = Path(path_mapping['config'], "config.json")
    config = json.loads(json_config_path.read_text())
    assert "RestApiEnabled" in config
    config["RestApiEnabled"] = True
    config['RestApiPort'] = 7878
    config["EnableTokenEndpointAuthentication"] = True
    config["ApplicationRestTokens"] = {
        "TESTTOKEN": {
        "Username": "Server",
        "UserGroupName": "superadmin"
    }}
    json_config_path.write_text(json.dumps(config))
    stdout = subprocess.PIPE
    p = subprocess.Popen(shlex.split("docker start --attach terraria"), bufsize=2**16, stdout=stdout, stderr=subprocess.STDOUT, stdin=subprocess.PIPE)
    pbuff = PopenBuffer(p)
    while b"Server started" not in pbuff.read():
        time.sleep(1)
        if time.monotonic() - start > timedelta(minutes=3).total_seconds():
            raise TimeoutError("unable to start the server")
    assert p.returncode is None

    r = requests.get(f"http://127.0.0.1:{config['RestApiPort']}/tokentest?token=TESTTOKEN")
    r.raise_for_status()
    return config, p, path_mapping, pbuff

class IntegrationTest(unittest.TestCase):
    world_path: Path
    server_config: dict
    server_process: subprocess.Popen
    tmp_dir: tempfile.TemporaryDirectory
    pbuff: PopenBuffer
    path_mapping: Dict[str, Path]

    @property
    def mapped_world_path(self) -> Path:
        return Path(self.path_mapping['world'], self.world_path.name)

    def setUp(self):
        self.tmp_dir = tempfile.TemporaryDirectory()
        self.world_path = download_map(dest=self.tmp_dir.name)
        self.server_config, self.server_process, self.path_mapping, self.pbuff = setup_tshock(self.world_path, cwd=self.tmp_dir.name)

    def tearDown(self):
        try:
            self.server_process.kill()
            self.server_process.wait(15)
            self.tmp_dir.cleanup()
            self.pbuff.stop()
            try:
                subprocess.check_call("docker stop terraria", shell=True, text=True)
            except subprocess.CalledProcessError:
                pass
        finally:
            subprocess.check_call("docker rm --force terraria", shell=True, text=True)
        

    def wait_for_ouput(self, pattern: Union[bytes, Callable, re.Pattern], timeout=None, buff=b"", clear=True) -> bytes:
        def is_a_match(buff):
            if isinstance(pattern, re.Pattern):
                return re.match(pattern, buff)
            if callable(pattern):
                return pattern(buff)
            return pattern in buff

        t = time.monotonic()
        c = 0
        while timeout is None or time.monotonic() - t < timeout:
            if is_a_match(buff):
                break
            if c > 0:
                wait_timeout = None
                if timeout is not None:
                    wait_timeout = timeout - (time.monotonic() - t)
                    wait_timeout = max(wait_timeout, 0.1)
                self.pbuff.wait_for_new_line(timeout=wait_timeout)
            buff = self.pbuff.read()
            c += 1
        else:
            raise TimeoutError(f"could not found given pattern for {timeout} seconds ({c} iterations)")
        if clear:
            self.pbuff.clear()
        return buff
            

    def save_world_file(self):
        r = requests.get(f"http://127.0.0.1:{self.server_config['RestApiPort']}/v2/world/save?token=TESTTOKEN", timeout=15)
        r.raise_for_status()
        data = r.json()
        
        buff = self.wait_for_ouput(b'World saved', timeout=30)

        return data, buff
        
    def test_save_world(self):
        original_stat = self.mapped_world_path.stat()
        self.save_world_file()
        self.assertGreater(self.mapped_world_path.stat().st_mtime, original_stat.st_mtime)

    def test_file_owner_are_set_to_puid(self):
        for d in ('config', 'logs', 'world', 'plugins'):
            p = self.path_mapping[d]
            self.assertEqual(str(PUID), str(p.stat().st_uid))
            for file_path in p.glob('**/*'):
                self.assertEqual(str(PUID), str(file_path.stat().st_uid))

    def test_plugin_is_loaded(self):
        cmd = '/tdiff'
        r = requests.get(f"http://127.0.0.1:{self.server_config['RestApiPort']}/v3/server/rawcmd", {'token': 'TESTTOKEN', 'cmd': cmd}, timeout=15)
        r.raise_for_status()
        data = r.json()
        self.assertEqual('200', str(data.get('status')))
        
        needle = f'Server executed: {cmd}.'.encode()
        haystack = self.wait_for_ouput(needle, timeout=30)

        self.assertIn(needle, haystack)
    


if __name__ == '__main__':
    unittest.main()