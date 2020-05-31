from .app import app,mongo
from .models import get_movie,get_movies
from flask_login import login_required,current_user
from flask import jsonify,redirect,render_template,request
import json

movies = mongo.db.movies

@app.route('/movie/<token>')
@login_required
def movie_data(token):
    movie = movies.find_one({"imdbID": token},{"_id": 0})
    if request.headers.get('JSON'):
        if movie == None:
            movie = dict(get_movie(token))
            movie["Liked"] = 0
            movies.insert_one(dict(movie))
        else:
            movie["Liked"] = 1 if movie["imdbID"] in dict(mongo.db.users.find_one({"email":current_user.email},{"movies":1}))["movies"].keys() else 0
        return jsonify(**movie)
    else:
        if movie == None:
            return redirect("/")
        movie["Liked"] = 1 if movie["imdbID"] in dict(mongo.db.users.find_one({"email":current_user.email},{"movies":1}))["movies"].keys() else 0
        return render_template("movie_page.html",Plot = movie['Plot'],Title = movie["Title"] +" ("+movie["Year"]+")" ,Poster = movie["Poster"],Liked = movie["Liked"]) 



@app.route('/movies/search/<token>')
@login_required
def movies_search(token):
    return get_movies(token)

@app.route('/movies/new')
@login_required
def movies_new():
    movie = movies.find({},{"_id": 0,"imdbID": 1,"Poster":1 ,"Year": 1,"imdbRating":1,"Liked":1})
    movie =  sorted(movie,key = lambda x: (int(x["Liked"]), int(x["Year"].split("–")[0]),float(x["imdbRating"])),reverse=True)[:10]

    return jsonify(json.dumps(movie))

@app.route('/movies/liked')
@login_required
def movies_liked():
    movie_list = mongo.db.users.find_one({"email":current_user.email},{"_id":0,"movies":1})["movies"].values()
    movie_list =  sorted(movie_list,key = lambda x: (int(x["Year"].split("–")[0]),float(x["imdbRating"])),reverse=True)
    return jsonify(json.dumps(movie_list))

@app.route('/movies/like/<token>')
@login_required
def movie_add(token):
    users =  mongo.db.users
    if token not in users.find_one({"email": current_user.email},{"_id":0,"movies":1})["movies"].keys():
        movie = list(movies.find({"imdbID": token},{"_id": 0,"Poster":1 ,"Year": 1,"imdbRating":1,"imdbID":1}))
        if(movie):
            movies.update_one({"imdbID": token},{ "$inc": { "Liked": 1} })
            users.update_one({"email": current_user.email},{ "$set": {"movies."+token: movie[0]}})
            return "Liked "+ token
        else:
            return "no such movie"
    else:
        movies.update_one({"imdbID": token},{ "$inc": { "Liked": -1} })
        users.update_one({"email": current_user.email},{ "$unset": {"movies."+token:""}})
        return "Unliked " +token
