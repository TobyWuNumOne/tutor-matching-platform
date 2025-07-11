from django.db import models
from django.db.models import Q, CheckConstraint
from django.contrib.auth.models import AbstractUser

# Choices 定義於 class 外，方便 constraint 使用
ROLE_CHOICES = [
    ("teacher", "Teacher"),
    ("student", "Student"),
    ("both", "Both"),
    ("superuser", "Superuser"),  # 新增 superuser 選項
]
ROLE_VALUES = [choice[0] for choice in ROLE_CHOICES]

STATUS_CHOICES = [
    ("pending", "Pending"),
    ("confirmed", "Confirmed"),
    ("cancelled", "Cancelled"),
]
STATUS_VALUES = [choice[0] for choice in STATUS_CHOICES]

RATING_CHOICES = [str(i) for i in range(1, 6)]  # 假設評分為1~5分


# 建立Users表格 - 繼承 AbstractUser
class Users(AbstractUser):
    # 繼承 AbstractUser 已包含：
    # - username (必填，唯一)
    # - first_name, last_name  
    # - email (可選，但我們可設為必填)
    # - password (自動雜湊)
    # - is_active, is_staff, is_superuser
    # - date_joined, last_login
    
    # 我們的自訂欄位
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # 設定 email 為必填且唯一
    email = models.EmailField(unique=True, null=False)
    
    # name property - 結合 username 或 first_name/last_name
    @property
    def name(self):
        """回傳完整姓名或 username"""
        if self.first_name and self.last_name:
            return f"{self.first_name} {self.last_name}"
        return self.username
    
    def save(self, *args, **kwargs):
        """儲存時根據 role 設定權限"""
        if self.role == 'superuser':
            self.is_staff = True
            self.is_superuser = True
        else:
            self.is_staff = False
            self.is_superuser = False
        super().save(*args, **kwargs)
    
    def has_perm(self, perm, obj=None):
        """檢查用戶權限"""
        return self.role == 'superuser'
    
    def has_module_perms(self, app_label):
        """檢查模組權限"""
        return self.role == 'superuser'

    class Meta:
        db_table = "Users"
        constraints = [
            CheckConstraint(
                check=models.Q(role__in=ROLE_VALUES),
                name="users_role_valid",
            ),
        ]

    def __str__(self):
        return self.name


# 建立Courses表格
class Courses(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    teacher_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        limit_choices_to={"role__in": ["teacher", "both"]},  # 改為 teacher 和 both
        related_name="courses",
        null=True,
    )
    subject = models.CharField(max_length=255, null=False)
    price_per_hour = models.DecimalField(
        max_digits=6, decimal_places=2, null=False
    )  # 6位數(包含小數點後2位):最高9999.99
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    students = models.ManyToManyField(
        "Users",
        related_name="enrolled_courses",
        limit_choices_to={"role": "student"},
        blank=True,
    )

    class Meta:
        db_table = "Courses"

    def __str__(self):
        return self.subject


# 建立Bookings表格
class Bookings(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    student_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},  # 只在 admin 或表單過濾
        related_name="booking_students",
        null=True,
    )
    course_id = models.ForeignKey(
        "Courses", on_delete=models.CASCADE, related_name="booking_courses", null=True
    )
    schedule_date = models.CharField(max_length=255, null=False)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Bookings"
        constraints = [
            CheckConstraint(
                check=models.Q(status__in=STATUS_VALUES),
                name="bookings_status_valid",
            ),
        ]


# 建立Reviews表格
class Reviews(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    course_id = models.ForeignKey(
        "Courses", on_delete=models.CASCADE, related_name="review_students", null=True
    )
    student_id = models.ForeignKey(
        "Users",
        on_delete=models.CASCADE,
        limit_choices_to={"role": "student"},  # 只在 admin 或表單過濾
        related_name="review_courses",
        null=True,
    )
    rating = models.CharField(max_length=255, null=False)
    comment = models.CharField(max_length=255, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "Reviews"
        constraints = [
            CheckConstraint(
                check=models.Q(rating__in=RATING_CHOICES),
                name="reviews_rating_valid",
            ),
        ]
