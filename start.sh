#!/bin/bash
# tshock startup script

# warning: this script is run as root
set -e

# set user/group id
PUID=${PUID:-1001}
PGID=${PGID:-1001}
usermod -u "$PUID" terraria
groupmod -g "$PGID" terraria

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
cp --archive -f /tshock/ServerPlugins/TShockAPI.dll /tmp/TShockAPI.dll &&
rsync -a --delete --exclude='*TShockAPI.dll*' --exclude=".*" /plugins/ /tshock/ServerPlugins
mv -f /tmp/TShockAPI.dll /tshock/ServerPlugins/TShockAPI.dll

# handle default flags
flag="--desktop"
if [ $(grep MemTotal /proc/meminfo | awk '{print $2}') -gt 2000000 ]; then
    flags="--server"
fi

# change user and group then execute mono command
exec gosu terraria:terraria mono TerrariaServer.exe --gc=sgen -O=all "${flag}" -configpath /config -logpath /logs -worldpath /world "$@"