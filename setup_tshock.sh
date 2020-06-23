# install new packages
apt-get update &&
apt-get install -y --no-install-recommends wget unzip rsync dumb-init sudo bash ca-certificates nuget python3 &&
# update mono cert store
timeout 120 cert-sync /etc/ssl/certs/ca-certificates.crt || :

# setup tshock
if [ -z "${TSHOCK_URL}" ]; then
    echo "Missing TSHOCK_URL env variable !"
    exit 1
fi
mkdir -p "/config" "/world" "/logs" "/plugins" "/tshock" &&
cd /tshock &&
echo "downloading tshock" &&
wget "$TSHOCK_URL" -O tshock.zip --tries=5 &&
unzip tshock.zip &&
rm tshock.zip &&
chmod +x /tshock/TerrariaServer.exe &&
chmod +x /start.py || exit $?

# install gosu
dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"
wget --tries=5 -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-$dpkgArch" &&
chmod +x /usr/local/bin/gosu || exit $?

# cleanup
rm -rf /var/lib/apt/lists/*
rm -rf /var/cache/debconf/templates.dat*
rm -rf /var/lib/dpkg/status-old
echo '' > /var/log/lastlog
echo '' > /var/log/dpkg.log
echo '' > /var/log/apt/term.log
echo '' >  /var/log/faillog

# terraria user & group
addgroup --system --gid 1001 terraria &&
adduser --system --uid 1001 --ingroup terraria --shell /bin/bash terraria &&
chown -R terraria:terraria "/config" "/world" "/logs" "/plugins" "/tshock"

exit $?