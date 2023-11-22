# Use the official MySQL image
FROM mysql:8.0.30

# Set environment variables
ENV MYSQL_DATABASE=jungo
ENV MYSQL_ROOT_PASSWORD=my-secret-pw

# Add the dump file to the container
COPY jungo_dump.sql /docker-entrypoint-initdb.d/jungo_dump.sql

# The default entrypoint will import the dump at startup
