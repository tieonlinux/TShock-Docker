# install mono (https://www.mono-project.com/download/stable/#download-lin-debian)
apt-get update &&
apt install -y --no-install-recommends apt-transport-https dirmngr gnupg ca-certificates &&
apt-key adv --keyserver hkp://keyserver.ubuntu.com:80 --recv-keys 3FA7E0328081BFF6A14DA29AA6A19B38D3D831EF &&
echo "deb https://download.mono-project.com/repo/debian stable-stretch main" | tee /etc/apt/sources.list.d/mono-official-stable.list &&
apt update &&
apt install -y --no-install-recommends mono-devel ||
exit $?


# install new packages
apt-get install -y --no-install-recommends wget unzip rsync dumb-init sudo bash ca-certificates nuget python3 &&
# update mono cert store
timeout 120 cert-sync /etc/ssl/certs/ca-certificates.crt || :

# install gosu
dpkgArch="$(dpkg --print-architecture | awk -F- '{ print $NF }')"
wget --tries=5 -O /usr/local/bin/gosu "https://github.com/tianon/gosu/releases/download/1.12/gosu-$dpkgArch" &&
chmod +x /usr/local/bin/gosu || exit $?

# cleanup
apt purge -y gnupg && 
apt autoremove -y && 
apt clean

rm -rf /tmp/* /var/tmp/* /var/lib/apt/lists/*
rm -f /var/cache/debconf/templates.dat* /var/lib/dpkg/status-old

echo '' > /var/log/lastlog
echo '' > /var/log/dpkg.log
echo '' > /var/log/apt/term.log
echo '' >  /var/log/faillog
echo '' > /var/log/apt/history.log
echo '' > /var/log/alternatives.log

# terraria user & group
addgroup --system --gid 1001 terraria &&
adduser --system --uid 1001 --ingroup terraria --shell /bin/bash terraria ||

exit $?