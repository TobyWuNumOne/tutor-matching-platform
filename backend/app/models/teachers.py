from app.extensions import db
from enum import Enum

class GenderEnum(Enum):
    MALE = 'male'
    FEMALE = 'female'
    OTHER = 'other'

class Teachers(db.Model):
    __tablename__ = 'teachers'
    id = db.Column(db.Integer, primary_key=True)
    avatar = db.Column(db.String(255), nullable=True)
    name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    subject = db.Column(db.String(255), nullable=False)
    phone = db.Column(db.String(255), nullable=False)
    gender = db.Column(db.Enum(GenderEnum), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    education = db.Column(db.String(255), nullable=True)
    certifications = db.Column(db.String(255), nullable=True)
    intro = db.Column(db.String(255), nullable=True)
    teaching_experience = db.Column(db.Text, nullable=True)
    status = db.Column(db.String(255), nullable=False)
    blue_premium = db.Column(db.Boolean, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    # 關聯設定
    user_id = db.relationship('User', backref='teachers')
    def __repr__(self):
        return f'<Teachers {self.subject}>'