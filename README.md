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
`/home/davisantana/projects/database-project`, I can simply run the  following command:

```bash
source ./bin/activate
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
