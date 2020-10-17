FROM debian:buster-slim


LABEL maintainer="github.com/tieonlinux" build-date="2020-10-17T02:33:10.466274" name="tshock" description="Tshock docker container by tieonlinux" url="https://github.com/tieonlinux/TShock-Docker" vcs-url="https://github.com/tieonlinux/TShock-Docker" vcs-ref="a0d41d20e024d3828b5f8f509c492a9eb92ebf81" tshock.release.url="https://github.com/Pryaxis/TShock/releases/tag/v4.4.0-pre13" tshock.release.id="32606704" tshock.release.tag="v4.4.0-pre13" tshock.release.author="QuiCM" tshock.release.prerelease="1" tshock.asset.name="TShock4.4.0_Pre13_Terraria1.4.1.1.zip" tshock.asset.url="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre13/TShock4.4.0_Pre13_Terraria1.4.1.1.zip" 

ENV TSHOCK_URL="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre13/TShock4.4.0_Pre13_Terraria1.4.1.1.zip" TSHOCK_TAG="v4.4.0-pre13" 


COPY "fs/*" "release_info.json" "README.md"   /

RUN /bin/sh -x /0.setup_system.sh

RUN /bin/sh -x /1.setup_tshock.sh

VOLUME ["/world", "/config", "/logs", "/plugins"]

WORKDIR /tshock

EXPOSE 7777

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/start.py"]