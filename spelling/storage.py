from spelling import app
from flask.ext.sqlalchemy import SQLAlchemy
import json, random, string, sqlalchemy

db = SQLAlchemy(app)
class WordList(db.Model):
    identifier = db.Column(db.String(50), primary_key=True)
    title = db.Column(db.String(256))
    pages = db.Column(db.PickleType)

    def __init__(self, identifier, title, pages):
        self.identifier = identifier
        self.title = title
        self.pages = pages

    def __repr__(self):
        return '<WordList %r>' % self.identifier

if app.debug:
    print "Development mode, creating database schema"
    db.create_all()

def random_identifier():
    return ''.join(random.choice(string.lowercase) for i in xrange(5))

def save(title, pages):
    identifier = random_identifier()
    obj = WordList(identifier, title, pages)
    for i in xrange(5):
        try:
            db.session.add(obj)
            db.session.commit()
            break
        except sqlalchemy.exc.IntegrityError, e:
            db.session.rollback()
            obj.identifier = random_identifier()
    else:
        raise Exception("couldn't generate identifier")
    return obj.identifier

def load(identifier):
    return WordList.query.filter_by(identifier=identifier).one()
