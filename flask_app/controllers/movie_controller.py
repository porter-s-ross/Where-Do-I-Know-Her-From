from flask_app import app
from flask import render_template, redirect, session, request, flash

# from flask_app.models.movies import Movie_search

import imdb
moviesDB = imdb.IMDb()



@app.route("/homepage")
def homepage():
    return render_template("homepage.html")



@app.route("/get_results", methods=["POST"])
def compare_results():
    if request.form["search_one"] == "":
        flash("please enter two movies")
        return redirect ("/homepage")
    elif request.form["search_one"] == "":
        flash("please enter two movies")
        return redirect("/homepage")
    else:
        session["search_two"] = request.form["search_two"]
        session["search_one"] = request.form["search_one"]
        
    return redirect("results")

@app.route("/results")
def show_results():
    
    search_one = session["search_one"]
    movies = moviesDB.search_movie(search_one)
    id = movies[0].getID()
    result_one = moviesDB.get_movie(id)
    
    search_two = session["search_two"]
    movies = moviesDB.search_movie(search_two)
    id = movies[0].getID()
    result_two = moviesDB.get_movie(id)


    result_one_cast = result_one["cast"]
    result_two_cast = result_two["cast"]
    shared_cast = []

    sort = {}
    # print(result_one_cast)
    # print(result_two_cast)
    

    for i in range(0, len(result_one_cast)):
        sort[result_one_cast[i]["name"]] = result_one_cast[i]

    for i in range(0, len(result_two_cast)):
        if result_two_cast[i]["name"] in sort:
            shared_cast.append({
                "movie_one": result_two_cast[i],
                "movie_two": sort[result_two_cast[i]["name"]]
            })

    if len(shared_cast) < 1:
        flash("no results found, please try again")
        return redirect("/homepage")

    print(shared_cast[0])
    return render_template("/results.html", result_one = result_one, result_two = result_two, shared_cast = shared_cast)






@app.route("/movie/info/<result>")
def movie_info(result):
    movies = moviesDB.search_movie(result)
    id = movies[0].getID()
    result = moviesDB.get_movie(id)
    cast = result["cast"]
    type(cast)
    directors = result["directors"]

    directStr = ' '.join(map(str, directors))

    # cast = ' '.join(map(str, casting))


    return render_template("/movie_info.html", result = result, directors = directStr, cast = cast)

@app.route("/bio/<actor>")
def bio(actor):
    print(actor)
    search = moviesDB.search_person(actor)
    id = search[0].getID()
    person = moviesDB.get_person(id)
    # bio = moviesDB.get_person_biography(id)


    data = {
        "bio" : person["mini biography"],
        "birth_date" : person["birth date"],
        # "trivia" : person["trivia"],
        # "quotes" : person["quotes"],
        # "nicknames" : person["nick names"]
    }
    # films = person["filmography"]
    # titles = bio["titlesRefs"]

    films = []
    for film in person["filmography"].keys():
        for film in person['filmography'][film]:
            films.append(film)




    # print(person.keys())

    # name = person['name']
    # birthDate = person['birth date']
    # height = person['height']
    # trivia = person['trivia']
    # titleRefs = bio['titlesRefs']

    return render_template("/bio.html", person = person, data = data, films = films)
