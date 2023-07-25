FROM python:3-slim-bullseye AS python3_buildessential
RUN apt update
RUN apt install -y build-essential cmake

#Ahoy
FROM python3_buildessential

WORKDIR /

COPY Ahoy/requirements.txt .
RUN pip install -r requirements.txt

COPY Ahoy/ahoy_rpi /ahoy
VOLUME /ahoy_work

RUN apt remove -y build-essential cmake
RUN apt autoremove -y
RUN apt autoclean -y

#Weatherstation
COPY Weatherstation/requirements.txt .
RUN pip install -r requirements.txt
RUN rm requirements.txt

COPY Weatherstation /weatherstation

###
WORKDIR /
COPY docker_entrypoint.py entrypoint.py
CMD ["python", "-u", "entrypoint.py"]