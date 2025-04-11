from . import db

class Weapon(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    damage = db.Column(db.Integer, nullable=False)
    weight = db.Column(db.Float, nullable=False)
    value = db.Column(db.Integer, nullable=False)
    type = db.Column(db.String(50), nullable=True)
    upgrade = db.Column(db.String(100), nullable=True)
    perk = db.Column(db.String(100), nullable=True)
    category = db.Column(db.String(50), nullable=True)
    speed = db.Column(db.Float, nullable=True)
