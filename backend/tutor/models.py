from django.db import models

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
    ROLE_CHOICES = [
        ('teacher', 'Teacher'),
        ('student', 'Student'),
        ('both', 'Both'),
    ]
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)  # 新增時自動填入
    updated_at = models.DateTimeField(auto_now=True)      # 每次儲存時自動更新
    class Meta:
        db_table = 'Users'
    
    def __str__(self):
        return self.name
#建立Courses表格
class Courses(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    teacher_id = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'teacher'},  # 只在 admin 或表單過濾
        related_name='courses',
        null=True
    )
    subject = models.CharField(max_length=255, null=False)
    price_per_hour = models.DecimalField(max_digits=6, decimal_places=2, null=False)#6位數(包含小數點後2位):最高9999.99
    location = models.CharField(max_length=255, null=True)
    description = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Courses'
#建立Bookings表格
class Bookings(models.Model):
    id = models.AutoField(primary_key=True)  # 自動遞增主鍵
    student_id = models.ForeignKey(
        'Users',
        on_delete=models.CASCADE,
        limit_choices_to={'role': 'student'},  # 只在 admin 或表單過濾
        related_name='bookings',
        null=True
    )
    course_id = models.ForeignKey(
        'Courses',
        on_delete=models.CASCADE,
        related_name='bookings',
        null=True
    )
    schedule_date = models.CharField(max_length=255, null=False)
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('cancelled', 'Cancelled'),
    ]
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, null=False)
    created_at = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table = 'Bookings'