from flask import Flask, request
from flask_restful import reqparse, Api, Resource
from get_twitter_followers import twitter_followers_count
from search_artist_on_spotify import spotify_search_artist

app = Flask(__name__)
api = Api(app)

todos = {}


class TodoSimple(Resource):

    def get(self, todo_id):
        return {todo_id: todos[todo_id]}

    def put(self, todo_id):
        todos[todo_id] = request.form['data']
        fc = twitter_followers_count(artist_twitter_handle="mhabdulbaaki")
        artist = spotify_search_artist(name="sarkodie")
        return {todo_id: todos[todo_id], "count": fc, **artist}


api.add_resource(TodoSimple, '/<string:todo_id>')

if __name__ == '__main__':
    app.run(debug=True)
