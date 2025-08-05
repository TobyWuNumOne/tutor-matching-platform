# 🔍 前後端API對比分析報告

## 📊 **後端路由 vs 前端API對比**

### ✅ **已正確對應的API**

| 分類 | 後端路由 | 前端API | 狀態 |
|------|----------|---------|------|
| **認證** | POST /auth/login | authAPI.login | ✅ 已對應 |
| **認證** | POST /auth/register | authAPI.register | ✅ 已對應 |
| **認證** | POST /auth/logout | authAPI.logout | ✅ 已對應 |
| **認證** | GET /auth/me | authAPI.getCurrentUser | ✅ 已對應 |
| **認證** | POST /auth/refresh | authAPI.refreshToken | ✅ 已對應 |
| **課程** | GET /course/list | courseAPI.getAllCourses | ✅ 已對應 |
| **課程** | GET /course/{id} | courseAPI.getCourse | ✅ 已對應 |
| **課程** | POST /course/create | courseAPI.createCourse | ✅ 已對應 |
| **課程** | PUT /course/{id} | courseAPI.updateCourse | ✅ 已對應 |
| **學生** | GET /student/user/{userId} | studentAPI.getStudentByUserId | ✅ 已對應 |
| **預約** | POST /booking/create | bookingAPI.createBooking | ✅ 已對應 |
| **評價** | POST /reviews/create | reviewAPI.createReview | ✅ 已對應 |
| **評價** | GET /reviews/course/{id} | reviewAPI.getCourseReviews | ✅ 已對應 |
| **支付** | POST /payment/ecpay | paymentAPI.createPayment | ✅ 已對應 |
| **支付** | GET /payment/status/{tradeNo} | paymentAPI.getPaymentStatus | ✅ 已對應 |

### ❌ **後端有但前端缺少的API**

| 分類 | 後端路由 | 缺少的前端API | 優先級 |
|------|----------|---------------|--------|
| **認證** | POST /auth/logout-all | authAPI.logoutAll | 🔴 高 |
| **認證** | POST /auth/logout-refresh | authAPI.logoutRefresh | 🟡 中 |
| **認證** | GET /auth/token-status | authAPI.getTokenStatus | 🟡 中 |
| **用戶** | GET /users/{userId} | userAPI.getUserById | 🔴 高 |
| **用戶** | PUT /users/{userId} | userAPI.updateUserById | 🔴 高 |
| **用戶** | DELETE /users/{userId} | userAPI.deleteUserById | 🟡 中 |
| **課程** | DELETE /course/{id} | courseAPI.deleteCourse | 🔴 高 |
| **老師** | POST /teacher/create | teacherAPI.createTeacher | 🔴 高 |
| **老師** | GET /teacher/name/{name} | teacherAPI.getTeacherByName | 🔴 高 |
| **老師** | PUT /teacher/update | teacherAPI.updateTeacher | 🔴 高 |
| **學生** | GET /student/{id} | studentAPI.getStudentById | 🟡 中 |
| **學生** | POST /student/create | studentAPI.createStudent | 🟡 中 |
| **學生** | POST /student/auto-create | studentAPI.autoCreateStudent | 🟡 中 |
| **預約** | GET /booking/list | bookingAPI.getAllBookings | 🔴 高 |
| **預約** | GET /booking/{id} | bookingAPI.getBooking | 🔴 高 |
| **預約** | PUT /booking/{id} | bookingAPI.updateBooking | 🔴 高 |
| **預約** | DELETE /booking/{id} | bookingAPI.deleteBooking | 🔴 高 |
| **評價** | GET /reviews/{id} | reviewAPI.getReview | 🟡 中 |
| **評價** | PUT /reviews/{id} | reviewAPI.updateReview | ✅ 已有 |
| **評價** | DELETE /reviews/{id} | reviewAPI.deleteReview | ✅ 已有 |
| **支付** | POST /payment/notify | paymentAPI.handleNotify | 🟡 中 |
| **支付** | POST /payment/result | paymentAPI.handleResult | 🟡 中 |
| **支付** | GET /payment/test | paymentAPI.getTestPage | 🟢 低 |

### ❌ **前端有但後端缺少的API**

| 前端API | 對應後端路由 | 狀態 |
|---------|-------------|------|
| courseAPI.searchCourses | GET /course/search | ❌ 後端缺少 |
| courseAPI.deleteCourse | DELETE /course/{id} | ❌ 後端缺少 |
| teacherAPI.registerTeacher | POST /teacher/register | ❌ 後端缺少 |
| teacherAPI.getTeacherCourses | GET /teacher/courses | ❌ 後端缺少 |
| teacherAPI.getAllTeachers | GET /teacher/all | ❌ 後端缺少 |
| studentAPI.registerStudent | POST /student/register | ❌ 後端缺少 |
| studentAPI.updateStudentInfo | PUT /student/profile | ❌ 後端缺少 |
| bookingAPI.getUserBookings | GET /booking/user | ❌ 後端缺少 |
| bookingAPI.getTeacherBookings | GET /booking/teacher | ❌ 後端缺少 |
| bookingAPI.updateBookingStatus | PUT /booking/{id}/status | ❌ 後端缺少 |
| reviewAPI.getTeacherReviews | GET /reviews/teacher/{id} | ❌ 後端缺少 |
| paymentAPI.getPaymentHistory | GET /payment/history | ❌ 後端缺少 |

---

## 🎯 **未串接功能清單 (按優先級排序)**

### 🔴 **高優先級 - 核心功能**

1. **預約系統完整串接**
   - [ ] 獲取預約列表 (booking/list)
   - [ ] 獲取單一預約 (booking/{id})
   - [ ] 更新預約 (booking/{id})
   - [ ] 刪除預約 (booking/{id})

2. **老師管理系統**
   - [ ] 創建老師 (teacher/create)
   - [ ] 根據姓名獲取老師 (teacher/name/{name})
   - [ ] 更新老師資訊 (teacher/update)
   - [ ] 獲取所有老師列表

3. **用戶管理系統**
   - [ ] 根據ID獲取用戶 (users/{userId})
   - [ ] 更新用戶資訊 (users/{userId})

4. **課程管理完善**
   - [ ] 刪除課程功能
   - [ ] 課程搜尋功能

### 🟡 **中優先級 - 增強功能**

5. **學生資料管理**
   - [ ] 更新學生資料 (student/profile)
   - [ ] 學生註冊功能

6. **認證系統增強**
   - [ ] 全部登出功能
   - [ ] Token狀態檢查

7. **評價系統完善**
   - [ ] 獲取老師評價
   - [ ] 獲取單一評價

### 🟢 **低優先級 - 輔助功能**

8. **支付系統完善**
   - [ ] 支付歷史記錄
   - [ ] 支付通知處理

9. **管理功能**
   - [ ] 刪除用戶功能
   - [ ] 系統管理功能

---

## 📋 **建議處理順序**

1. **第一階段**: 預約系統 (最重要的核心功能)
2. **第二階段**: 老師管理系統
3. **第三階段**: 學生資料更新功能
4. **第四階段**: 課程搜尋和刪除功能
5. **第五階段**: 其他增強功能

---

## 🔧 **需要修復的API端點不匹配**

| 問題 | 前端調用 | 後端實際 | 修復方案 |
|------|----------|----------|----------|
| 用戶資料 | GET /users/profile | GET /users/{userId} | 修改前端API |
| 老師更新 | PUT /teacher/profile | PUT /teacher/update | 修改前端API |
| 預約列表 | GET /booking/user | GET /booking/list | 需要後端新增 |
