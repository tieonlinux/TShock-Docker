# 🚢[TShock-Docker](https://github.com/tieonlinux/TShock-Docker)

a [Docker image](https://hub.docker.com/repository/docker/tieonlinux/terraria) for [TShock a terraria server](https://github.com/Pryaxis/TShock)


[![](https://images.microbadger.com/badges/image/tieonlinux/terraria.svg)](https://microbadger.com/images/tieonlinux/terraria)  [![](https://images.microbadger.com/badges/version/tieonlinux/terraria.svg)](https://microbadger.com/images/tieonlinux/terraria)  [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/tieonlinux/TShock-Docker/blob/main/LICENSE)  
![CI Docker Image](https://github.com/tieonlinux/TShock-Docker/workflows/Update%20Docker.io%20Image/badge.svg)


# Key Features

- Use [github actions](https://github.com/tieonlinux/TShock-Docker/actions) in order to automatically build/test/publish [latest TShock release](https://github.com/Pryaxis/TShock/releases) into docker images
- Multi arch: `x64` and `arm` support
- Smart world choosing process

# About TShock
<p align="center">
  <img src="https://tshock.co/newlogo.png" alt="TShock for Terraria"><br />
  <a href="https://ci.appveyor.com/project/hakusaro/tshock">
    <img src="https://ci.appveyor.com/api/projects/status/chhe61q227lqdlg1?svg=true" alt="AppVeyor Build Status">
  </a>
  <a href="https://github.com/Pryaxis/TShock/actions">
    <img src="https://github.com/Pryaxis/TShock/workflows/Build%20Server/badge.svg" alt="GitHub Actions Build Status">
  </a>
  <a href="#contributors">
    <img src="https://img.shields.io/github/contributors/Pryaxis/TShock.svg" alt="All contributors">
  </a>
  <br/><br/>
  <a href="https://github.com/Pryaxis/TShock/blob/general-devel/README_cn.md">查看中文版</a>
</p>

TShock is a toolbox for Terraria servers and communities. That toolbox is jam packed with anti-cheat tools, server-side characters, groups, permissions, item bans, tons of commands, and limitless potential. It's one of a kind.

* Download: [official](https://github.com/TShock/TShock/releases) or [experimental](https://github.com/TShock/TShock#experimental-downloads).
* Download: [plugins and tools](https://github.com/Pryaxis/plugins) that work with TShock, TSAPI, and Terraria.
* Read [the documentation](https://tshock.readme.io/) to quickly get up to speed.
* Join [Discord](https://discord.gg/Cav9nYX).
* Use the ancient [old forums](https://tshock.co/xf/index.php?resources/) to find old stuff.
* Talk on [GitHub discussions](https://github.com/Pryaxis/TShock/discussions) to ask for help, chat, and other things. This is the best way to get help if Discord isn't your thing.
* For news, follow [@Pryaxis](https://twitter.com/Pryaxis) on Twitter.

# 🎡 Supported Architectures 🎡
Built images support multiple architectures such as *x86-64*, *arm64* and *armhf*.

Pulling [tieonlinux/terraria:latest](https://hub.docker.com/repository/docker/tieonlinux/terraria) retrieve the image matching your architecture.  
You can also pull arch images via specific tags.

The architectures supported are the following:
| Architecture | Tag |
|:-- | :-- |
| x86-64 | amd64-latest |
| 386 | 386-latest |
| arm64 | arm64v8-latest |
| armhf | arm32v7-latest |
| ▲ *Any of those* ▲  | ★ **latest** ★ |

# 🎮 Usage

## 🚢 Docker
A standard docker knowledge is required to set this up

```
docker create \
  --name=terraria \
  -e PUID=1001 \
  -e PGID=1001 \
  -v /path/to/tshock/config:/config \
  -v /path/to/tshock/logs:/logs \
  -v /path/to/tshock/world:/world \
  -v /path/to/tshock/plugins:/plugins \
  --name="terraria" \
  tieonlinux/terraria \
  -world "a world_name.wld"
```

## Parameters
| Parameter | Description |
| :-- | :--
| -e PUID=1001 | for UserID - [see below for explanation](#usergroupidentifiers) |
| -e PGID=1001 | for GroupID - [see below for explanation](#usergroupidentifiers) |
| -v /path/to/tshock/config:/config | TShock's config location. Allow persistance of databases and json config |
| -v /path/to/tshock/logs:/logs | TShock's log files location |
| -v /path/to/tshock/world:/world | Terraria's world(s) location (containing .wld files) |
| -v /path/to/tshock/plugins:/plugins | TShock's plugins location |
| -world "a world_name.wld"  | The file name or absolute path to the world to load |

Note that those parameters are all *optional*. But it's **strongly recommended to use them all**.


## <a name="usergroupidentifiers">User / Group Identifiers</a>

When using volumes (`-v` flags) permissions issues can arise between the host OS and the container, we avoid this issue by allowing you to specify the user `PUID` and group `PGID`.

Ensure any volume directories on the host are owned by the same user you specify and any permissions issues will vanish like magic.

In this instance `PUID=1001` and `PGID=1001`, to find yours use `id user` as below:

```
  $ id username
    uid=1001(terrariauser) gid=1001(terrariagroup) groups=1001(terrariagroup)
```

# Special Thanks
- [TShock devs](https://github.com/Pryaxis/TShock) 
- [LinuxServer](https://www.linuxserver.io/) for inspiration on docker images features / readme  

# Build info
**Build context from the [gen branch](https://github.com/tieonlinux/TShock-Docker/tree/gen)**

## labels
| Key | Value |
| :-- | --:|
| maintainer | github.com/tieonlinux |
| build-date | 2020-06-26T12:10:17.941441 |
| name | tshock |
| description | Tshock docker container by tieonlinux |
| url | https://github.com/tieonlinux/TShock-Docker |
| vcs-url | https://github.com/tieonlinux/TShock-Docker |
| vcs-ref | aa95ee2c76acc5da63dbf767b2a8f28f0b46575c |
| tshock.release.url | https://github.com/Pryaxis/TShock/releases/tag/v4.4.0-pre11 |
| tshock.release.id | 27248651 |
| tshock.release.tag | v4.4.0-pre11 |
| tshock.release.author | hakusaro |
| tshock.release.prerelease | 1 |
| tshock.asset.name | TShock4.4.0_Pre11_Terraria1.4.0.5.zip |
| tshock.asset.url | https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre11/TShock4.4.0_Pre11_Terraria1.4.0.5.zip |


## env
| Key | Value |
| :-- | --:|
| TSHOCK_URL | https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre11/TShock4.4.0_Pre11_Terraria1.4.0.5.zip |
| TSHOCK_TAG | v4.4.0-pre11 |



## files
| Key |
| :-- |
| start.py |
| setup_tshock.sh |
| release_info.json |
| README.md |
