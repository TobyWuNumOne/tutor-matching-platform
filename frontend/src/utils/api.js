// API 統一管理
import axios from 'axios';

// 設定基本配置
const API_BASE_URL = 'http://127.0.0.1:5000/api';

// 創建 axios 實例
const api = axios.create({
    baseURL: API_BASE_URL,
    timeout: 10000,
    headers: {
        'Content-Type': 'application/json',
    }
});

// 請求攔截器 - 自動添加 JWT token
api.interceptors.request.use(
    (config) => {
        const token = localStorage.getItem('jwt');
        if (token) {
            config.headers.Authorization = `Bearer ${token}`;
        }
        return config;
    },
    (error) => {
        return Promise.reject(error);
    }
);

// 響應攔截器 - 統一處理錯誤
api.interceptors.response.use(
    (response) => {
        return response;
    },
    (error) => {
        if (error.response?.status === 401) {
            // Token 過期或無效，清除本地存儲並跳轉到登入頁
            localStorage.removeItem('jwt');
            localStorage.removeItem('user_info');
            window.location.href = '/login';
        }
        return Promise.reject(error);
    }
);

// 認證相關 API
export const authAPI = {
    // 登入
    login: (credentials) => api.post('/auth/login', credentials),
    
    // 註冊
    register: (userData) => api.post('/auth/register', userData),
    
    // 登出
    logout: () => api.post('/auth/logout'),
    
    // 獲取當前用戶資訊
    getCurrentUser: () => api.get('/auth/me'),
    
    // 刷新 token
    refreshToken: () => api.post('/auth/refresh'),
};

// 用戶相關 API
export const userAPI = {
    // 獲取用戶資訊
    getProfile: () => api.get('/users'),
    
    // 更新用戶資訊
    updateProfile: (userData) => api.put('/users/profile', userData),
    
    // 刪除用戶
    deleteUser: () => api.delete('/users/profile'),
};

// 課程相關 API
export const courseAPI = {
    // 獲取所有課程
    getAllCourses: (params) => api.get('/course/list', { params }),
    
    // 獲取單一課程
    getCourse: (courseId) => api.get(`/course/${courseId}`),
    
    // 創建課程
    createCourse: (courseData) => api.post('/course/create', courseData),
    
    // 更新課程
    updateCourse: (courseId, courseData) => api.put(`/course/${courseId}`, courseData),
    
    // 刪除課程
    deleteCourse: (courseId) => api.delete(`/course/${courseId}`),
    
    // 搜尋課程
    searchCourses: (searchParams) => api.get('/course/search', { params: searchParams }),
};

// 老師相關 API
export const teacherAPI = {
    // 註冊成為老師
    registerTeacher: (teacherData) => api.post('/teacher/register', teacherData),
    
    // 獲取老師資訊
    getTeacherInfo: (teacherId) => api.get(`/teacher/${teacherId}`),
    
    // 更新老師資訊
    updateTeacherInfo: (teacherData) => api.put('/teacher/profile', teacherData),
    
    // 獲取老師的課程
    getTeacherCourses: () => api.get('/teacher/courses'),
    
    // 獲取所有老師
    getAllTeachers: () => api.get('/teacher/all'),
};

// 學生相關 API
export const studentAPI = {
    // 註冊成為學生
    registerStudent: (studentData) => api.post('/student/register', studentData),
    
    // 根據用戶ID獲取學生資訊
    getStudentByUserId: (userId) => api.get(`/student/user/${userId}`),
    
    // 更新學生資訊
    updateStudentInfo: (studentData) => api.put('/student/profile', studentData),
};

// 預約相關 API
export const bookingAPI = {
    // 創建預約
    createBooking: (bookingData) => api.post('/booking/create', bookingData),
    
    // 獲取所有預約列表
    getAllBookings: (params) => api.get('/booking/list', { params }),
    
    // 獲取單一預約
    getBooking: (bookingId) => api.get(`/booking/${bookingId}`),
    
    // 更新預約
    updateBooking: (bookingId, bookingData) => api.put(`/booking/${bookingId}`, bookingData),
    
    // 刪除預約
    deleteBooking: (bookingId) => api.delete(`/booking/${bookingId}`),
    
    // 獲取用戶的預約 (需要後端新增)
    getUserBookings: () => api.get('/booking/user'),
    
    // 獲取老師的預約 (需要後端新增)
    getTeacherBookings: () => api.get('/booking/teacher'),
    
    // 更新預約狀態 (需要後端新增)
    updateBookingStatus: (bookingId, status) => api.put(`/booking/${bookingId}/status`, { status }),
};

// 評價相關 API
export const reviewAPI = {
    // 創建評價
    createReview: (reviewData) => api.post('/reviews/create', reviewData),
    
    // 獲取課程評價
    getCourseReviews: (courseId) => api.get(`/reviews/course/${courseId}`),
    
    // 獲取老師評價
    getTeacherReviews: (teacherId) => api.get(`/reviews/teacher/${teacherId}`),
    
    // 更新評價
    updateReview: (reviewId, reviewData) => api.put(`/reviews/${reviewId}`, reviewData),
    
    // 刪除評價
    deleteReview: (reviewId) => api.delete(`/reviews/${reviewId}`),
};

// 支付相關 API
export const paymentAPI = {
    // 創建支付訂單
    createPayment: (paymentData) => api.post('/payment/ecpay', paymentData),
    
    // 獲取支付狀態
    getPaymentStatus: (tradeNo) => api.get(`/payment/status/${tradeNo}`),
    
    // 獲取支付記錄
    getPaymentHistory: () => api.get('/payment/history'),
};

// 導出默認 api 實例
export default api;