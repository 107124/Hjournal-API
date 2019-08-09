from flask import Flask, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from flask_marshmallow import Marshmallow
from flask_heroku import Heroku
import os

app = Flask(__name__)
heroku = Heroku(app)

basedir = os.path.abspath(os.path.dirname(__file__))
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(basedir, "app.sqlite")

CORS(app)

db = SQLAlchemy(app)
ma = Marshmallow(app)

class journal(db.Model):
    __tablename__ = "journals"
    id = db.Column(db.Integer, primary_key=True)
    symptom = db.Column(db.String(50))
    pain_rate = db.Column(db.Integer)
    journal_detail = db.Column(db.String(500))

    def __init__(self, symptom, pain_rate, journal_detail):
        self.symptom = symptom
        self.pain_rate = pain_rate
        self.journal_detail = journal_detail

class journalSchema(ma.Schema):
    class Meta:
        fields = ("id", "symptom", "pain_rate","journal_detail")

journal_schema = journalSchema()
journals_schema = journalSchema(many=True)

@app.route("/") #homepage
def greeting():
    return "<h1>hjournal application API</h1>" 

@app.route("/journals",methods=["GET"])
def get_journals():
    all_journals = journal.query.all()
    result = journals_schema.dump(all_journals)
    return jsonify(result.data)


@app.route("/journal/<id>",methods=["GET"])
def get_journal(id):
    journal_single = journal.query.get(id)
    return journal_schema.jsonify(journal_single)


@app.route("/add-journal" , methods=["POST"])
def add_journal():
    symptom = request.json["symptom"]
    pain_rate = request.json["pain_rate"]
    journal_detail = request.json["journal_detail"]

    new_journal = journal(symptom, pain_rate, journal_detail)

    db.session.add(new_journal)
    db.session.commit()

    return jsonify("journal CREATED")

@app.route("/journal/<id>", methods=["DELETE"])  
def delete_journal(id):
    journal_single = journal.query.get(id)
    db.session.delete(journal_single)
    db.session.commit()

    return jsonify("journal DELETED")


@app.route("/journal/<id>", methods=["PUT"])  
def update_journal(id):
    journal_single = journal.query.get(id)
    
    new_symptom = request.json["symptom"]
    new_journal_detail = request.json["journal_detail"]

    journal_single.symptom = new_symptom
    journal_single.journal_detail = new_journal_detail

    db.session.commit()

    return journal_schema.jsonify(journal_single)


if __name__ =="__main__":
    app.debug = True
    app.run()