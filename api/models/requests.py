from ..utils import db
from datetime import datetime

class Request(db.Model):
    __tablename__ = 'Requests'
    id=db.Column(db.Integer(), primary_key=True)
    text=db.Column(db.String(), nullable=False)
    intention = db.Column(db.String(), nullable=False)
    entities = db.Column(db.JSON())
    criticity = db.Column(db.String(), nullable=False)
    created_at = db.Column(db.DateTime(), default=datetime.utcnow)
    user_id = db.Column(db.Integer(), db.ForeignKey('users.id'))

    def __repr__(self):
        return f'<Request : {self.text}'

    def save(self):
        db.session.add(self)
        db.session.commit()
