<template>
    <Navbar />

    <div class="pt-32 px-6 bg-gray-100 min-h-screen">
        <div class="max-w-7xl mx-auto flex gap-6">
            <!-- 左側 老師資訊 -->
            <aside class="w-64 bg-white shadow rounded-lg p-4 shrink-0">
                <div class="flex flex-col items-center">
                    <div class="w-24 h-24 bg-gray-200 rounded-full mb-4"></div>
                    <p class="font-bold">{{ teacher.name }}</p>
                    <p class="text-sm text-gray-600">
                        科目：{{ teacher.subject }}
                    </p>
                    <p class="text-sm text-gray-600 mb-2">
                        全部影片：{{ teacher.videos }}
                    </p>
                    <p class="mb-2">
                        一對一指導：
                        <span class="text-green-500 font-bold">可預約</span>
                    </p>
                    <p class="mb-2 font-semibold">【開課時間】</p>
                    <p class="text-sm text-gray-600 text-center">
                        {{ teacher.schedule }}
                    </p>
                    <div class="flex items-center mt-4">
                        <span
                            v-for="star in teacher.rating"
                            :key="star"
                            class="text-yellow-500 text-xl"
                            >★</span
                        >
                    </div>
                    <button
                        class="bg-[#3F3FF0] text-white px-4 py-2 rounded mt-6 hover:bg-blue-700 transition w-full"
                    >
                        線上試聽
                    </button>
                </div>
            </aside>
            <div class="max-w-5xl mx-auto">
                <!-- 月份切換 -->
                <div
                    class="flex justify-between items-center mb-4 text-xl font-bold text-gray-800"
                >
                    <button @click="prevMonth" class="text-2xl px-2">←</button>
                    <span>{{ currentMonthLabel }}</span>
                    <button @click="nextMonth" class="text-2xl px-2">→</button>
                </div>

                <!-- 日期橫向 scroll -->
                <div class="flex overflow-x-auto space-x-3 pb-6 date-container">
                    <div
                        v-for="(day, index) in daysInMonth"
                        :key="index"
                        @click="selectDate(day)"
                        :class="[
                            'min-w-[60px] px-3 py-2 text-center rounded-lg cursor-pointer flex-shrink-0 transition date-item',
                            selectedDate.toDateString() ===
                            day.date.toDateString()
                                ? 'bg-blue-600 text-white'
                                : 'bg-white text-gray-800 shadow hover:bg-blue-100',
                        ]"
                    >
                        <div class="text-sm font-semibold">
                            {{ day.weekday }}
                        </div>
                        <div class="text-lg font-bold">
                            {{ day.date.getDate() }}
                        </div>
                    </div>
                </div>

                <!-- 時間 slot -->
                <div class="bg-white rounded-lg shadow p-4 space-y-3">
                    <div
                        v-for="(slot, idx) in timeSlots"
                        :key="idx"
                        class="flex justify-between items-center py-3 px-4 rounded-md bg-gray-50"
                    >
                        <span class="font-mono text-gray-700">{{ slot }}</span>
                        <button
                            class="text-sm px-4 py-1 rounded transition font-semibold"
                            :class="getButtonClass(slot)"
                            :disabled="isSlotDisabled(slot)"
                            @click="bookSlot(slot)"
                        >
                            {{ getSlotLabel(slot) }}
                        </button>
                    </div>
                </div>
            </div>
        </div>
    </div>

    <Footer />
</template>

