FROM debian:buster-slim


LABEL maintainer="github.com/tieonlinux" build-date="2020-06-27T11:54:38.659288" name="tshock" description="Tshock docker container by tieonlinux" url="https://github.com/tieonlinux/TShock-Docker" vcs-url="https://github.com/tieonlinux/TShock-Docker" vcs-ref="7287efa414551004278266386c03578c50783d88" tshock.release.url="https://github.com/Pryaxis/TShock/releases/tag/v4.4.0-pre12" tshock.release.id="27983039" tshock.release.tag="v4.4.0-pre12" tshock.release.author="hakusaro" tshock.release.prerelease="1" tshock.asset.name="TShock4.4.0_Pre12_Terraria1.4.0.5.zip" tshock.asset.url="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre12/TShock4.4.0_Pre12_Terraria1.4.0.5.zip" 

ENV TSHOCK_URL="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre12/TShock4.4.0_Pre12_Terraria1.4.0.5.zip" TSHOCK_TAG="v4.4.0-pre12" 


COPY "fs/*" "release_info.json" "README.md"   /


RUN /bin/sh -x /0.setup_system.sh

RUN /bin/sh -x /1.setup_tshock.sh

VOLUME ["/world", "/config", "/logs", "/plugins"]

WORKDIR /tshock

EXPOSE 7777

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/start.py"]