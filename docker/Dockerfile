###################################################
# Dockerfile to run a Django-based web application
# Based on Debian Bookworm Linux Image
###################################################
FROM python:3.11-slim-bookworm
MAINTAINER Bailey Solution

# Configure Timezone
ENV TIMEZONE "Europe/Vienna"
# set enviroments
ENV PRJPATH=/web
ENV DJANGO_ENV=production


RUN apt-get update && apt-get install -y --no-install-recommends libxml2-dev libxslt1-dev zlib1g-dev tzdata gcc g++ \
    default-libmysqlclient-dev libxml2-utils libpq-dev mime-support bzip2 file libmagic-mgc libmagic1 xz-utils \
    gettext && \
    rm -rf /var/lib/apt/lists/*

RUN ln -snf /usr/share/zoneinfo/$TIMEZONE /etc/localtime && \
    echo $TIMEZONE > /etc/timezone

#create user django
RUN useradd -M -d $PRJPATH -s /bin/bash django
#change workdir
WORKDIR $PRJPATH
# copy and install python requirements
COPY requirements.txt $PRJPATH/
RUN pip3 install -U pip && \
    pip3 install --no-cache-dir -r requirements.txt
# copy project related files
COPY app warehouse templates $PRJPATH/
COPY manage.py asgi.py LICENSE wsgi.py docker/uwsgi.ini docker/entrypoint.sh $PRJPATH/

# set permissions on files
RUN chmod a+x manage.py wsgi.py uwsgi.ini entrypoint.sh asgi.py && chown -R django:django $PRJPATH
# create volume for media files
VOLUME ["$PRJPATH/templates/media/"]

EXPOSE 8001

ENTRYPOINT ["./entrypoint.sh"]
