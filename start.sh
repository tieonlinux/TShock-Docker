#!/bin/bash
# tshock startup script

# warning: this script is run as root
set -e

# set user/group id
PUID=${PUID:-1001}
PGID=${PGID:-1001}
usermod -u "$PUID" terraria
groupmod -g "$PGID" terraria

DEFAULT_MONO_FLAGS=("--gc=sgen" "-O=all")

# fix perms
if [ -z "${NO_CHOWN}" ]; then
    for dir in "/config" "/world" "/logs" "/plugins" "/tshock"
    do
        if [ ! "$(stat -c %u $dir)" = "$PUID" ]; then
            echo "chown terraria $dir/* ..."
            chown -R terraria $dir
        fi
    done
fi

# copy plugins
cp --archive -f /tshock/ServerPlugins/TShockAPI.dll /tshock/TShockAPI.dll &&
rsync -a --delete --exclude='*TShockAPI.dll*' --exclude=".*" /plugins/ /tshock/ServerPlugins ;
mv -f /tshock/TShockAPI.dll /tshock/ServerPlugins/TShockAPI.dll

# handle default flags
flags="${MONO_FLAGS[@]}"
if [ -z "$flags" ]; then
    flags="--desktop"
    if [ $(grep MemTotal /proc/meminfo | awk '{print $2}') -gt 2000000 ]; then
        flags="--server"
    fi
    flags=("${flags}" "${DEFAULT_MONO_FLAGS[@]}")
fi

# change user and group then execute mono command
exec gosu terraria:terraria mono "${flags[@]}" TerrariaServer.exe -configpath /config -worldpath /world -logpath /logs "$@"