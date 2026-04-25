FROM pgvector/pgvector:pg16

COPY postgresql/docker-entrypoint-wrapper.sh /usr/local/bin/docker-entrypoint-wrapper.sh
COPY postgresql/01-enable-pgvector.sql /docker-entrypoint-initdb.d/01-enable-pgvector.sql

ENTRYPOINT ["/bin/sh", "/usr/local/bin/docker-entrypoint-wrapper.sh"]

EXPOSE 5432
