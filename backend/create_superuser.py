#!/usr/bin/env python
"""
建立指定的 superuser 腳本
"""
import os
import sys
import django

# 設定 Django 環境
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'backend.settings')
django.setup()

from django.contrib.auth import get_user_model

User = get_user_model()

def create_superuser():
    # 檢查是否已存在 id=1 的用戶
    if User.objects.filter(id=1).exists():
        print("ID=1 的用戶已存在，正在刪除...")
        User.objects.filter(id=1).delete()
    
    # 檢查是否已存在 username=admin 的用戶
    if User.objects.filter(username='admin').exists():
        print("Username=admin 的用戶已存在，正在刪除...")
        User.objects.filter(username='admin').delete()
    
    # 建立 superuser
    try:
        user = User.objects.create_user(
            username='admin',
            email='admin@email.com',
            password='admin1234',
            role='superuser',
            first_name='Admin',
            last_name='User',
        )
        
        # 確保這個用戶有正確的 ID
        print(f"Superuser 建立成功！")
        print(f"ID: {user.id}")
        print(f"Username: {user.username}")
        print(f"Email: {user.email}")
        print(f"Role: {user.role}")
        print(f"Name: {user.name}")
        print(f"Is staff: {user.is_staff}")
        print(f"Is superuser: {user.is_superuser}")
        
    except Exception as e:
        print(f"建立 superuser 失敗: {e}")

if __name__ == "__main__":
    create_superuser()
