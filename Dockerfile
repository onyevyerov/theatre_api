FROM python:3.11-alpine3.21
LABEL maintainer="onyevyerov@gmail.com"

ENV PYTHONUNBUFFERED 1

WORKDIR app/

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

# create directory for media files
RUN mkdir -p /files/media

RUN adduser \
    --disabled-password \
    --no-create-home \
    my_user

# make my_user owner of media directory
RUN chown -R my_user /files/media
# give right for owner to Write/Read/Exec and for else Read/Exec
RUN chmod -R 755 /files/media

USER my_user