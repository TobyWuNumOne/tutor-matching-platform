from app.extensions import db
from .model import BaseModel


class Teacher(BaseModel):
    __tablename__ = "teachers"

    avatar = db.Column(db.String(255))
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), nullable=False)
    phone = db.Column(db.String(20))
    gender = db.Column(db.String(10))
    age = db.Column(db.String(20))
    education = db.Column(db.String(100), nullable=False)
    certifications = db.Column(db.String(255), nullable=False)
    intro = db.Column(db.Text, nullable=False)
    teaching_experience = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20))
    blue_premium = db.Column(db.Boolean, default=False)
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 關聯
    user = db.relationship("User", backref="teacher_profile")

    def __repr__(self):
        return f"<Teacher {self.name}>"
