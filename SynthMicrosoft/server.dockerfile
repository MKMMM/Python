FROM ubuntu:23.04
RUN apt update
RUN apt install -y python3
RUN apt install -y pip
RUN apt install -y python3-requests
RUN apt install -y python3-pandas
RUN apt install -y python3-tk
RUN apt install -y python3-django
RUN apt install -y git curl python3-pip
RUN apt install -y neofetch
COPY *.py /app/

