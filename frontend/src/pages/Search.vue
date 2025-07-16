<script setup>
import { computed, onMounted, ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";
import axios from "axios";

// 資料
const CourseCategories = ["國文", "英文", "數學", "社會", "自然", "日文"];
const Rating = [
    { text: "5顆星", value: 5 },
    { text: "4顆星", value: 4 },
    { text: "3顆星", value: 3 },
    { text: "2顆星", value: 2 },
    { text: "1顆星", value: 1 },
];

const selectedCategory = ref("");
const selectedRating = ref("");
const login = ref(true); // 預設為未登入，可切換成 true 模擬登入成功
const router = useRouter();

// 取得資料庫中的Courses、Teacher表格資料用來填入課程卡片
const courses = ref([]);
const loading = ref(false); //用來表示載入狀態(後面有需要可以用來顯示spinner)
const error = ref("");
//獲取課程資料
async function fetchCourses() {
    loading.value = true;
    error.value = "";
    try {
        const response = await axios.get("/api/courses");

        if (response.data.success) {
            //如果response有成功拉到資料(response.data.success = true)
            courses.value = response.data.data;
        } else {
            error.value = response.data.error
                ? response.data.error
                : "資料拉取失敗";
            //如果後端api有回傳error的話顯示error，沒有的話顯示"資料拉取失敗"
        }
    } catch (err) {
        error.value = "無法連線伺服器";
        console.error("拉取資料錯誤:", err); //debug用
    } finally {
        loading.value = false;
    }
}

//篩選課程資料
const filteredCourses = computed(() => {
    return courses.value.filter((course) => {
        const categoryMatch = selectedCategory.value
            ? course.subject === selectedCategory.value
            : true; //沒選擇的科目的話，每次回圈的categoryMatch都是true(不會被過濾掉)
        const ratingMatch = selectedRating.value
            ? course.avg_rating >= selectedRating.value
            : true; //沒選擇的分數的話，每次回圈的ratingMatch都是true(不會被過濾掉)
        return categoryMatch && ratingMatch;
    });
});
// 控制哪個 modal 被打開
const activeModalIndex = ref(null);

function openModal(index) {
    activeModalIndex.value = index;
}

function closeModal() {
    activeModalIndex.value = null;
}
function goToTeacherInfo(teacherName) {
    router.push(`/teacher/${encodeURIComponent(teacherName)}`);
}
// 星星評分顯示
const getStars = (rating) => {
    return Math.round(rating ? rating : 0);
};

onMounted(() => {
    fetchCourses();
});
</script>

<template>
    <Navbar />

    <main class="pt-[110px] min-h-screen flex flex-col">
        <section class="p-6 flex items-center space-x-6 bg-gray-50 flex-wrap">
            <select v-model="selectedCategory" class="select-style">
                <option disabled value="">請選擇課程分類</option>
                <option
                    v-for="(item, i) in CourseCategories"
                    :key="i"
                    :value="item"
                >
                    {{ item }}
                </option>
            </select>

            <select v-model="selectedRating" class="select-style">
                <option disabled value="">請選擇評價</option>
                <option
                    v-for="(star, i) in Rating"
                    :key="i"
                    :value="star.value"
                >
                    {{ star.text }}
                </option>
            </select>

            <p
                class="text-gray-700 text-base sm:text-lg flex-grow text-center min-w-[200px]"
            >
                找到最適合你的導師，開始學習吧！
            </p>
        </section>

        <section
            class="flex-1 p-6 bg-gray-100 grid grid-cols-2 gap-4 sm:grid-cols-4 overflow-x-auto"
        >
            <div
                v-for="(course, index) in filteredCourses"
                :key="course.id"
                class="bg-white rounded-xl shadow-md p-4 flex flex-col items-center min-w-[200px] hover:shadow-lg transition relative"
            >
                <!-- 將點擊事件限制在這個div -->
                <div
                    class="w-full flex flex-col items-center cursor-pointer"
                    @click="goToTeacherInfo(course.teacher_name)"
                >
                    <img
                        :src="
                            course.avatar ||
                            `https://source.unsplash.com/random/200x200?sig=${index}`
                        "
                        alt="老師照片"
                        class="w-32 h-32 rounded-full object-cover mb-4"
                    />
                    <div class="font-bold text-xl mb-2 text-center">
                        {{ course.teacher_name }}
                    </div>
                    <p class="text-gray-700 mb-3 text-center">
                        我教學的是 {{ course.subject }}，歡迎找我學習。
                    </p>
                    <div class="flex space-x-1 mb-4">
                        <img
                            v-for="starIndex in getStars(course.avg_rating)"
                            :key="starIndex + '-' + index"
                            src="../assets/star_icon.png"
                            alt="star"
                            class="w-5 h-5"
                        />
                    </div>
                </div>

                <!-- 預約按鈕 -->
                <button
                    class="bg-[#3F3FF0] text-white px-4 py-2 rounded hover:bg-blue-700 transition w-full mt-2"
                    @click.stop="openModal(index)"
                >
                    預約老師
                </button>

                <!-- Modal -->
                <div v-if="activeModalIndex === index" class="modal-overlay">
                    <div v-if="login" class="modal-content">
                        <button class="modal-close" @click="closeModal">
                            ✕
                        </button>
                        <h2 class="text-xl font-bold mb-4">
                            預約：{{ course.teacher_name }}
                        </h2>
                        <p class="mb-4 text-gray-600">您可以選擇以下動作：</p>
                        <button
                            class="btn-primary"
                            @click="router.push('/booking')"
                        >
                            確認預約
                        </button>
                        <button class="btn-secondary">發送訊息</button>
                        <button class="btn-danger" @click="closeModal">
                            取消
                        </button>
                    </div>

                    <div v-else class="modal-content">
                        <button class="modal-close" @click="closeModal">
                            ✕
                        </button>
                        <p class="mb-4 text-lg font-semibold text-red-600">
                            您尚未登入，請先登入
                        </p>
                        <RouterLink to="/login">
                            <button class="btn-primary">前往登入</button>
                        </RouterLink>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <Footer />
</template>

<style scoped>
.select-style {
    background-color: white;
    color: #374151;
    font-size: 1rem;
    border: 1px solid #d1d5db;
    border-radius: 0.375rem;
    padding: 0.5rem 1rem;
    max-width: 10rem;
    box-shadow: 0 1px 3px rgba(0, 0, 0, 0.1);
}

.modal-overlay {
    position: fixed;
    inset: 0;
    background: rgba(255, 255, 255, 0.3);
    backdrop-filter: blur(6px);
    display: flex;
    justify-content: center;
    align-items: center;
    z-index: 50;
}

.modal-content {
    background: white;
    border-radius: 0.5rem;
    padding: 1.5rem;
    box-shadow: 0 10px 15px rgba(0, 0, 0, 0.1);
    width: 100%;
    max-width: 20rem;
    position: relative;
    text-align: center;
}
/* 被冒泡事件卡住沒辦法hover */
.modal-close {
    position: absolute;
    top: 0.5rem;
    right: 0.5rem;
    color: #6b7280;
    font-size: 1.25rem;
    background: none;
    border: none;
    cursor: pointer;
}

.btn-primary {
    background-color: #3b82f6;
    color: white;
    width: 100%;
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: 0.375rem;
    font-weight: bold;
}

.btn-secondary {
    background-color: #d1d5db;
    color: #000;
    width: 100%;
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: 0.375rem;
    font-weight: bold;
}

.btn-danger {
    background-color: #ef4444;
    color: white;
    width: 100%;
    margin-top: 0.5rem;
    padding: 0.5rem;
    border-radius: 0.375rem;
    font-weight: bold;
}
</style>
