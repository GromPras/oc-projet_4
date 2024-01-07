# Développez un programme logiciel en Python

## Français

### Introduction

Un programme écrit en Python pour créer et gérer des tournois d'échecs

### Installation

Pré-requis:

- Python >=3.6.0
- Git 2.X

```sh
git clone https://github.com/GromPras/oc-projet_4.git
```

`Ou téléchargez le fichier ZIP depuis https://github.com/GromPras/oc-projet_4/archive/refs/heads/main.zip`

Créez un environement virtuel à l'intérieur du dossier cloné:

```sh
cd oc-projet_4
python3 -m venv {/path/to/new/virtual/environment}
```

Sur Windows, appelez la commande venv comme suit :

```sh
c:\>c:\Python35\python -m venv c:\path\to\myenv
```

Activez l'environement virtuel :

```sh
source {/path/to/new/virtual/environment}/bin/activate
```

Sur Windows, appelez la commande venv comme suit :

```sh
C:\> <venv>\Scripts\activate.bat
```

Installez les packages requis :

```sh
pip install -r requirements.txt
```

Ou sur Windows :

```sh
py -m pip install -r requirements.txt
```

Si vous avez un problème avec la création de l'environnement consultez la documentation : `https://docs.python.org/fr/3/library/venv.html#creating-virtual-environments`

### Post Installation

Exécutez la commande suivante :

```sh
python3 src/main.py
```
