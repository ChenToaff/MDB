from flask_login import UserMixin
import os
import hashlib
import requests
import json
from .secrets import apiKey

def hash_password(password,**kwargs):
    if 'salt' in kwargs:
        salt =  kwargs['salt']
    else:
        salt =  os.urandom(16).hex()
    hash = hashlib.md5(('%s%s' % (salt, password)).encode('utf-8')).hexdigest()
    return (hash,salt)


class User(UserMixin):
    def __init__(self, user):
        self.id = (user['email'] , user['password'])
        self.name = user['name']
        self.email = user['email']
        self.password = user['password']
        self.salt = user['salt']
        self.confirmed = user['confirmed']
    



def get_movie(imdbId):
    url = "http://www.omdbapi.com/?apikey="+ apiKey+"&i=" +imdbId+ "&plot=full"
    try:
        data = requests.get(url)
        return data.json()
    except:
        return ""

def get_movies(name):
    url = "http://www.omdbapi.com/?apikey="+ apiKey+"&i=" +name.replace(" ", "%20")+"&type=movie"
    try:
        data = requests.get(url).json()
        return json.dumps(sorted(data["Search"],key = lambda x: (int(x["Year"].split("–")[0])),reverse=True))
    except Exception as e:
        print(e)
        return ""


