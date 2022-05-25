FROM python:3.10.4-slim

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN groupadd --gid $USER_GID $USERNAME \
    && useradd -g $USERNAME $USERNAME 

WORKDIR /app

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN python -m pip install --upgrade pip
COPY --chown=$USERNAME:$USERNAME ./requirements.txt .
RUN python -m pip install -r requirements.txt

# copy project
COPY --chown=$USERNAME:$USERNAME . .

RUN python manage.py collectstatic --noinput && \
    python manage.py migrate 

RUN chown -R $USERNAME:$USERNAME /app

USER $USERNAME