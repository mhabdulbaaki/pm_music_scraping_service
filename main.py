from flask import Flask
from flask_restful import reqparse, Api, Resource
from get_artist_media_performance_metrics import get_artist_stats

app = Flask(__name__)
api = Api(app)


parser = reqparse.RequestParser()

parser.add_argument("spotifyURL", location="args", required=True)
parser.add_argument("twitterURL", location="args")
parser.add_argument("instagramURL", location="args")
parser.add_argument("tiktokURL", location="args")
parser.add_argument("fbURL", location="args")
parser.add_argument("youtubeURL", location="args")
parser.add_argument("soundcloudURL", location="args")


class ArtistStats(Resource):

    def get(self):
        args = parser.parse_args()
        data = get_artist_stats(
            spotify_url=args["spotifyURL"],
            soundcloud=args["soundcloudURL"],
            youtube=args["youtubeURL"],
            twitter=args["twitterURL"],
            instagram=args["instagramURL"],
            fb=args["fbURL"],
            tiktok=args["tiktokURL"],
        )
        if data:
            return {"data": data}, 200


api.add_resource(ArtistStats, '/artist')

if __name__ == '__main__':
    app.run(debug=True)
