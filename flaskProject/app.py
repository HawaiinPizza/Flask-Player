from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
import boto3
from json2html import *
import json
from jinja2 import Environment, FileSystemLoader
from boto3.dynamodb.conditions import Key
from collections import Counter
from api import getRecords

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

@app.route('/additems')
def add_items():pass



@app.route('/search', methods=["POST", "GET"])
def get_items():
    if( request.method == "GET"):
        return render_template("table.j2")
    elif( request.method == "POST"):
        search = request.form["search"]
        data = getRecords(search)
        tmp = dict((album.album, album) for album in data).values()
        return render_template("table.j2", data=tmp)



@app.route('/viewtable')
def searchbar():
    # response = table.scan()
    # response = (response['Items'])
    # rendered = env.get_template("getitemtemplate.html").render(albums=response)
    # with open(f"./templates/table.html", "w") as f:
    #     f.write(rendered)
    return render_template("search.html")


# @app.route('/')
# def getsearchterm():
#     search = request.args.get('q')
#     return app.route('/'+search)



if __name__ == '__main__':
    app.run()
