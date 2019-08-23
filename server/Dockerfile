# Python version
FROM python:3.7
ENV C_FORCE_ROOT true
ENV PYTHONUNBUFFERED=1

WORKDIR /code/server

# Install gettext to compile tranlations
RUN apt-get update && apt-get install gettext -y htop telnet

# Install pipenv
# RUN pip install --upgrade pip && pip install pipenv

RUN python -m venv /opt/venv

# Copy pipfile and install it as a system packages
COPY ./requirements.txt /code/server/
RUN . /opt/venv/bin/activate

# No need in virtualenv as we are already inside container
RUN pip install -r requirements.txt

# Copy project files only here, because we don't want to reinstall
# requirements each time file is changed.
COPY ./ /code/server/
