FROM debian:bullseye-slim
COPY start.sh setup_tshock.sh /

ENV TSHOCK_URL="https://github.com/Pryaxis/TShock/releases/download/v4.4.0-pre11/TShock4.4.0_Pre11_Terraria1.4.0.5.zip"

RUN /bin/sh -x /setup_tshock.sh
USER terraria

VOLUME ["/world", "/config", "/logs", "/plugins"]

WORKDIR /tshock

EXPOSE 7777

ENTRYPOINT ["/usr/bin/tini", "--", "/start.sh"]
