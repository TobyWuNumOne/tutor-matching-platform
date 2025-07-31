from app.extensions import db
from .model import BaseModel


class Review(BaseModel):
    __tablename__ = "reviews"

    course_id = db.Column(db.Integer, db.ForeignKey("courses.id"), nullable=False)
    student_id = db.Column(db.Integer, db.ForeignKey("students.id"), nullable=False)
    rating = db.Column(db.String(10), nullable=False)  # 可以存 "5" 或 "4.5" 等
    comment = db.Column(db.Text)

    # 建立關聯
    course = db.relationship("Course", backref=db.backref("reviews", lazy=True))
    student = db.relationship("Student", backref=db.backref("reviews", lazy=True))

    def __repr__(self):
        return f"<Review {self.id}: Course {self.course_id} - Rating {self.rating}>"

    @property
    def rating_float(self):
        """將評分轉換為浮點數"""
        try:
            return float(self.rating)
        except (ValueError, TypeError):
            return 0.0

    def to_dict_with_relations(self):
        """包含關聯資料的字典轉換"""
        base_dict = self.to_dict()
        base_dict["rating_float"] = self.rating_float

        # 加入課程資訊
        if self.course:
            base_dict["course"] = {
                "id": self.course.id,
                "subject": self.course.subject,
                "description": self.course.description,
                "teacher_name": (
                    self.course.teacher.name if self.course.teacher else None
                ),
            }

        return base_dict
