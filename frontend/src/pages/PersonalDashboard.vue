<script setup>
import { reactive, ref, onMounted } from "vue";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";
import { authAPI, userAPI, studentAPI, bookingAPI } from "../utils/api.js";

// 個人資料
const students = reactive({
    name: "",
    email: "",
    country: "",
    specialization: "",
    gender: "",
    age: "",
    role: "",
    id: null,
});

// 載入狀態
const loading = ref(false);
const error = ref("");

const isEditing = ref(false); // 是否進入編輯模式

const studentForm = reactive({
    email: "",
    gender: "",
    age: "",
});

// 獲取用戶資料
const fetchUserProfile = async () => {
    loading.value = true;
    error.value = "";
    
    try {
        const response = await authAPI.getCurrentUser();
        const userData = response.data;
        
        console.log("✅ 用戶資料載入成功:", userData);
        
        // 更新用戶基本資料
        students.id = userData.id;
        students.name = userData.name;
        students.email = userData.account; // API返回的是account字段
        students.role = userData.role;
        
        // 根據角色獲取詳細資料
        if (userData.role === 'student') {
            await fetchStudentDetails(userData.id);
        } else if (userData.role === 'teacher') {
            await fetchTeacherDetails(userData.id);
        }
        
        // 更新表單資料 (在獲取詳細資料後)
        setTimeout(() => {
            studentForm.email = students.email;
            studentForm.gender = students.gender;
            studentForm.age = students.age;
        }, 200);
        
    } catch (err) {
        console.error("獲取用戶資料失敗:", err);
        error.value = "無法載入用戶資料，請重新登入";
    } finally {
        loading.value = false;
    }
};

// 獲取學生詳細資料
const fetchStudentDetails = async (userId) => {
    try {
        console.log("🔍 獲取學生詳細資料...", userId);
        const response = await studentAPI.getStudentByUserId(userId);
        
        if (response.data.success) {
            const studentData = response.data.data;
            console.log("✅ 學生詳細資料:", studentData);
            
            // 更新學生資料
            students.email = studentData.email || students.email;
            students.gender = studentData.gender || "尚未設定";
            students.age = studentData.age || "尚未設定";
            students.country = "臺北 Taipei";
            students.specialization = "學生";
        } else {
            console.log("⚠️ 沒有找到學生資料，使用預設值");
            students.country = "臺北 Taipei";
            students.specialization = "學生";
            students.gender = "尚未設定";
            students.age = "尚未設定";
        }
    } catch (err) {
        console.error("獲取學生詳細資料失敗:", err);
        // 使用預設值
        students.country = "臺北 Taipei";
        students.specialization = "學生";
        students.gender = "尚未設定";
        students.age = "尚未設定";
    }
};

// 獲取老師詳細資料
const fetchTeacherDetails = async (userId) => {
    try {
        // 這裡可以調用老師詳細資料API
        // const response = await teacherAPI.getTeacherInfo();
        // 暫時使用預設值
        students.country = "臺北 Taipei";
        students.specialization = "專業教師";
        students.gender = "尚未設定";
        students.age = "尚未設定";
    } catch (err) {
        console.error("獲取老師詳細資料失敗:", err);
    }
};

// 更新個人資料
const submitProfileEdit = async () => {
    try {
        console.log("📝 更新學生資料：", studentForm);
        
        // 調用學生資料更新API
        const updateData = {
            email: studentForm.email,
            gender: studentForm.gender,
            age: studentForm.age
        };
        
        const response = await studentAPI.updateStudentInfo(updateData);
        console.log("✅ 學生資料更新成功:", response.data);
        
        // 更新本地顯示資料
        students.email = studentForm.email;
        students.gender = studentForm.gender;
        students.age = studentForm.age;
        
        isEditing.value = false;
        
    } catch (err) {
        console.error("更新學生資料失敗:", err);
        error.value = "更新失敗，請稍後再試";
    }
};

// 獲取用戶預約資料 (暫時使用假資料)
const fetchUserBookings = async () => {
    bookingsLoading.value = true;
    bookingsError.value = '';
    
    try {
        console.log("🔍 獲取用戶預約資料 (暫時使用假資料)...");
        
        // 暫時使用假資料，避免API錯誤影響頁面
        const fakeBookings = [
            {
                id: 1,
                teacher_name: "張老師",
                course_name: "數學",
                schedule_date: "2025-01-10 10:00:00",
                status: "confirmed"
            },
            {
                id: 2,
                teacher_name: "李老師", 
                course_name: "英文",
                schedule_date: "2025-01-12 14:00:00",
                status: "pending"
            }
        ];
        
        // 轉換預約資料為顯示格式
        bookedTeachers.value = fakeBookings.map(booking => ({
            id: booking.id,
            name: booking.teacher_name,
            course: booking.course_name,
            time: formatBookingTime(booking.schedule_date),
            status: getBookingStatus(booking.status),
            originalStatus: booking.status,
            scheduleDate: booking.schedule_date
        }));
        
        console.log("✅ 假資料預約資料:", bookedTeachers.value);
        
    } catch (err) {
        console.error("獲取預約資料失敗:", err);
        bookingsError.value = "載入預約資料時發生錯誤";
        bookedTeachers.value = [];
    } finally {
        bookingsLoading.value = false;
    }
};

