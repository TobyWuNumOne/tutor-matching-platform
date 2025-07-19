from app.extensions import db
from .model import BaseModel


class Student(BaseModel):
    __tablename__ = "students"

    email = db.Column(db.String(120), nullable=False)
    gender = db.Column(db.String(10))
    age = db.Column(db.String(20))
    user_id = db.Column(db.Integer, db.ForeignKey("users.id"), nullable=False)

    # 關聯
    user = db.relationship("User", back_populates="student_profile")

    def __repr__(self):
        return f"<Student {self.email}>"
