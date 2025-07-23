from app.extensions import db
from .model import BaseModel


class Booking(BaseModel):
    __tablename__ = "bookings"

    course_id = db.Column(db.Integer, db.ForeignKey('courses.id'), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey('students.id'), nullable=False)
    schedule_date = db.Column(db.String(50), nullable=False)  # 可以存 "2024-01-15 14:00" 格式
    status = db.Column(db.String(20), nullable=False, default='pending')  # pending, confirmed, completed, cancelled
    
    # 建立關聯
    course = db.relationship('Course', backref=db.backref('bookings', lazy=True))
    student = db.relationship('Student', backref=db.backref('bookings', lazy=True))
    
    def __repr__(self):
        return f'<Booking {self.id}: Course {self.course_id} - Student {self.student_id}>'
    
    def to_dict_with_relations(self):
        """包含關聯資料的字典轉換"""
        base_dict = self.to_dict()
        
        # 加入課程資訊
        if self.course:
            base_dict['course'] = {
                'id': self.course.id,
                'subject': self.course.subject,
                'description': self.course.description,
                'price': float(self.course.price) if self.course.price else None,
                'location': self.course.location,
                'teacher_name': self.course.teacher.name if self.course.teacher else None
            }
        
        # 加入學生資訊
        if self.student:
            base_dict['student'] = {
                'id': self.student.id,
                'name': self.student.name,
                'email': self.student.email
            }
            
        return base_dict