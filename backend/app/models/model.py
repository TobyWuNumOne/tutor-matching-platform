from app.extensions import db
from datetime import datetime, timezone


class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    updated_at = db.Column(
        db.DateTime,
        default=lambda: datetime.now(timezone.utc),
        onupdate=lambda: datetime.now(timezone.utc),
    )

    def save(self):
        """保存記錄"""
        db.session.add(self)
        db.session.commit()
        return self

    def delete(self):
        """刪除記錄"""
        db.session.delete(self)
        db.session.commit()
        return True

    def update(self, **kwargs):
        """更新記錄"""
        for key, value in kwargs.items():
            if hasattr(self, key):
                setattr(self, key, value)
        db.session.commit()
        return self

    def to_dict(self):
        """轉換為字典"""
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
