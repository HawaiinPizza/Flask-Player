from flask import Flask, jsonify, render_template, request
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField, RadioField, HiddenField, StringField, IntegerField, FloatField
import boto3
from json2html import *
import json
from jinja2 import Environment, FileSystemLoader
from boto3.dynamodb.conditions import Key

dynamodb = boto3.resource('dynamodb', region_name='us-east-1')
table = dynamodb.Table('Albums')


fileLoader = FileSystemLoader("templates")
env = Environment(loader=fileLoader)

app = Flask(__name__)


@app.route('/additems')



@app.route('/viewtable')
def get_items():
    response = table.scan()
    response = (response['Items'])
    rendered = env.get_template("getitemtemplate.html").render(albums=response)
    with open(f"./templates/table.html", "w") as f:
        f.write(rendered)
    return render_template("table.html")


@app.route('/search')
def searchbar():
    return render_template("search.html")


@app.route('/')
def getsearchterm():
    search = request.args.get('q')
    return app.route('/'+q)



if __name__ == '__main__':
    app.run()
