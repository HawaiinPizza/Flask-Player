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
    return redirect("/viewtable")

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
