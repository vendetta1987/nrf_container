#FROM python:3-slim-bullseye AS base
#RUN apt update
#RUN apt install -y build-essential cmake
#
#FROM base
FROM python3_buildessential

COPY requirements.txt .
RUN pip install -r requirements.txt

RUN apt remove -y build-essential cmake
RUN apt autoremove -y

COPY ahoy_rpi /ahoy

VOLUME /ahoy_work

WORKDIR /ahoy
CMD ["python", "-m", "hoymiles", "-c", "/ahoy_work/ahoy.yml" ]