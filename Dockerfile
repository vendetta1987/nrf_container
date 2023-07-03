FROM python:3-slim-bullseye AS python3_buildessential
RUN apt update
RUN apt install -y build-essential cmake

FROM python3_buildessential

COPY Ahoy/requirements.txt .
RUN pip install -r requirements.txt

RUN apt remove -y build-essential cmake
RUN apt autoremove -y
RUN apt autoclean -y

COPY Ahoy/ahoy_rpi /ahoy

VOLUME /ahoy_work

WORKDIR /ahoy
CMD ["python", "-m", "hoymiles", "-c", "/ahoy_work/ahoy.yml" ]