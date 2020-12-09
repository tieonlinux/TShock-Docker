FROM debian:buster-slim


LABEL maintainer="github.com/tieonlinux" build-date="2020-12-09T11:32:16.258200" name="tshock" description="Tshock docker container by tieonlinux" url="https://github.com/tieonlinux/TShock-Docker" vcs-url="https://github.com/tieonlinux/TShock-Docker" vcs-ref="04ade446156bf98ffb5b7d81ae029bf69559db7b" tshock.release.url="https://github.com/Pryaxis/TShock/releases/tag/v4.4.0-pre15" tshock.release.id="33960138" tshock.release.tag="v4.4.0-pre15" tshock.release.author="QuiCM" tshock.release.prerelease="1" tshock.asset.name="TShock4.4.0_Pre15_Terraria1.4.1.2.zip" tshock.asset.url="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre15/TShock4.4.0_Pre15_Terraria1.4.1.2.zip" 

ENV TSHOCK_URL="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre15/TShock4.4.0_Pre15_Terraria1.4.1.2.zip" TSHOCK_TAG="v4.4.0-pre15" 


COPY "fs/*" "release_info.json" "README.md"   /

RUN /bin/sh -x /0.setup_system.sh

RUN /bin/sh -x /1.setup_tshock.sh

VOLUME ["/world", "/config", "/logs", "/plugins"]

WORKDIR /tshock

EXPOSE 7777

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/start.py"]