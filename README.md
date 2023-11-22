# Introduction 
API du projet ACCIA.

# Getting Started
TODO: Guide d'installation
##1.	Créer un environnement virtuel (installer python sur son ordinateur si ce n'est pas déjà le cas)

Dans le dossier du projet lancer les commandes suivantes dans un terminal:

    pip install virtualenv
    virtualenv venv
    .\venv\Scripts\activate

Vous devriez voir (venv) pour vous indiquer que vous êtes dans l'environnement virtuel


##2.	Installer les dépendances

Lancer la commande :

    pip install -r requirements.txt

Cela peut prendres quelques minutes

##3.	Lancer l'API

Toujours dans le même dossier, lancer l'API avec la commande:

    python runserver.py

##4.	Documentation de l'API

Toute la documentation de l'API est disponible à http://127.0.0.1:5000/ une fois l'API lancée

# Build and Test
TODO: Describe and show how to build your code and run the tests. 

# Contribute
TODO: Explain how other users and developers can contribute to make your code better. 

If you want to learn more about creating good readme files then refer the following [guidelines](https://docs.microsoft.com/en-us/azure/devops/repos/git/create-a-readme?view=azure-devops). You can also seek inspiration from the below readme files:
- [ASP.NET Core](https://github.com/aspnet/Home)
- [Visual Studio Code](https://github.com/Microsoft/vscode)
- [Chakra Core](https://github.com/Microsoft/ChakraCore)

# Configuration avec Docker

### Requirements

- [Docker](https://www.docker.com/get-started)
- [Docker Compose](https://docs.docker.com/compose/install/)

### Commencer

1. Clonez ce référentiel sur votre machine locale:

```sh
$ git clone URL
```

2. Accéder au répertoire du projet:

```sh
$ cd ProxIA
```

3. Construire l'image:

```sh
$ docker-compose build
```

3. Lancer l'image:

```sh
$ docker-compose up
```

4. Arrêter les conteneurs:

```sh
$ docker-compose down
```