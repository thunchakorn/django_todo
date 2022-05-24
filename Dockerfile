FROM python:3.10.4-alpine

ARG USERNAME=user
ARG USER_UID=1000
ARG USER_GID=$USER_UID

RUN addgroup --gid $USER_GID $USERNAME \
    && adduser -u $USER_UID -G $USERNAME -S $USERNAME 

USER $USERNAME
WORKDIR /app

# Prevents Python from writing pyc files to disc (equivalent to python -B option)
ENV PYTHONDONTWRITEBYTECODE 1
# Prevents Python from buffering stdout and stderr (equivalent to python -u option)
ENV PYTHONUNBUFFERED 1

# install dependencies
RUN pip install --upgrade pip
COPY --chown=$USERNAME:$USERNAME ./requirements.txt .
RUN pip install -r requirements.txt

# copy project
COPY --chown=$USERNAME:$USERNAME . .

RUN python manage.py collectstatic && \
    python manage.py migrate
    