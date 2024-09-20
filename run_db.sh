sudo docker run -d \
--name mnist-mariadb \
--env MARIADB_USER=mnist \
--env MARIADB_PASSWORD=1234 \
--env MARIADB_DATABASE=mnistdb \
--env MARIADB_ROOT_PASSWORD=1234 \
-p 43306:3306 \
mariadb:latest
