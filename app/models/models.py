from app import db

class Hero(db.Model):
    __tablename__ = 'heroes'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    image_url = db.Column(db.String(256))

    def __repr__(self):
        return f'<Hero {self.name}>'

class UnitType(db.Model):
    __tablename__ = 'unit_types'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)

    def __repr__(self):
        return f'<id {self.id} UnitType {self.name}>'

class Game(db.Model):
    __tablename__ = 'games'
    id = db.Column(db.Integer, primary_key=True)
    # исправь добавь за значение по умочанию текущее время
    timestamp = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    player1_hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    player1_place = db.Column(db.Integer, nullable=False)
    player1_unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id'))
    player2_hero_id = db.Column(db.Integer, db.ForeignKey('heroes.id'))
    player2_place = db.Column(db.Integer, nullable=False)
    player2_unit_type_id = db.Column(db.Integer, db.ForeignKey('unit_types.id'), default=1)
    fl_calculated = db.Column(db.Boolean, default=False)

    player1_hero = db.relationship('Hero', foreign_keys=[player1_hero_id])
    player2_hero = db.relationship('Hero', foreign_keys=[player2_hero_id])
    player1_unit_type = db.relationship('UnitType', foreign_keys=[player1_unit_type_id])
    player2_unit_type = db.relationship('UnitType', foreign_keys=[player2_unit_type_id])

    def __repr__(self):
        txt = f"""<Game {self.id} ({self.timestamp}
        - Calculated: {self.fl_calculated})
        Player 1: {self.player1_hero.name} ({self.player1_place}), {self.player1_unit_type.name}
        Player 2: {self.player2_hero.name} ({self.player2_place}), {self.player2_unit_type.name})>
        """
        return txt
