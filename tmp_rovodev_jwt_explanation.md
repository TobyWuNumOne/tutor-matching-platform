# 🔐 JWT Token 內容和設定說明

## 📋 **當前JWT Token包含的資訊**

### **Header (標頭)**
```json
{
  "alg": "HS256",    // 加密演算法
  "typ": "JWT"       // Token類型
}
```

### **Payload (載荷) - 用戶資訊**
```json
{
  "fresh": false,                    // Flask-JWT-Extended內建
  "iat": 1754398924,                // 發行時間 (issued at)
  "jti": "3d1c9b3f-7a6f-4712...",   // JWT ID (唯一識別)
  "type": "access",                 // Token類型
  "sub": "3",                       // 主體 (用戶ID)
  "nbf": 1754398924,                // 生效時間 (not before)
  "csrf": "088eb955-c651-459c...",  // CSRF保護
  "exp": 1754402524,                // 過期時間 (expires)
  
  // 🎯 自定義的用戶資訊 (可以修改)
  "account": "test@example.com",    // 用戶帳號
  "name": "測試用戶",               // 用戶姓名
  "role": "student"                 // 用戶角色
}
```

---

## ⚙️ **JWT設定位置和修改方法**

### **1. 基本配置** (`backend/app/config.py`)
```python
# JWT密鑰和過期時間
JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY", "super-secret-key")
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=1)      # 1小時過期
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)     # 30天過期
```

### **2. 自定義用戶資訊** (`backend/app/routes/auth_routes.py` 第125-129行)
```python
# 🎯 這裡可以自定義JWT中包含的用戶資訊
additional_claims = {
    "account": user.account,    # 用戶帳號
    "name": user.name,         # 用戶姓名  
    "role": user.role          # 用戶角色
}

# 創建包含自定義資訊的token
access_token = create_access_token(
    identity=str(user.id), 
    additional_claims=additional_claims
)
```

---

## 🔧 **如何修改JWT內容**

### **方法1: 添加更多用戶資訊**
```python
# 在 auth_routes.py 的 login() 函數中修改
additional_claims = {
    "account": user.account,
    "name": user.name,
    "role": user.role,
    
    # 🆕 可以添加更多資訊
    "email": user.email,           # 如果有email欄位
    "created_at": user.created_at.isoformat(),  # 註冊時間
    "permissions": ["read", "write"],           # 權限列表
    "department": "IT",                         # 部門
    "avatar_url": user.avatar_url,             # 頭像URL
}
```

### **方法2: 根據角色添加不同資訊**
```python
additional_claims = {
    "account": user.account,
    "name": user.name,
    "role": user.role
}

# 根據角色添加特定資訊
if user.role == "student":
    student = Student.query.filter_by(user_id=user.id).first()
    if student:
        additional_claims["student_id"] = student.id
        additional_claims["grade"] = student.grade  # 如果有年級欄位
        
elif user.role == "teacher":
    teacher = Teacher.query.filter_by(user_id=user.id).first()
    if teacher:
        additional_claims["teacher_id"] = teacher.id
        additional_claims["subjects"] = teacher.subjects  # 如果有科目欄位
```

### **方法3: 修改過期時間**
```python
# 在 config.py 中修改
JWT_ACCESS_TOKEN_EXPIRES = timedelta(hours=2)    # 改為2小時
JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=7)    # 改為7天

# 或者針對不同角色設定不同過期時間
if user.role == "admin":
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=8)  # 管理員8小時
    )
else:
    access_token = create_access_token(
        identity=str(user.id), 
        additional_claims=additional_claims,
        expires_delta=timedelta(hours=1)  # 一般用戶1小時
    )
```

---

## 🎯 **建議的JWT內容優化**

### **當前問題**
- refresh token創建時也包含了additional_claims，但第177行的refresh沒有包含

### **建議修改**
```python
# 在 refresh() 函數中 (第177行) 也添加用戶資訊
additional_claims = {
    "account": user.account,
    "name": user.name,
    "role": user.role
}

new_access_token = create_access_token(
    identity=str(user.id),
    additional_claims=additional_claims  # 添加這行
)
```

---

## 🔍 **如何在前端使用JWT資訊**

### **解析JWT內容**
```javascript
// 在前端解析JWT token
function parseJWT(token) {
    const base64Url = token.split('.')[1];
    const base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/');
    const jsonPayload = decodeURIComponent(atob(base64).split('').map(function(c) {
        return '%' + ('00' + c.charCodeAt(0).toString(16)).slice(-2);
    }).join(''));
    
    return JSON.parse(jsonPayload);
}

// 使用方式
const token = localStorage.getItem('jwt');
const userInfo = parseJWT(token);
console.log('用戶姓名:', userInfo.name);
console.log('用戶角色:', userInfo.role);
```

---

## 💡 **安全注意事項**

1. **不要在JWT中存放敏感資訊** (如密碼、信用卡號)
2. **JWT是可以被解碼的** (只是簽名驗證，不是加密)
3. **適合存放的資訊**: 用戶ID、姓名、角色、權限等
4. **定期更換JWT_SECRET_KEY**
5. **設定合理的過期時間**