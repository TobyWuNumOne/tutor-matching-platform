from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from tutor.models import Users, Courses, Bookings, Reviews
from tutor.serializers import UsersSerializer, CoursesSerializer, BookingsSerializer, ReviewsSerializer

@method_decorator(csrf_exempt, name='dispatch')
class UsersViewSet(viewsets.ModelViewSet):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer
    
    def get_permissions(self):
        """
        註冊功能允許匿名訪問
        """
        if self.action == 'register':
            permission_classes = [AllowAny]
        else:
            permission_classes = self.permission_classes
        return [permission() for permission in permission_classes]
    
    @action(detail=False, methods=['post'], permission_classes=[AllowAny])
    def register(self, request):
        """
        用戶註冊 API
        POST /api/users/register/
        """
        # 取得表單資料
        name = request.data.get('username')  # 前端用 username，後端用 name
        email = request.data.get('email')
        password = request.data.get('password')
        password2 = request.data.get('password2')
        role = request.data.get('role')
        
        # 基本驗證
        if not all([name, email, password, password2, role]):
            return Response({
                'error': '所有欄位都是必填的'
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查密碼是否一致
        if password != password2:
            return Response({
                'password': ['密碼不一致']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查密碼長度
        if len(password) < 6:
            return Response({
                'password': ['密碼至少需要6個字元']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查 role 是否有效
        valid_roles = ['teacher', 'student', 'both']
        if role not in valid_roles:
            return Response({
                'role': ['身分必須是 teacher, student 或 both']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # 檢查 email 是否已存在
        if Users.objects.filter(email=email).exists():
            return Response({
                'email': ['此 email 已被註冊']
            }, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            # 建立用戶
            user = Users.objects.create(
                name=name,
                email=email,
                password=password,  # 會自動雜湊（因為 save 方法）
                role=role
            )
            
            # 回傳成功訊息和用戶資料（不包含密碼）
            return Response({
                'message': '註冊成功！',
                'user': {
                    'id': user.id,
                    'name': user.name,
                    'email': user.email,
                    'role': user.role,
                    'created_at': user.created_at
                }
            }, status=status.HTTP_201_CREATED)
            
        except Exception as e:
            return Response({
                'error': f'註冊失敗：{str(e)}'
            }, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

@method_decorator(csrf_exempt, name='dispatch')
class CoursesViewSet(viewsets.ModelViewSet):
    queryset = Courses.objects.all()
    serializer_class = CoursesSerializer

@method_decorator(csrf_exempt, name='dispatch')
class BookingsViewSet(viewsets.ModelViewSet):
    queryset = Bookings.objects.all()
    serializer_class = BookingsSerializer

@method_decorator(csrf_exempt, name='dispatch')
class ReviewsViewSet(viewsets.ModelViewSet):
    queryset = Reviews.objects.all()
    serializer_class = ReviewsSerializer
