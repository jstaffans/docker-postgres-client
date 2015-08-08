docker-postgres-client
======================
I created this library to work with different version of Docker Postgres without having the need to change my Postgres client.

.. warning::
   If you have a the official Postgres client installed on your machine, you will get some name conflict in your bash commands. I have uninstalled my official Postgres client since all my Postgres servers are running in a Docker container.

To install and use it type the command below:

.. code-block:: bash

    pip install docker-Postgres-client

You will then have four new commands available in your shell: psql, createdb, dropdb, and pg_dump. They allow you to connect, create, drop, dump, and import a database. If you want to add additional features feel free to fork this repository and make a merge request.

All the bash command have -C (container) option  that you can use like below:

.. code-block:: bash

    psql -C CONTAINER_NAME -U user_name

Last but not least all the scripts contain a useful help message to know how to use them.

.. code-block:: bash

    psql --help