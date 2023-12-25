FROM python:3.10
FROM sagemath/sagemath:latest

# USER root
RUN sudo apt-get update && sudo apt-get install socat -y && sudo apt-get install python3-pip -y
RUN sage --pip install pycryptodome

COPY server.sage .
COPY input.pdf .
VOLUME ["/output"]

EXPOSE 6002
ENTRYPOINT ["socat", "TCP-LISTEN:6002,fork,reuseaddr", "EXEC:'sage server.sage',stderr"]<