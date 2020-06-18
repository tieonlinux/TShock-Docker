#!/bin/sh
# tshock startup script
set -e
#copy plugins
[ "$(ls -A /plugins)" ] && rsync -a --delete /plugins/ /tshock/ServerPlugins
exec mono --desktop --gc=sgen -O=all TerrariaServer.exe -configpath /config -worldpath /world -logpath /logs "$@"