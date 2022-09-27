FROM ubuntu
ENV HOME=/opt/app
WORKDIR $HOME
RUN apt-get update
ENV DEBIAN_FRONTEND=noninteractive
RUN apt-get install -y python3 python3-pip nginx gcc uwsgi-plugin-python3
COPY requirements.txt $HOME
RUN pip install -i https://mirrors.aliyun.com/pypi/simple -r requirements.txt

COPY . $HOME

ENV PYTHONUNBUFFERED=true

RUN rm -r /etc/nginx/conf.d \
 && cp -r nginx/gallery-back.conf /etc/nginx/sites-available/default

# RUN ln -sf /dev/stdout /var/log/nginx/access.log \
#  && ln -sf /dev/stderr /var/log/nginx/error.log

EXPOSE 80
CMD ["/bin/sh", "config/run.sh"]
