from app.extensions import db
from .model import BaseModel
from werkzeug.security import generate_password_hash, check_password_hash


class User(BaseModel):
    __tablename__ = "users"

    name = db.Column(db.String(100), nullable=False)
    account = db.Column(db.String(50), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(20), nullable=False)  # 'teacher', 'student', 'admin'

    def set_password(self, password):
        """設定密碼（加密）"""
        self.password = generate_password_hash(password)

    def check_password(self, password):
        """驗證密碼"""
        return check_password_hash(self.password, password)

    def __repr__(self):
        return f"<User {self.account}>"
