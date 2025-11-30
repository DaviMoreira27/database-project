# database-project

## Configuring Pyenv

To run in dev mode this application, firstly you need to activate the virtual environment:

```bash
| Plataforma | Shell      | Comando para ativar o ambiente virtual              |
|-------------|------------|----------------------------------------------------|
| POSIX       | bash/zsh   | `$ source <venv>/bin/activate`                    |
| POSIX       | fish       | `$ source <venv>/bin/activate.fish`               |
| POSIX       | csh/tcsh   | `$ source <venv>/bin/activate.csh`                |
| POSIX       | pwsh       | `$ <venv>/bin/Activate.ps1`                       |
| Windows     | cmd.exe    | `C:\> <venv>\Scripts\activate.bat`                |
| Windows     | PowerShell | `PS C:\> <venv>\Scripts\Activate.ps1`             |
```

The `<venv>` notation refers to installation path of the virtual environment, for my case, when the current path is the project itself,
`/home/davisantana/projects/database-project/backend/.venv`, I can simply run the  following command:

```bash
source .venv/bin/activate
```
If the terminal informs you that it was not possible to find the path, maybe you need to initiate a virtual environment first. For this you can run:

```bash
python -m venv /caminho/para/novo/ambiente/virtual
```

For more info about pyenv you can check the official [documentation](https://docs.python.org/pt-br/3/library/venv.html).

## Installing the dependencies

Now you can install the dependencies using `pip package manager`

```bash
pip install -r require.txt
```

## Starting the database

Now for the database you can install postgres directly on your machine, or run it on a container

**If you are using linux:**

```bash
podman run -d \
  --name postgres-db \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=123456789 \
  -e POSTGRES_DB=db-project \
  -p 5432:5432 \
  docker.io/library/postgres:17
```

To test the connection you can run:

```bash
podman exec -it postgres-db psql -U testuser -d db-project
```

Note that this command will start a temporary container to run the database, after every restart the data will be lost. To persist between restarts, use this:

```bash
podman volume rm -f pgdata
podman volume create pgdata
podman run --replace -d \
  --name postgres-db \
  -e POSTGRES_USER=testuser \
  -e POSTGRES_PASSWORD=123456789 \
  -e POSTGRES_DB=db-project \
  -v pgdata:/var/lib/postgresql/data \
  -p 5432:5432 \
  docker.io/library/postgres:17
```

**if you are using Windows** first you will need to install Docker Desktop on your computer, for more details just read the (documentation)[https://docs.docker.com/desktop/setup/install/windows-install/]

To access the database you can run:

```bash 
podman exec -it postgres-db psql -U testuser -d db-project
```

To create the schema and insert the data, you can run:
```bash
podman exec -i postgres-db psql -U testuser -d db-project < schema.sql
podman exec -i postgres-db psql -U testuser -d db-project < data-creation.sql
```

## Create the .env

You will need a .env at the root of this project. The only variable we will use is:

```bash
DB_STRING="postgresql://testuser:123456789@localhost/db-project"
```

## Running the application

```bash
fastapi dev main.py
```
