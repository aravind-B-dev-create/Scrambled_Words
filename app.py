from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from flask import Flask, render_template, request, redirect, flash
from datetime import datetime
from bson.objectid import ObjectId
import random

uri = "mongodb+srv://aravindn2004:nArAyAnA28@cluster0.6yq2yjf.mongodb.net/?appName=Cluster0"

# Create a new client and connect to the server
client = MongoClient(uri, tls = True, tlsAllowInvalidCertificates=True)
db = client.Word_Databse  
app = Flask("Word_Database")
app.config['SECRET_KEY'] = ';ljapw98u439p8lvkdfscv'


@app.route('/', methods = ['GET', 'POST'])
def index():
    if request.method == "GET":
        return render_template('index.html')
    if request.method == 'POST':
        a = list(request.form['word'])
        random.shuffle(a)
        scrambled = ''.join(a)
        document = {'word_unscrambled':request.form['word'], 'word_scrambled':scrambled}
        db.words.insert_one(document)
        flash("New word added")
        return redirect('/')


@app.route('/play', methods = ["GET", "POST"])
def getlist():
    sample = []
    keys = []
    words = db.words.find()
    for i in words:
        print("hello")
        keys.append([i['word_scrambled'], i['_id']])
        print(keys)
    for i in range(0, 5, 1):
        rand = random.choice(keys)
        keys.remove(rand)
        sample.append(rand)
    if (request.method == "GET"):
        return render_template('play_game.html', jumbledlist = sample)
    if (request.method == "POST"):
        response = []
        score = 0
        correct = []
        for j in request.form:
            response.append(request.form[j])
            ans = db.words.find_one({'_id':ObjectId(j)})
            correct.append(ans['word_unscrambled'])
            if (request.form[j] == ans['word_unscrambled']):
                score += 1
        return render_template('result.html', score = score, user_answer = response, correct_answer = correct)
            



#href = "/delete/{{note['_id']}}"


if __name__ == '__main__':
    app.run(debug=True)



