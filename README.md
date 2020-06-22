# 🚢[TShock-Docker](https://github.com/tieonlinux/TShock-Docker)

a [Docker image](https://hub.docker.com/repository/docker/tieonlinux/terraria) for [TShock a terraria server](https://github.com/Pryaxis/TShock)

[![](https://images.microbadger.com/badges/image/tieonlinux/terraria.svg)](https://microbadger.com/images/tieonlinux/terraria)  [![](https://images.microbadger.com/badges/version/tieonlinux/terraria.svg)](https://microbadger.com/images/tieonlinux/terraria)  [![GPLv3 license](https://img.shields.io/badge/License-GPLv3-blue.svg)](https://github.com/tieonlinux/TShock-Docker/blob/main/LICENSE)  
![CI Docker Image](https://github.com/tieonlinux/TShock-Docker/workflows/Update%20Docker.io%20Image/badge.svg)

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
| -- | -- |
| x86-64 | amd64-latest |
| 386 | 386-latest |
| arm64 | arm64v8-latest |
| armhf | arm32v7-latest |
| ▲ *Any of those* ▲  | ★ **latest** ★ |

# 🎮 Usage

## 🚢 Docker
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