// 格式化預約時間顯示
const formatBookingTime = (scheduleDate) => {
    if (!scheduleDate) return "時間未定";
    
    try {
        const date = new Date(scheduleDate);
        const timeStr = date.toLocaleTimeString('zh-TW', { 
            hour: '2-digit', 
            minute: '2-digit',
            hour12: false 
        });
        const dateStr = date.toLocaleDateString('zh-TW', {
            month: 'numeric',
            day: 'numeric'
        });
        return `${dateStr} ${timeStr}`;
    } catch (err) {
        return scheduleDate;
    }
};

// 轉換預約狀態為顯示文字
const getBookingStatus = (status) => {
    const statusMap = {
        'pending': '待確認',
        'confirmed': '已確認',
        'completed': '已完成',
        'cancelled': '已取消'
    };
    return statusMap[status] || status;
};

// 頁面載入時獲取用戶資料
onMounted(async () => {
    console.log("🚀 PersonalDashboard載入，開始獲取用戶資料...");
    
    // 先獲取用戶資料，再獲取預約資料
    await fetchUserProfile();
    
    // 獨立獲取預約資料，不影響用戶資料顯示
    fetchUserBookings().catch(err => {
        console.error("預約資料載入失敗，但不影響其他功能:", err);
    });
});

// 真實預約資料
const bookedTeachers = ref([]);
const bookingsLoading = ref(false);
const bookingsError = ref('');

const showAllTeachers = ref(false);
</script>

