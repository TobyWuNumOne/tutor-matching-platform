from .auth_routes import auth_bp
from .user_routes import user_bp
from .student_route import student_bp
from .course_routes import course_bp
from .teacher_routes import teacher_bp
from .booking_routes import booking_bp
from .review_routes import review_bp
from .payment_routes import payment_bp


def register_routes(app):
    app.register_blueprint(auth_bp, url_prefix="/api/auth")
    app.register_blueprint(user_bp, url_prefix="/api/users")
    app.register_blueprint(course_bp, url_prefix="/api/course")
    app.register_blueprint(teacher_bp, url_prefix="/api/teacher")
    app.register_blueprint(booking_bp, url_prefix="/api/booking")
    app.register_blueprint(student_bp, url_prefix="/api/student")
    app.register_blueprint(review_bp, url_prefix="/api/reviews")
    app.register_blueprint(payment_bp, url_prefix="/api/payment")
