
from flask import Flask, render_template, redirect, request
from pymongo import MongoClient
import sys
import os
import random

card1, card2, card3, card4, card5, card6 = [], [], [], []
app = Flask(__name__)
host = os.getenv("MONGO_HOST")+":27017"

def get_content(host):
    client = MongoClient(host)
    db = client.marvel
    doc_ids = db.characters.distinct("id", {})
    doc_id = random.choice(doc_ids)
    doc_content = db.characters.find_one({"id": doc_id})
    image_url = doc_content['thumbnail'] + "/landscape_incredible." + doc_content['extension']
    name = doc_content['name']
    comic_items = doc_content['comics']['items']
    comic_list = []
    for comic in comic_items:
        comic_list.append(comic['name'])
    return {'image_url': image_url, 'name': name, 'comic_list': comic_list}
    
@app.route("/")
def main():
    global card1, card2, card3, card4, card5, card6
    card1 = get_content(host)
    card2 = get_content(host)
    card3 = get_content(host)
    card4 = get_content(host)
    
    return render_template('page.html', image1_url=card1['image_url'],
                            image2_url=card2['image_url'],
                            image3_url=card3['image_url'], 
                            image4_url=card4['image_url'],
                            name1=card1['name'], name2=card2['name'],
                            name3=card3['name'], name4=card4['name'],
                            seq1=card1['comic_list'], seq2=card2['comic_list'],
                            seq3=card3['comic_list'], seq4=card4['comic_list'],
                            seq5=card5['comic_list'], seq6=card6['comic_list'])

@app.route("/reload", methods=["POST"])
def reload():
    global card1, card2, card3, card4, card5, card6
    card = request.form["reload"]
    if card == "card1":
        card1 = get_content(host)
    elif card == "card2":
        card2 = get_content(host)
    elif card == "card3":
        card3 = get_content(host)
    elif card == "card4":
        card4 = get_content(host)
    elif card == "card5":
        card5 = get_content(host)
    else:
        card6 = get_content(host)

    return render_template('page.html', image1_url=card1['image_url'],
                            image2_url=card2['image_url'],
                            image3_url=card3['image_url'], 
                            image4_url=card4['image_url'],
                            image5_url=card5['image_url'],
                            image6_url=card6['image_url'],
                            name1=card1['name'], name2=card2['name'],
                            name3=card3['name'], name4=card4['name'],
                            seq1=card1['comic_list'], seq2=card2['comic_list'],
                            seq3=card3['comic_list'], seq4=card4['comic_list'],
                            seq5=card5['comic_list'], seq6=card6['comic_list'],)
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=80)
    