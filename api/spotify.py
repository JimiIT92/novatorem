import os
import json
import random
import requests

from base64 import b64encode
from dotenv import load_dotenv, find_dotenv
from flask import Flask, Response, jsonify, render_template, templating, request

load_dotenv(find_dotenv())

# Spotify scopes:
#   user-read-currently-playing
#   user-read-recently-played
PLACEHOLDER_IMAGE = "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"
SPOTIFY_CLIENT_ID = os.getenv("SPOTIFY_CLIENT_ID")
SPOTIFY_SECRET_ID = os.getenv("SPOTIFY_SECRET_ID")
SPOTIFY_REFRESH_TOKEN = os.getenv("SPOTIFY_REFRESH_TOKEN")

FALLBACK_THEME = "spotify.html.j2"

REFRESH_TOKEN_URL = "https://accounts.spotify.com/api/token"
NOW_PLAYING_URL = "https://api.spotify.com/v1/me/player/currently-playing"

app = Flask(__name__)


def getAuth():
    return b64encode(f"{SPOTIFY_CLIENT_ID}:{SPOTIFY_SECRET_ID}".encode()).decode(
        "ascii"
    )


def refreshToken():
    data = {
        "grant_type": "refresh_token",
        "refresh_token": SPOTIFY_REFRESH_TOKEN,
    }

    headers = {"Authorization": "Basic {}".format(getAuth())}
    response = requests.post(REFRESH_TOKEN_URL, data=data, headers=headers)

    try:
        return response.json()["access_token"]
    except KeyError:
        print(json.dumps(response.json()))
        print("\n---\n")
        raise KeyError(str(response.json()))


def nowPlaying():
    token = refreshToken()
    headers = {"Authorization": f"Bearer {token}"}
    response = requests.get(NOW_PLAYING_URL, headers=headers)

    if response.status_code == 204:
        return {}
    return response.json()


def barGen(barCount):
    barCSS = ""
    left = 1
    for i in range(1, barCount + 1):
        anim = random.randint(1000, 1350)
        barCSS += (
            ".bar:nth-child({})  {{ left: {}px; animation-duration: {}ms; }}".format(
                i, left, anim
            )
        )
        left += 4
    return barCSS


def getTemplate():
    try:
        file = open("api/templates.json", "r")
        templates = json.loads(file.read())
        return templates["templates"][templates["current-theme"]]
    except Exception as e:
        print(f"Failed to load templates.")
        return FALLBACK_THEME


def loadImageB64(url):
    response = requests.get(url)
    return b64encode(response.content).decode("ascii")


def codeGen(uri):
    if uri == {} or uri == "" or uri is None:
        return "R0lGODlhAQABAAAAACH5BAEKAAEALAAAAAABAAEAAAICTAEAOw=="
    url = "https://scannables.scdn.co/uri/plain/png/000000/white/640/" + uri
    return loadImageB64(url)



def makeSVG(data, background_color, border_color):
    barCount = 84
    contentBar = "".join(["<div class='bar'></div>" for i in range(barCount)])
    barCSS = barGen(barCount)

    if data == {} or data["item"] == "None" or data["item"] is None:
        contentBar = ""
        currentStatus = "Not vibing :("
        item = {'name': "Currently not vibing 😢", 'artists': [{'name': "That's sad...", 'external_urls': {'spotify': "https://www.spotify.com/"}}], 'external_urls': {'spotify': "https://www.spotify.com/"}, 'album': {'images': []}, 'uri': ""}
    else:
        item = data["item"]
        currentStatus = "Vibing to:"

    if item["album"]["images"] == []:
        image = PLACEHOLDER_IMAGE
    else:
        image = loadImageB64(item["album"]["images"][1]["url"])

    artistName = item["artists"][0]["name"].replace("&", "&amp;")
    songName = item["name"].replace("&", "&amp;")
    songURI = item["external_urls"]["spotify"]
    artistURI = item["artists"][0]["external_urls"]["spotify"]
    scanCode = codeGen(item["uri"])

    dataDict = {
        "contentBar": contentBar,
        "barCSS": barCSS,
        "artistName": artistName,
        "songName": songName,
        "songURI": songURI,
        "artistURI": artistURI,
        "image": image,
        "status": currentStatus,
        "background_color": background_color,
        "border_color": border_color,
        "scanCode": scanCode
    }

    return render_template(getTemplate(), **dataDict)


@app.route("/", defaults={"path": ""})
@app.route("/<path:path>")
@app.route('/with_parameters')
def catch_all(path):
    background_color = request.args.get('background_color') or "181414"
    border_color = request.args.get('border_color') or "181414"

    data = nowPlaying()
    svg = makeSVG(data, background_color, border_color)

    resp = Response(svg, mimetype="image/svg+xml")
    resp.headers["Cache-Control"] = "s-maxage=1"

    return resp


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=os.getenv("PORT") or 5000)
