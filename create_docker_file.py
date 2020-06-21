import jinja2
from jinja2 import Template, Environment
import os
import tempfile
import datetime
import subprocess
from collections import OrderedDict
import requests
from functools import lru_cache
import json
from pathlib import Path
import warnings

_DEFAULT_TSHOCK_REPO='Pryaxis/TShock'

@lru_cache(512)
def parse_github_date(d):
    return datetime.datetime.strptime(d, "%Y-%m-%dT%H:%M:%SZ")

def list_recent_tshock_release(tshock_repo=_DEFAULT_TSHOCK_REPO):
    r = requests.get(f'https://api.github.com/repos/{tshock_repo}/releases', timeout=60)
    r.raise_for_status()
    return r.json()

def get_latest_release(tshock_repo=_DEFAULT_TSHOCK_REPO):
    payload = list_recent_tshock_release(tshock_repo=tshock_repo)
    return max(payload, key=lambda d: parse_github_date(d['published_at']))


def get_release_asset(release: dict):
    for asset in release['assets']:
        name = asset['name'].lower()
        if name.endswith('zip') and name.startswith('tshock'):
            return asset
    else:
        raise ValueError("unable to find valid asset")

def filter_quote(s: str, quote='"', escape='\\"') -> str:
    return f'"{str(s).replace(quote, escape)}"'

def gen_default_labels():
    yield "maintainer", "github.com/tieonlinux"
    yield "build-date", datetime.datetime.utcnow().isoformat()
    yield "name", "tshock"
    yield "description", "Tshock docker container by tieonlinux"
    yield "url", "https://github.com/tieonlinux/TShock-Docker"
    vcs_ref = os.environ.get("GITHUB_SHA") or os.environ.get("GITHUB_REF")
    if vcs_ref is None:
        try:
            vcs_ref = subprocess.check_output("git rev-parse --short HEAD", shell=True, text=True).strip()
        except:
            pass
    if vcs_ref:
        yield "vcs-ref", str(vcs_ref)


def gen_release_labels(release: dict):
    yield "tshock.release.url", release['html_url']
    yield "tshock.release.id", release['id']
    yield "tshock.release.tag", release['tag_name']
    yield "tshock.release.author", release['author']['login']
    yield "tshock.release.prerelease", 1 if release['prerelease'] else 0

    asset = get_release_asset(release)
    yield "tshock.asset.name", asset['name']
    yield "tshock.asset.url", asset['browser_download_url']


templateLoader = jinja2.FileSystemLoader(searchpath="templates")
jenv = jinja2.Environment(loader=templateLoader)
jenv.filters['quote'] = filter_quote

release = get_latest_release()
asset = get_release_asset(release)

labels = OrderedDict(gen_default_labels())
labels.update(gen_release_labels(release))

env = OrderedDict()
env['TSHOCK_URL'] = asset['browser_download_url']
env['TSHOCK_TAG'] = release['tag_name']


with open('release_info.json', 'w') as f:
    json.dump(release, f, indent=4)

files = ['start.sh', 'setup_tshock.sh', 'release_info.json', 'README.md']

for template_name in jenv.list_templates():
    template_path = Path(template_name)
    if template_path.suffix not in ('.jinja2', 'j2'):
        warnings.warn(f"found a non template file in template folder: {template_path}")
        continue
    template = jenv.get_template(template_name)
    output = template.render(labels=labels, env=env, files=files)
    with open(template_name[:-len(template_path.suffix)], 'w') as f:
        f.write(output)