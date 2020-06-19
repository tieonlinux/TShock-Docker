# install new packages
apt-get update &&
apt-get install -y --no-install-recommends rsync dumb-init wget unzip sudo bash util-linux && 
apt-get install -y --no-install-recommends build-essential ca-certificates llvm &&
# update mono cert store
timeout 120 cert-sync /etc/ssl/certs/ca-certificates.crt || :

# setup tshock
if [ -z "${TSHOCK_URL}" ]; then
    echo "Missing TSHOCK_URL env variable !"
    exit 1
fi
mkdir /world /config /logs /plugins /tshock &&
cd /tshock &&
echo "downloading tshock" &&
wget "$TSHOCK_URL" -O tshock.zip --tries=5 &&
unzip tshock.zip &&
rm tshock.zip &&
chmod +x /tshock/TerrariaServer.exe &&
chmod +x /start.sh || exit $?

# precompile TerrariaServer
if [ -z "${MONO_NO_AOT}" ]; then
    timeout 120 mono --aot -O=all TerrariaServer.exe
    if [ $? -ne 124 -a $? -ne 0 ]; then
        exit $?
    fi

    # note that mono aot OTAPI.dll crash
fi

# download gosu
dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"
wget --tries=5 -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-$dpkgArch" &&
chmod +x /usr/local/bin/gosu || exit $?

# cleanup apt
apt-mark hold mono-csharp-shell msbuild mono-mcs libmono-2.0-dev libmonosgen-2.0-dev libmonosgen-2.0-1
apt-get remove -y --purge build-essential llvm
apt-get autoremove -y --purge build-essential llvm && apt-get clean
rm -rf /var/lib/apt/lists/*

# terraria user & group
addgroup --system --gid 1001 terraria && adduser --system --uid 1001 --ingroup terraria --shell /bin/bash terraria &&
chown -R terraria:terraria /world /config /logs /plugins /tshock &&
exit $?