from app.extensions import db
from .model import BaseModel
class Course(BaseModel):
    __tablename__ = "courses"

    subject = db.Column(db.String(255), nullable=False)
    teacher_id = db.Column(db.Integer, db.ForeignKey('teachers.id', name="fk_courses_teacher_id", ondelete='CASCADE'), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Numeric(8, 2), nullable=False)
    location = db.Column(db.String(255), nullable=False)
    avg_rating= db.Column(db.Float, nullable=True)

    # 關聯
    teacher = db.relationship("Teacher", back_populates="courses")

    def __repr__(self):
        return f"<Course {self.subject}>"
    def calculate_avg_rating(self):
        """計算平均評分"""
        if not self.reviews:
            return 0.0
        
        total_rating = sum(review.rating_float for review in self.reviews)
        return round(total_rating / len(self.reviews), 2)
    
    def update_avg_rating(self):
        """更新平均評分到資料庫"""
        self.avg_rating = self.calculate_avg_rating()
        db.session.commit()
        return self.avg_rating
    
    def to_dict_with_relations(self):
        """包含關聯資料的字典轉換"""
        base_dict = self.to_dict()
        
        # 加入老師資訊
        if self.teacher:
            base_dict['teacher'] = {
                'id': self.teacher.id,
                'name': self.teacher.name,
                'email': self.teacher.email,
                'avatar': self.teacher.avatar
            }
        
        # 加入評論統計
        base_dict['review_count'] = len(self.reviews) if self.reviews else 0
        base_dict['booking_count'] = len(self.bookings) if self.bookings else 0
        
        return base_dict