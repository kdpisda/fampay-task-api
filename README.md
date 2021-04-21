# Run fampay Task API

## Install Python

If you have not installed `python` already on your system, please follow [this link](https://www.python.org/downloads/) to install the same.

## Installing PostgreSQL

Please follow the steps mentioned [here](https://www.postgresql.org/download/) for your operating system to install `postgreSQL` in your system.

### Accesing `psql`

> If you are using linux as your driver OS you may follow the below steps. PostgreSQL usually create a user `postgres` who can access `psql`. So, we will try to access `psql` with user `postgres`.

```sh
sudo -su postgres psql
```

It will promt you to enter your root password. And after putting the right password you shall get access to `psql`.

### Creating Database

```sql
CREATE DATABASE fampay;
```

### Creating Database User

```sql
CREATE USER fampay WITH ENCRYPTED PASSWORD 'fampay';
```

### Granting the database user `fampay` access of the database `fampay`

```sql
GRANT ALL PRIVILEGES ON DATABASE fampay TO fampay;
```

> Press `\q` followed by `enter` to come out of terminal

## Installing Redis

You may follow [these steps](https://redis.io/download) to install redis on your system. After installing it successfully, start the `redis-server`.

## Setting up the environment and environment variables

### Creating virtual environment

```sh
python -m venv env
```

This will create a virtual enironment with the name `env` in the project root.

### Activating the virtual environment

```sh
source env/bin/activate
```

You might see `(env)` in your terminal which states that the virtual environment is active. For example:

```sh
(env) kdpisda @ kuldeep-vostro ~/Projects/fampay-task
```

### Installing the requirements

```sh
pip install -r requirements.txt
```

### Setting up the environment variables

If you changed anythig while we were preparing the database in `PostgreSQL` you might want to update the respective value in the `.env.temp` file. Rename the file to `.env`.

> Will now we have activated the virtual environment and have placed a `.env` file in the project root with the respective value. This step is required to run the server and the worker.

### Running the migrations

```sh
source .env && ./manage.py migrate
```

### Installing other requirements

Since we rely on [`pdfkit`](https://pypi.org/project/pdfkit/) to generate PDF files. Please follow the steps mentioned [here](https://pypi.org/project/pdfkit/) to install `wkhtmltopdf` as well which is necessary for smooth functioning of the app.

### Setting up admin username and password

```sh
source .env && ./manage.py createsuperuser
```

It will ask for `username`, `email`, `password` in a prompt, fill all the details and press enter. Make sure to enter email as well. So that we can login with the same credentials.

## Running Server

```sh
source .env && ./manage.py migrate
```

This will run the server in port `8000`

## Running Beat

In order to keep updating the database we need to run celery beat on another terminal.

```sh
source .env && celery -A fampay beat -l info
```

## Running Background Worker

Make sure you have activated the virtual environment. So in order for the better execution of the app we need to run the worker at the same time but in different terminal. So ideally, you would want to run the above command in one terminal, and the below command in the other terminal with virtual environment activated.

```sh
source .env && celery -A fampay worker -l info
```

## Running React APP

In order to run the app, you must also have your [`React App Client`](https://github.com/kdpisda/fampay-task-app) Clone the repository and follow the instructions specified in the `README.md` file in the [React App](https://github.com/kdpisda/fampay-task-app) repository. Use the credentials defined while creating the admin user for the Django API.

## Running it via `docker-compose`

Install `docker` following [this link](https://docs.docker.com/get-docker/). And `docker-compose` via [this link](https://docs.docker.com/compose/install/).
Make sure to rename `.env.temp` to `.env`.

```sh
bash build.sh
docker-compose up -d
```

> The server will be up in port `5000`. In order to enter `DEVELOPER_KEY` we need to create a admin user account on `django`.

### Inspect docker container running `api`

```sh
docker ps
```

It might list somthing like this.

```sh
CONTAINER ID   IMAGE             COMMAND                  CREATED       STATUS       PORTS                                       NAMES
9ced73a6a586   fampay/api:v0.1   "gunicorn -c gunicor…"   2 hours ago   Up 2 hours   0.0.0.0:5000->5000/tcp, :::5000->5000/tcp   api
de4c6bc34d23   fampay/api:v0.1   "celery -A fampay wo…"   2 hours ago   Up 2 hours   5000/tcp                                    worker
e56deefc7abf   fampay/api:v0.1   "celery -A fampay be…"   2 hours ago   Up 2 hours   5000/tcp                                    beat
2c669efca673   postgres          "docker-entrypoint.s…"   2 hours ago   Up 2 hours   5432/tcp                                    db
4e0a57eb3e17   redis:6.0.3       "docker-entrypoint.s…"   3 hours ago   Up 2 hours   6379/tcp                                    redis
```

Follow the container ID with the name `api`. In our case it is `9ced73a6a586`.
SSHing into the container

```sh
docker exec -it 9ced73a6a586 bash
```

We might see the SSH terminal like this.

```sh
root@9ced73a6a586:/api#
```

Now enter

```sh
./manage.py createadminuser
```

And continue the process to create admin user. Login into the admin panel and enter the `DEVELOPER_KEY`.
