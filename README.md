# docker-postgres-client
I created these scripts to work with different version of docker postgres without having the need to change my postgres client. This small python scripts are all standalone and will use the psql client inside your docker machine.

To connect to your docker postgres image you can use the following command:

psql -C CONTAINER_NAME -U user_name

All the scripts contain a usefull help message to know how to use them. I usually put those scripts in /usr/local/bin/ but you can use them from everywhere (i removed the official postgres client from all my clients and servers).