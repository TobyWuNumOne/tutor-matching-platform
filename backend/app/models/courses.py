from app.extensions import db
from datetime import datetime

class Courses(db.Model):
    __tablename__ = 'courses'
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(255), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(8, 2),nullable=False)
    location = db.Column(db.String(255), nullable=False)
    avg_rating = db.Column(db.Float)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    # 關聯設定
    teacher = db.relationship('Teachers', backref='courses')
    def __repr__(self):
        return f'<Courses {self.subject}>'