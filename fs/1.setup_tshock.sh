# create tshock realted directories
mkdir -p "/config" "/world" "/logs" "/plugins" "/tshock" &&
chown -R terraria:terraria "/config" "/world" "/logs" "/plugins" "/tshock" &&
chmod +x /start.py

if [ -z "${TSHOCK_URL}" ]; then
    echo "Missing TSHOCK_URL env variable !"
    exit 1
fi
cd /tshock &&
echo "downloading tshock" &&
wget "$TSHOCK_URL" -O tshock.zip --tries=5 &&
unzip tshock.zip &&
rm tshock.zip || exit $?

mv TShock*/* . || :

chown -R terraria:terraria "/tshock" &&
chmod +x /tshock/TerrariaServer.exe ||
exit $?