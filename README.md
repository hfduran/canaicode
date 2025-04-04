# CAN (A)I CODE?
![Kurisu](https://i.pinimg.com/564x/85/63/a7/8563a71c903571dcf7f98ce36226e848.jpg)

## Requirements
- python 3.13.2 ([pyenv](https://github.com/pyenv/pyenv) reccomended)
- [pipenv](https://pipenv.pypa.io/en/latest/)
- [mypy](https://mypy.readthedocs.io/en/stable/getting_started.html)

## Intro

The project uses the following tools:
- `pipenv`: kind of a package manager (actually a wrapper for pip)
- `ruff`: linter
- `mypy`: static analyser
- `pyright` (or pylance in vscode): language server

All extensions for that tools are included on the `.vscode` folder on this repo. Opening the project should popup the suggestions. It might be necessary to install some tools on your system (specially mypy) for the extensions to work properly.

## Running


```bash
pipenv install
pipenv run main
```

For now the program has two functionalities:

1. summarize the LOC of a repo

2. consume gh_copilot api (for now you need to put a json file of the response on sensible_data)

You may want to config the system with .env, with the variables contained on config.py

## Developing

I strongly suggest setting up Pyright/Pylance (with strict rules), MyPy and Ruff on your IDE and assure it is working properly.

Ensure that the python environment you are using is the Pipenv one. In vscode:

Ctrl+Shift+P > "Python: Select Interpreter" > (search for your project pipenv)


### IMPORTANT:
Please, whenever submiting a PR run the static check and correct **ALL** errors.
```bash
mypy
```

## Installing new dependencies

Please use `pipenv` to install new dependencies. It will update the Pipenv lockfiles
```bash
pipenv install <your dependency>
```
