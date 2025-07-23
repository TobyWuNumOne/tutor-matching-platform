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

@course_bp.route('/createcourse', methods=['POST'])
@swag_from({
    'tags': ['課程管理'],
    'summary': '新增課程',
    'description': '老師新增課程資訊',
    'parameters': [
        {
            'name': 'body',
            'in': 'body',
            'required': True,
            'description': '課程資訊',
            'schema': {
                'type': 'object',
                'properties': {
                    'subject': {
                        'type': 'string',
                        'description': '科目名稱',
                        'example': '數學'
                    },
                    'teacher_id': {
                        'type': 'integer',
                        'description': '老師ID',
                        'example': 1
                    },
                    'description': {
                        'type': 'string',
                        'description': '課程描述',
                        'example': '高中數學課程，包含代數與幾何'
                    },
                    'price': {
                        'type': 'number',
                        'description': '課程價格（每小時）',
                        'example': 800.0
                    },
                    'location': {
                        'type': 'string',
                        'description': '上課地點',
                        'example': '台北市信義區'
                    }
                },
                'required': ['subject', 'teacher_id', 'price', 'location']
            }
        }
    ],
    'responses': {
        201: {
            'description': '課程新增成功',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': True},
                    'message': {'type': 'string', 'example': '課程新增成功'},
                    'data': {
                        'type': 'object',
                        'properties': {
                            'id': {'type': 'integer', 'example': 1},
                            'subject': {'type': 'string', 'example': '數學'},
                            'teacher_id': {'type': 'integer', 'example': 1},
                            'description': {'type': 'string', 'example': '高中數學課程'},
                            'price': {'type': 'number', 'example': 800.0},
                            'location': {'type': 'string', 'example': '台北市信義區'},
                            'avg_rating': {'type': 'number', 'example': 0.0},
                            'created_at': {'type': 'string', 'example': '2024-01-01T10:00:00'}
                        }
                    }
                }
            }
        },
        400: {
            'description': '請求參數錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '必填欄位不能為空'},
                    'errors': {
                        'type': 'object',
                        'example': {
                            'subject': ['科目名稱不能為空'],
                            'price': ['價格必須大於0']
                        }
                    }
                }
            }
        },
        404: {
            'description': '老師不存在',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '指定的老師不存在'}
                }
            }
        },
        500: {
            'description': '伺服器錯誤',
            'schema': {
                'type': 'object',
                'properties': {
                    'success': {'type': 'boolean', 'example': False},
                    'message': {'type': 'string', 'example': '課程新增失敗'}
                }
            }
        }
    }
})
def create_course():
    """
    新增課程
    """
    try:
        # 獲取請求資料
        data = request.get_json()
        
        # 驗證必填欄位
        required_fields = ['subject', 'teacher_id', 'price', 'location']
        errors = {}
        
        for field in required_fields:
            if not data or field not in data or not data[field]:
                if field not in errors:
                    errors[field] = []
                errors[field].append(f'{field} 不能為空')
        
        # 驗證價格
        if data and 'price' in data:
            try:
                price = float(data['price'])
                if price <= 0:
                    if 'price' not in errors:
                        errors['price'] = []
                    errors['price'].append('價格必須大於0')
            except (ValueError, TypeError):
                if 'price' not in errors:
                    errors['price'] = []
                errors['price'].append('價格格式錯誤')
        
        # 如果有驗證錯誤，回傳錯誤訊息
        if errors:
            return jsonify({
                'success': False,
                'message': '必填欄位不能為空',
                'errors': errors
            }), 400
        
        # 檢查老師是否存在
        teacher = Teacher.query.get(data['teacher_id'])
        if not teacher:
            return jsonify({
                'success': False,
                'message': '指定的老師不存在'
            }), 404
        
        # 建立新課程
        new_course = Course(
            subject=data['subject'],
            teacher_id=data['teacher_id'],
            description=data.get('description', ''),
            price=float(data['price']),
            location=data['location'],
            avg_rating=0.0  # 新課程預設評分為0
        )
        
        # 儲存到資料庫
        db.session.add(new_course)
        db.session.commit()
        
        # 回傳新建立的課程資料
        return jsonify({
            'success': True,
            'message': '課程新增成功',
            'data': {
                'id': new_course.id,
                'subject': new_course.subject,
                'teacher_id': new_course.teacher_id,
                'description': new_course.description,
                'price': float(new_course.price),
                'location': new_course.location,
                'avg_rating': new_course.avg_rating,
                'created_at': new_course.created_at.isoformat() if new_course.created_at else None
            }
        }), 201
        
    except Exception as e:
        # 如果發生錯誤，回滾交易
        db.session.rollback()
        return jsonify({
            'success': False,
            'message': f'課程新增失敗: {str(e)}'
        }), 500