<template>
    <div class="flex flex-col min-h-screen">
        <Navbar />

        <main class="flex-1 bg-gray-50 p-6 pt-[110px] mt-4">
            <div
                class="max-w-6xl mx-auto grid grid-cols-1 md:grid-cols-10 gap-6"
            >
                <!-- 左側 -->
                <div
                    class="md:col-span-3 bg-white p-4 rounded-lg shadow flex flex-col items-center"
                >
                    <img
                        src="https://source.unsplash.com/random/180x200"
                        alt="avatar"
                        class="w-[180px] h-[200px] rounded-lg mb-4 object-cover"
                    />
                    <p class="text-xl font-bold mb-2">{{ students.name }}</p>
                    <p class="text-sm text-gray-600 mb-4">
                        {{ students.email }}
                    </p>
                    <p class="text-gray-600 mb-2">
                        <span class="font-bold">來自：</span
                        >{{ students.country }}
                    </p>
                    <p class="text-gray-600">
                        <span class="font-bold">專精科目：</span
                        >{{ students.specialization }}
                    </p>
                    <p class="text-gray-600">
                        <span class="font-bold">性別：</span
                        >{{ students.gender }}
                    </p>
                    <p class="text-gray-600">
                        <span class="font-bold">年齡：</span>{{ students.age }}
                    </p>
                </div>

                <!-- 右側 -->
                <div class="md:col-span-7 space-y-6">
                    <!-- 預約老師 -->
                    <div class="bg-white p-4 rounded-lg shadow space-y-4">
                        <div
                            class="flex justify-between items-center border-b pb-2"
                        >
                            <p class="font-semibold text-xl">選課狀態：</p>
                            <button 
                                @click="fetchUserBookings" 
                                :disabled="bookingsLoading"
                                class="text-sm px-3 py-1 bg-blue-500 text-white rounded hover:bg-blue-600 disabled:opacity-50"
                            >
                                {{ bookingsLoading ? '載入中...' : '重新整理' }}
                            </button>
                        </div>

                        <!-- 載入狀態 -->
                        <div v-if="bookingsLoading && bookedTeachers.length === 0" class="text-center py-4">
                            <p class="text-gray-600">載入預約資料中...</p>
                        </div>

                        <!-- 錯誤狀態 -->
                        <div v-else-if="bookingsError" class="text-center py-4">
                            <p class="text-red-500">{{ bookingsError }}</p>
                            <button 
                                @click="fetchUserBookings" 
                                class="mt-2 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
                            >
                                重新載入
                            </button>
                        </div>

                        <!-- 無預約資料 -->
                        <div v-else-if="bookedTeachers.length === 0" class="text-center py-8">
                            <p class="text-gray-500 mb-4">目前沒有預約課程</p>
                            <router-link 
                                to="/search" 
                                class="px-4 py-2 bg-green-500 text-white rounded hover:bg-green-600"
                            >
                                立即預約課程
                            </router-link>
                        </div>

                        <div
                            v-for="(teacher, i) in showAllTeachers
                                ? bookedTeachers
                                : bookedTeachers.slice(0, 3)"
                            :key="i"
                            class="bg-gray-100 p-3 rounded-lg mb-2 text-sm md:text-base grid grid-cols-2 grid-rows-2 gap-2 items-center md:flex md:justify-between md:items-center"
                        >
                            <!-- 老師名稱 -->
                            <p class="font-medium text-left md:w-1/4">
                                {{ teacher.name }}
                            </p>

                            <!-- 狀態 -->
                            <p class="text-right md:text-left md:w-1/4">
                                <span class="font-bold mr-1">狀態：</span>
                                <span
                                    :class="
                                        teacher.status === '可預約'
                                            ? 'text-green-600'
                                            : 'text-red-600'
                                    "
                                >
                                    {{ teacher.status }}
                                </span>
                            </p>

                            <!-- 預約課程 -->
                            <p class="text-left md:w-1/4">
                                <span class="font-bold">預約課程：</span>
                                <span>{{ teacher.course }}</span>
                            </p>

                            <!-- 預約時間 -->
                            <p class="text-left md:w-1/4">
                                <span class="font-bold">預約時間：</span>
                                <span>{{ teacher.time || "未填寫" }}</span>
                            </p>
                        </div>

                        <!-- 展開已預約課程 -->
                        <div
                            v-if="bookedTeachers.length > 3"
                            class="text-center"
                        >
                            <button
                                class="text-blue-500 hover:underline text-base cursor-pointer"
                                @click="showAllTeachers = !showAllTeachers"
                            >
                                {{
                                    showAllTeachers ? "顯示較少" : "查看更多..."
                                }}
                            </button>
                        </div>
                    </div>

                    <!-- 設定選單 -->
                    <div class="bg-white p-4 rounded-lg shadow">
                        <p class="font-semibold text-xl mb-3">設定：</p>
                        <div class="space-y-2 text-sm">
                            <!-- 編輯個人資料 -->
                            <div
                                class="bg-gray-50 hover:bg-gray-200 p-2 rounded cursor-pointer text-base"
                                @click="isEditing = !isEditing"
                            >
                                {{ isEditing ? "取消編輯" : "編輯個人資料" }}
                            </div>
                            <!-- 編輯個人資料表單 -->
                            <div v-if="isEditing" class="mt-4 space-y-4">
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >Email：</label
                                    >
                                    <input
                                        v-model="studentForm.email"
                                        type="email"
                                        class="mt-1 p-2 block w-full border border-gray-300 rounded"
                                    />
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >性別：</label
                                    >
                                    <select
                                        v-model="studentForm.gender"
                                        class="mt-1 p-2 block w-full border border-gray-300 rounded"
                                    >
                                        <option value="">請選擇</option>
                                        <option value="男">男</option>
                                        <option value="女">女</option>
                                    </select>
                                </div>
                                <div>
                                    <label
                                        class="block text-sm font-medium text-gray-700"
                                        >年齡：</label
                                    >
                                    <input
                                        v-model="studentForm.age"
                                        type="text"
                                        class="mt-1 p-2 block w-full border border-gray-300 rounded"
                                    />
                                </div>
                                <button
                                    @click="submitProfileEdit"
                                    class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600"
                                >
                                    儲存
                                </button>
                            </div>

                            <div
                                class="bg-gray-50 hover:bg-gray-200 p-2 rounded cursor-pointer text-base"
                            >
                                安全性
                            </div>
                            <div
                                class="bg-gray-50 hover:bg-gray-200 p-2 rounded cursor-pointer text-base"
                            >
                                通知
                            </div>
                            <div
                                class="bg-gray-50 hover:bg-gray-200 p-2 rounded cursor-pointer text-base"
                            >
                                回報問題
                            </div>
                            <Router-link to="/login">
                                <div
                                    class="bg-red-100 hover:bg-red-200 p-2 rounded cursor-pointer text-red-600 text-base"
                                >
                                    登出
                                </div>
                            </Router-link>
                        </div>
                    </div>
                </div>
            </div>
        </main>

        <Footer />
    </div>
</template>

<style scoped></style>
