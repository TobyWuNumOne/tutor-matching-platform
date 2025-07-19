from app.extensions import db
from .model import BaseModel
class Teacher(BaseModel):
    __tablename__ = "courses"

    subject = db.Column(db.String(225), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), ondelete='CASCADE', nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Muneric(8, 2), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    avg_rating= db.Column(db.Float, nullable=True)

    # 關聯
    teacher = db.relationship("Teacher", backref="courses")

    def __repr__(self):
        return f"<Course {self.subject}>"