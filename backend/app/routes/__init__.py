from .auth_routes import auth_bp
from .user_routes import user_bp
from .course_routes import course_bp
from .teacher_routes import teacher_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(course_bp, url_prefix="/api/course")
    app.register_blueprint(teacher_bp, url_prefix="/api/teacher")
