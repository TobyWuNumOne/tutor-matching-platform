from flask import Blueprint, request, jsonify
from app.models.course import Course
from app.models.teacher import Teacher
from app.schemas.schemas import CourseSchema
from app.extensions import db

course_bp = Blueprint('courses', __name__)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


@course_bp.route('/courseinfo', methods=['GET'])
def get_courses_with_teacher_details():
    """
    獲取課程資訊，包含老師名字
    """
    try:
        # 使用 joinedload 來確保一次查詢就載入關聯資料
        from sqlalchemy.orm import joinedload
        
        query = Course.query.options(joinedload(Course.teacher))
        
        # 可以直接透過關聯篩選
        teacher_name = request.args.get('teacher_name')
        if teacher_name:
            query = query.join(Teacher).filter(Teacher.name.ilike(f'%{teacher_name}%'))
        
        courses = query.all()
        
        # 手動組建回應，確保包含 teacher name
        result = []
        for course in courses:
            course_data = {
                'id': course.id,
                'subject': course.subject,
                'description': course.description,
                'price': float(course.price) if course.price else None,
                'location': course.location,
                'avg_rating': course.avg_rating,
                'teacher_id': course.teacher_id,
                'teacher_name': course.teacher.name if course.teacher else None,  
                'avatar': course.teacher.avatar if course.teacher else None,  
                'teacher_email': course.teacher.email if course.teacher else None,
                'created_at': course.created_at.isoformat() if course.created_at else None
            }
            result.append(course_data)
        
        return jsonify({
            'success': True,
            'data': result,
            'total': len(result)
        }), 200
        
    except Exception as e:
        return jsonify({
            'success': False,
            'message': f'獲取課程資訊失敗: {str(e)}'
        }), 500

    