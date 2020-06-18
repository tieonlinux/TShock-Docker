apt-get update &&
apt-get install -y --no-install-recommends mono-complete rsync tini wget unzip && 
apt-get install -y --no-install-recommends build-essential ca-certificates llvm &&
timeout 120 cert-sync /etc/ssl/certs/ca-certificates.crt
if [ $? -ne 124 -a $? -ne 0 ]; then
    exit $?
fi
if [[ -z "${TSHOCK_URL}" ]]; then
    exit 1
fi
mkdir /world /config /logs /plugins /tshock &&
cd /tshock &&
echo "downloading tshock" &&
wget "$TSHOCK_URL" -O tshock.zip --no-check-certificate --tries=5 &&
unzip tshock.zip &&
rm tshock.zip &&
chmod +x /tshock/TerrariaServer.exe &&
cp --archive /start.sh /start &&
chmod +x /start || exit $?
if [[ -z "${MONO_NO_AOT}" ]]; then
    timeout 120 mono --aot -O=all TerrariaServer.exe
    if [ $? -ne 124 -a $? -ne 0 ]; then
        exit $?
    fi
fi
apt-get autoremove -y --purge build-essential ca-certificates llvm &&
rm -rf /var/lib/apt/lists/*
addgroup --gid 1001 --system terraria && adduser --system --uid 1001 --ingroup terraria terraria &&
chown -R terraria:terraria /world /config /logs /plugins /tshock
exit $?
