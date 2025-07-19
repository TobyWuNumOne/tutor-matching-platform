from flask import Blueprint, request, jsonify
from flasgger import swag_from
from app.models.course import Course
from app.models.teacher import Teacher
from app.schemas.schemas import CourseSchema
from app.extensions import db

course_bp = Blueprint('courses', __name__)
course_schema = CourseSchema()
courses_schema = CourseSchema(many=True)


@course_bp.route('/courseinfo', methods=['GET'])
@swag_from({
    'tags': ['課程管理'],
    'summary': '獲取課程資訊',
    'description': '獲取所有課程資訊，包含老師詳細資訊',
    'parameters': [
        {
            'name': 'teacher_name',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '老師姓名篩選'
        },
        {
            'name': 'avatar',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '老師頭像篩選'
        },
        {
            'name': 'subject',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '科目篩選'
        },
        {
            'name': 'location',
            'in': 'query',
            'type': 'string',
            'required': False,
            'description': '地點篩選'
        },
        {
            'name': 'price',
            'in': 'query',
            'type': 'number',
            'required': False,
            'description': '價格'
        },
        
    ],
    'responses': {
        200: {
            'description': '成功獲取課程資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'data': {
                        'type': 'array',
                        'items': {
                            'type': 'object',
                            'properties': {
                                'id': {'type': 'integer', 'example': 1},
                                'subject': {'type': 'string', 'example': '數學'},
                                'description': {'type': 'string', 'example': '高中數學課程'},
                                'price': {'type': 'number', 'example': 800.0},
                                'location': {'type': 'string', 'example': '台北'},
                                'avg_rating': {'type': 'number', 'example': 4.5},
                                'teacher_id': {'type': 'integer', 'example': 1},
                                'teacher_name': {'type': 'string', 'example': '張老師'},
                                'avatar': {'type': 'string', 'example': 'avatar_url.jpg'},
                                'teacher_email': {'type': 'string', 'example': 'teacher@example.com'},
                                'created_at': {'type': 'string', 'example': '2024-01-01T10:00:00'}
                            }
                        }
                    },
                    'total': {'type': 'integer', 'example': 10}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '獲取課程資訊失敗'}
                }
            }
        }
    }
})
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

    