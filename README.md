# Musicorpus

## Table of contents
* [General Informations](#general-informations)
* [Installation](#installation)
* [How To Run?](#how-to-run)

## General Informations
This repository is created for the final project of [IDEA Software Development Project.](https://idea.metu.edu.tr/).

## Contributors:
* [Balam Kaynakçı](https://github.com/balamkaynakci)

* [Selin Bilginay](https://github.com/selinbilginay)

* [Ali Kemal Yıldırım](https://github.com/akemalyildirim1)

## Installation

### Python Dependencies
Make sure that you are in a **virtual environment** before installing the requirements:   
Run `pip install -r requirements.txt`

### .env
You need to create a `.env` file to run.  
The format of this `.env` file should be in this format:
```
CLIENT_ID="client_id"
CLIENT_SECRET="client_secret"
```
You need to create a new project in the [Spotify dashboard](https://developer.spotify.com/dashboard/applications)

After creating, you will see your `CLIENT_ID` and `CLIENT_SECRET`. Add them into `.env` file.

Then, click `EDIT SETTINGS` button from [Spotify dashboard](https://developer.spotify.com/dashboard/applications), you need to add `http://localhost:8888/spotify/callback/` into `Redirect URIs`.

### Database
Default database settings:
```
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'musicorpus',
        "USER":"postgres",
        "PASSWORD": "postgres",
        "PORT":5432,
        "HOST":"localhost"
    }
}
```
According to your `POSTGRESQL` configurations, you can change this `DATABASES` settings in [Musicorpus/settings.py](Musicorpus/settings.py) 

After connecting to the database correctly:

Run `python3 manage.py migrate` 

## How to Run?
After activating **virtual environment**:

Run `python3 manage.py runserver 8888`  

Now, you can click [here](http://localhost:8888/) to open this website.
