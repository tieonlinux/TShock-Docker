FROM mono:slim


LABEL maintainer="github.com/tieonlinux" build-date="2020-06-23T15:35:06.313069" name="tshock" description="Tshock docker container by tieonlinux" url="https://github.com/tieonlinux/TShock-Docker" vcs-url="https://github.com/tieonlinux/TShock-Docker" vcs-ref="41e3cc68c5368ae37b1adce06c25c0405e9ba8ca" tshock.release.url="https://github.com/Pryaxis/TShock/releases/tag/v4.4.0-pre11" tshock.release.id="27248651" tshock.release.tag="v4.4.0-pre11" tshock.release.author="hakusaro" tshock.release.prerelease="1" tshock.asset.name="TShock4.4.0_Pre11_Terraria1.4.0.5.zip" tshock.asset.url="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre11/TShock4.4.0_Pre11_Terraria1.4.0.5.zip" 

ENV TSHOCK_URL="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre11/TShock4.4.0_Pre11_Terraria1.4.0.5.zip" TSHOCK_TAG="v4.4.0-pre11" 


COPY "start.py" "setup_tshock.sh" "release_info.json" "README.md"   /


RUN /bin/sh -x /setup_tshock.sh

VOLUME ["/world", "/config", "/logs", "/plugins"]

WORKDIR /tshock

EXPOSE 7777

ENTRYPOINT ["/usr/bin/dumb-init", "--", "/start.py"]