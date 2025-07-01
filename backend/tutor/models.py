from django.db import models
from django.db.models import Q, CheckConstraint
from django.contrib.auth.hashers import make_password

# Choices 定義於 class 外，方便 constraint 使用
ROLE_CHOICES = [
    ('teacher', 'Teacher'),
    ('student', 'Student'),
    ('both', 'Both'),
]
ROLE_VALUES = [choice[0] for choice in ROLE_CHOICES]

STATUS_CHOICES = [
    ('pending', 'Pending'),
    ('confirmed', 'Confirmed'),
    ('cancelled', 'Cancelled'),
]
STATUS_VALUES = [choice[0] for choice in STATUS_CHOICES]

RATING_CHOICES = [str(i) for i in range(1, 6)]  # 假設評分為1~5分

#建立Users表格
class Users(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵 
    name = models.CharField(max_length=255, null=False)
    email = models.EmailField(max_length=255, null=False, unique=True)
    #   ↑設定email格式
        #必須包含「@」符號。
        #必須有一個有效的網域（如 example.com）。
        #不允許空白字元。
        #最長長度由 max_length 控制（預設 254）。
        #不會驗證信箱是否真實存在，只檢查格式。 
    password = models.CharField(max_length=255, null=False)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)  # 新增時自動填入
    updated_at = models.DateTimeField(auto_now=True)      # 每次儲存時自動更新
    class Meta:
        db_table = 'Users'
        constraints = [
            CheckConstraint(
                check=models.Q(role__in=ROLE_VALUES),
                name='users_role_valid',
            ),
        ]
    
    def __str__(self):
        return self.name
    #設定儲存前自動將密碼欄位進行雜湊（使用 Django 內建 make_password）
    def save(self, *args, **kwargs):
        if not self.password.startswith('pbkdf2_'):
            self.password = make_password(self.password)
        super().save(*args, **kwargs)
#建立Courses表格
class Courses(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    teacher_id = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["teacher", "both"]},  # 改為 teacher 和 both
        related_name='courses',
        null=True
    )
    subject = models.CharField(max_length=255, null=False)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, null=False)#6位數(包含小數點後2位):最高9999.99
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        'Users',
        related_name='enrolled_courses',
        limit_choices_to={'role': 'student'},
        blank=True
    )
    class Meta:
        db_table = 'Courses'
    
    def __str__(self):
        return self.subject
#建立Bookings表格
class Bookings(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    student_id = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},  # 只在 admin 或表單過濾
        related_name='booking_students',
        null=True
    )
    course_id = models.ForeignKey(
        'Courses',
        on_delete=models.CASCADE,
        related_name='booking_courses',
        null=True
    )
    schedule_date = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Bookings'
        constraints = [
            CheckConstraint(
                check=models.Q(status__in=STATUS_VALUES),
                name='bookings_status_valid',
            ),
        ]
#建立Reviews表格
class Reviews(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    course_id = models.ForeignKey(
        'Courses',
        on_delete=models.CASCADE,
        related_name='review_students',
        null=True
    )
    student_id = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},  # 只在 admin 或表單過濾
        related_name='review_courses',
        null=True
    )
    rating = models.CharField(max_length=255, null=False)
    comment = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Reviews'
        constraints = [
            CheckConstraint(
                check=models.Q(rating__in=RATING_CHOICES),
                name='reviews_rating_valid',
            ),
        ]