<script setup>
    import { ref, computed, onMounted } from 'vue';
    import Navbar from '../components/Navbar.vue';
    import Footer from '../components/Footer.vue';
    import { bookingAPI, courseAPI, authAPI } from '../utils/api.js';

    // 教師資料
    const teacher = ref({
        name: 'A老師',
        subject: '數學',
        videos: 83,
        schedule: '星期一 晚上7:00~8:00 / 星期四 晚上6:00~7:00',
        rating: 4,
    });

    // 當前用戶和預約資訊
    const currentUser = ref(null);
    const currentStudentId = ref(null);  // 添加學生ID
    const userBookings = ref([]);
    const loading = ref(false);
    const error = ref('');

    // 當前日期與所選日期
    const today = new Date();
    const currentDate = ref(new Date(today));
    const selectedDate = ref(new Date(today));

    // 範例時間 slot (修正時間格式)
    const timeSlots = ref([
        '09:00am',
        '10:00am',
        '11:00am',
        '12:00pm',  // 修正：中午12點應該是pm
        '01:00pm',  // 修正：下午1點
        '02:00pm',  // 修正：下午2點
        '03:00pm',  // 修正：下午3點
        '04:00pm',  // 修正：下午4點
        '05:00pm',  // 修正：下午5點
        '06:00pm',  // 修正：下午6點
        '07:00pm',  // 修正：下午7點
        '08:00pm',  // 修正：下午8點
        '09:00pm',  // 修正：下午9點
        '10:00pm',  // 修正：下午10點
        '11:00pm',  // 修正：下午11點
    ]);

    // 月份標籤
    const currentMonthLabel = computed(() =>
        currentDate.value.toLocaleDateString('en-US', {
            month: 'long',
            year: 'numeric',
        })
    );

    // 切換月份
    function prevMonth() {
        const newDate = new Date(currentDate.value);
        newDate.setMonth(newDate.getMonth() - 1);
        currentDate.value = newDate;
    }
    function nextMonth() {
        const newDate = new Date(currentDate.value);
        newDate.setMonth(newDate.getMonth() + 1);
        currentDate.value = newDate;
    }

    // 取得月份內所有日期
    const daysInMonth = computed(() => {
        const year = currentDate.value.getFullYear();
        const month = currentDate.value.getMonth();
        const totalDays = new Date(year, month + 1, 0).getDate();

        return Array.from({ length: totalDays }, (_, i) => {
            const date = new Date(year, month, i + 1);
            return {
                date,
                weekday: date.toLocaleDateString('en-US', { weekday: 'short' }),
            };
        });
    });

    function selectDate(day) {
        selectedDate.value = day.date;
    }

    // 假資料：某些 slot 不可預約 / 已上課
    const disabledSlots = ['12:00pm'];  // 修正時間格式
    const joinedClassSlots = ['11:00am'];

    function isSlotDisabled(slot) {
        return disabledSlots.includes(slot);
    }
    function getSlotLabel(slot) {
        if (joinedClassSlots.includes(slot)) return 'link to class';
        return 'book';
    }
    function getButtonClass(slot) {
        if (isSlotDisabled(slot)) {
            return 'bg-gray-300 text-gray-500 cursor-not-allowed';
        }
        if (joinedClassSlots.includes(slot)) {
            return 'bg-blue-200 text-blue-800';
        }
        return 'bg-blue-600 text-white hover:bg-blue-700';
    }

    // 獲取用戶資訊和預約資料
    const fetchUserData = async () => {
        loading.value = true;
        error.value = '';

        try {
            // 獲取當前用戶資訊
            const userResponse = await authAPI.getCurrentUser();
            currentUser.value = userResponse.data;
            console.log('✅ 用戶資訊:', currentUser.value);
            console.log('✅ 用戶ID:', currentUser.value?.id);
            console.log('✅ 用戶類型:', typeof currentUser.value?.id);

            // 根據用戶ID查找學生ID
            if (currentUser.value && currentUser.value.role === 'student') {
                await fetchStudentId(currentUser.value.id);
            }

            // 獲取用戶的預約列表
            await fetchUserBookings();
        } catch (err) {
            console.error('獲取用戶資料失敗:', err);
            error.value = '無法載入用戶資料';
        } finally {
            loading.value = false;
        }
    };

    // 根據用戶ID獲取學生ID
    const fetchStudentId = async (userId) => {
        try {
            // 這裡需要調用後端API獲取學生ID，暫時使用假數據
            // 根據數據庫查詢結果，用戶ID 1 對應學生ID 5
            const studentIdMap = {
                1: 5,
                2: 1,
                3: 2,
                4: 3,
                5: 4
            };
            currentStudentId.value = studentIdMap[userId] || 1;
            console.log('✅ 學生ID:', currentStudentId.value);
        } catch (err) {
            console.error('獲取學生ID失敗:', err);
            // 如果失敗，使用默認值
            currentStudentId.value = 1;
        }
    };

    // 獲取用戶預約列表
    const fetchUserBookings = async () => {
        try {
            const response = await bookingAPI.getAllBookings();
            if (response.data.success) {
                userBookings.value = response.data.data;
                console.log('✅ 預約列表:', userBookings.value);
            }
        } catch (err) {
            console.error('獲取預約列表失敗:', err);
        }
    };

    // 修正時間格式處理，確保正確拼接時間
    const createBooking = async (courseId, scheduleDate, timeSlot) => {
        try {
            // 將時間格式轉換為24小時制
            const formattedTime = timeSlot.replace(/(\d{1,2}):(\d{2})(am|pm)/i, (match, hour, minute, period) => {
                let adjustedHour = parseInt(hour, 10);
                if (period.toLowerCase() === 'pm' && adjustedHour !== 12) {
                    adjustedHour += 12;
                } else if (period.toLowerCase() === 'am' && adjustedHour === 12) {
                    adjustedHour = 0;
                }
                return `${adjustedHour.toString().padStart(2, '0')}:${minute}`;
            });

            // 後端期望的格式：YYYY-MM-DD HH:MM
            const scheduleDateTime = `${scheduleDate} ${formattedTime}`;

            const bookingData = {
                course_id: courseId,
                student_id: currentStudentId.value || 1,  // 使用學生ID而不是用戶ID
                schedule_date: scheduleDateTime,  // 使用後端期望的格式
            };

            console.log('📤 傳遞的預約數據:', bookingData);
            console.log('📅 時間格式:', scheduleDateTime);

            const response = await bookingAPI.createBooking(bookingData);
            if (response.data.success) {
                console.log('✅ 預約創建成功:', response.data);
                await fetchUserBookings(); // 重新載入預約列表
                return true;
            } else {
                console.error('❌ 預約創建失敗，後端返回:', response.data);
                return false;
            }
        } catch (err) {
            console.error('❌ 創建預約時發生錯誤:', err);
            if (err.response) {
                console.error('❌ 錯誤詳情:', err.response.data);
            }
            return false;
        }
    };

    // 確保選擇的日期和時間正確傳遞
    function bookSlot(slot) {
        if (isSlotDisabled(slot)) return;

        if (!currentUser.value || !currentStudentId.value) {
            alert('請先登入才能預約');
            return;
        }

        const confirmed = confirm(
            `確定要預約 ${selectedDate.value.toDateString()} 的 ${slot} 嗎？`
        );
        if (confirmed) {
            createBooking(
                1, // 假設課程 ID 為 1
                selectedDate.value.toISOString().split('T')[0],
                slot
            ).then((success) => {
                if (success) {
                    alert(
                        `預約成功！${selectedDate.value.toDateString()} 的 ${slot}`
                    );
                } else {
                    alert('預約失敗，請稍後再試');
                }
            });
        }
    }

    // 頁面載入時獲取資料
    onMounted(() => {
        console.log('🚀 Booking頁面載入，開始獲取資料...');
        fetchUserData();
    });
</script>

<style scoped>
/* 日期橫向 scroll 容器樣式 */
.date-container {
    display: flex;
    flex-wrap: wrap;
    justify-content: space-between;
}

/* 日期欄樣式 */
.date-item {
    flex: 1 1 auto; /* 讓每個日期欄根據空間自動調整寬度 */
    min-width: 60px;
    text-align: center;
    margin: 5px;
}

/* 針對小屏幕的樣式 */
@media screen and (max-width: 768px) {
    .date-item {
        flex: 1 1 100%; /* 小屏幕時每個日期欄占滿整行 */
    }
}
</style>
