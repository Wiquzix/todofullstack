FROM redis:alpine

COPY redis.conf /usr/local/etc/redis/redis.conf
COPY init.sh /usr/local/bin/init.sh

RUN chmod +x /usr/local/bin/init.sh

CMD ["/usr/local/bin/init.sh"]
