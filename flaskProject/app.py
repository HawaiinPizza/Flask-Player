from flask import Flask, jsonify, render_template, request, redirect
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
import boto3
from json2html import *
import json
from jinja2 import Environment, FileSystemLoader
from boto3.dynamodb.conditions import Key
from collections import Counter
from api import getRecords,album
from datetime import datetime

import createTable
dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Albums')


fileLoader = FileSystemLoader("templates")
env = Environment(loader=fileLoader)

app = Flask(__name__)
def makeTable(table, primary):
    """Check if the table exist, and if not then make it"""
    client = boto3.client("dynamodb")
    tables =  client.list_tables()
    # if(table not in tables):
    #     client.create_table(TableName=names, 


@app.route("/")
def home():
    return "king of the pirates!"

@app.route('/additem')
def add_items():
    print(request.args)
    # date = datetime.fromisoformat(request.args["date"])
    date = request.args["date"]
    album2=request.args["album"]
    artist=request.args["artist"]
    genre=request.args["genre"]
    stream=request.args["stream"]
    art=request.args["art"]
    print()
    table.put_item(Item={"Artist": artist, "Album":album2,"genre":genre, "stream":stream, "art":art, "date":date })
    print(album2, artist, genre, stream, art, date, sep="\n")
    print()

    data=[album(artist, album2, genre, stream, art, date)]
    return redirect("/viewtable")
    # return render_template("table.j2", data=data)
    # return render_template("table.j2")


@app.route('/removeitem')
def remove():
    print(request.args)
    # date = datetime.fromisoformat(request.args["date"])
    date = request.args["date"]
    album2=request.args["album"]
    artist=request.args["artist"]
    genre=request.args["genre"]
    stream=request.args["stream"]
    art=request.args["art"]
    print("WOW")
    table.delete_item(TableName="Albums", Key={"Album":album2, "Artist":artist})
    return redirect("/viewtable")


@app.route('/search', methods=["POST", "GET"])
def get_items():
    if( request.method == "GET"):
        return render_template("table.j2")
    elif( request.method == "POST"):
        search = request.form["search"]
        if(search !=""):
            data = getRecords(search)
            tmp = dict((album.album, album) for album in data).values()
            return render_template("table.j2", data=tmp)
        return render_template("table.j2")




@app.route('/viewtable')
def searchbar():
    response = table.scan()
    response = (response['Items'])
# [{'Title': 'Naruto Uncut, Season 3, Vol. 2', 'date': '2008-10-13', 'stream': 'https://video-ssl.itunes.apple.com/itunes-assets/Video128/v4/39/e0/ee/39e0eedf-1198-c0b7-af62-a39f646bfab9/mzvf_22655529530827002.64│························
# 0x480.h264lc.U.p.m4v', 'art': 'https://is5-ssl.mzstatic.com/image/thumb/Video/v4/35/1c/ca/351cca34-39f9-42d1-ec08-93f156cb4ed4/source/100x100bb.jpg', 'genre': 'Animation', 'Artist': 'Naruto'}]                  │························
    def extract(i):
        return album(i["Artist"], i["Album"], i["genre"], i["stream"], i["art"], i["date"])
    data = list(map(extract, response))
    # rendered = env.get_template("getitemtemplate.html").render(albums=response)
    # with open(f"./templates/table.html", "w") as f:
    #     f.write(rendered)
    print(data)
    return render_template("listTable.j2", data=data)
    # return render_template("listTable.j2")


# @app.route('/')
# def getsearchterm():
#     search = request.args.get('q')
#     return app.route('/'+search)



if __name__ == '__main__':
    app.run()
