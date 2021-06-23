# Dockerfile for Tilavarauspalvelu backend

FROM registry.access.redhat.com/ubi8/python-38 as appbase

USER root

RUN rm /etc/rhsm-host

ARG LOCAL_REDHAT_USERNAME
ARG LOCAL_REDHAT_PASSWORD
ARG BUILD_MODE


WORKDIR /tvp

RUN useradd -N -M --system -s /bin/bash celery && echo celery:"B1llyB0n3s" | /usr/sbin/chpasswd
# celery perms
RUN groupadd grp_celery && usermod -a -G grp_celery celery && mkdir -p /var/run/celery/ /var/log/celery/
RUN chown -R celery:grp_celery /var/run/celery/ /var/log/celery/
# copy celery daemon files
ADD init_celeryd /etc/init.d/celeryd
RUN chmod +x /etc/init.d/celeryd

# copy celery config
ADD celery_config /etc/default/celeryd
RUN chmod 640 /etc/default/celeryd

RUN if [ "x$BUILD_MODE" = "xlocal" ] ;\
    then \
        subscription-manager register --username $LOCAL_REDHAT_USERNAME --password $LOCAL_REDHAT_PASSWORD --auto-attach; \
    else \
        subscription-manager register --username ${REDHAT_USERNAME} --password ${REDHAT_PASSWORD} --auto-attach; \
    fi

RUN subscription-manager repos --enable codeready-builder-for-rhel-8-x86_64-rpms
RUN yum -y update

RUN rpm -Uvh https://download.fedoraproject.org/pub/epel/epel-release-latest-8.noarch.rpm

RUN yum install -y gdal


RUN useradd -ms /bin/bash -d /tvp tvp
# Statics are kept inside container image for serving using whitenoise
RUN mkdir -p /srv/static && chown tvp /srv/static && chown tvp /opt/app-root/bin

RUN chown tvp /opt/app-root/lib/python3.8/site-packages
RUN chown tvp /opt/app-root/lib/python3.8/site-packages/*
RUN pip install --upgrade pip


WORKDIR /tvp


ENV APP_NAME tilavarauspalvelu



COPY deploy/* ./deploy/

RUN subscription-manager remove --all

RUN npm install @sentry/cli

# Can be used to inquire about running app
# eg. by running `echo $APP_NAME`

# Served by whitenoise middleware
ENV STATIC_ROOT /srv/static

ENV PYTHONUNBUFFERED True

ENV PYTHONUSERBASE /pythonbase

# Copy and install requirements files to image
COPY requirements.txt ./

RUN pip install --no-cache-dir uwsgi
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV DEBUG=True

RUN python manage.py collectstatic --noinput

RUN chgrp -R 0 /tvp
RUN chmod g=u -R /tvp

ENTRYPOINT ["/tvp/deploy/entrypoint.sh"]

EXPOSE 8000

# Next, the development & testing extras
FROM appbase as development

ENV DEBUG=True

#production
FROM appbase as production

ENV DEBUG=False
