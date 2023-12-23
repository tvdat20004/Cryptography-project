FROM python:3.10

RUN apt-get update && apt-get install socat -y
RUN pip install pycryptodome

COPY elliptic_curve.py .
COPY server.py .
COPY input3.pdf .
VOLUME ["/output"]


EXPOSE 2030
ENTRYPOINT ["socat", "TCP-LISTEN:2030,fork,reuseaddr", "EXEC:'python server.py',stderr"]
