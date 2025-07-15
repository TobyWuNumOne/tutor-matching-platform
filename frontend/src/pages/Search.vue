<script setup>
import { ref } from "vue";
import { useRouter } from "vue-router";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

// 資料
const CourseCategories = ["國文", "英文", "數學", "社會", "自然", "日文"];
const Rating = ["5顆星", "4顆星", "3顆星", "2顆星", "1顆星"];

const selectedCategory = ref("");
const selectedRating = ref("");
const login = ref(true); // 預設為未登入，可切換成 true 模擬登入成功
const router = useRouter();

// 假老師資料
const Teachers = [
    { name: "老師A", rating: 5, subject: "國文" },
    { name: "老師B", rating: 4, subject: "英文" },
    { name: "老師C", rating: 3, subject: "數學" },
    { name: "老師D", rating: 2, subject: "社會" },
    { name: "老師E", rating: 1, subject: "自然" },
    { name: "老師F", rating: 5, subject: "日文" },
    { name: "老師G", rating: 4, subject: "國文" },
    { name: "老師H", rating: 3, subject: "英文" },
    { name: "老師I", rating: 2, subject: "數學" },
    { name: "老師J", rating: 1, subject: "社會" },
    { name: "老師K", rating: 5, subject: "自然" },
    { name: "老師L", rating: 4, subject: "日文" },
    { name: "老師M", rating: 3, subject: "國文" },
    { name: "老師N", rating: 2, subject: "英文" },
    { name: "老師O", rating: 1, subject: "數學" },
    { name: "老師P", rating: 5, subject: "社會" },
];

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
</script>

<template>
    <Navbar />

    <main class="pt-[110px] min-h-screen flex flex-col">
        <!-- 篩選區 -->
        <section class="p-6 flex items-center space-x-6 bg-gray-50 flex-wrap">
            <select
                v-model="selectedCategory"
                class="bg-white text-gray-700 text-sm sm:text-lg border border-gray-300 rounded px-4 py-2 shadow-md max-w-xs hover:cursor-pointer focus:outline-none"
            >
                <option disabled value="">請選擇課程分類</option>
                <option
                    v-for="(item, i) in CourseCategories"
                    :key="i"
                    :value="item"
                >
                    {{ item }}
                </option>
            </select>

            <select
                v-model="selectedRating"
                class="bg-white text-gray-700 text-sm sm:text-lg border border-gray-300 rounded px-4 py-2 shadow-md max-w-xs hover:cursor-pointer focus:outline-none"
            >
                <option disabled value="">請選擇評價</option>
                <option v-for="(star, i) in Rating" :key="i" :value="star">
                    {{ star }}
                </option>
            </select>

            <p
                class="text-gray-700 text-base sm:text-lg flex-grow text-center min-w-[200px]"
            >
                找到最適合你的導師，開始學習吧！
            </p>
        </section>

        <!-- 導師卡片區 -->
        <section
            class="flex-1 p-6 bg-gray-100 grid grid-cols-2 gap-4 sm:grid-cols-4 overflow-x-auto"
        >
            <!-- click冒泡事件用.self 只在點擊卡片背景時觸發跳轉之後 優化可以添加 -->
            <div
                v-for="(teacher, index) in Teachers"
                :key="index"
                @click="goToTeacherInfo(teacher.name)"
                class="bg-white rounded-xl shadow-md p-4 flex flex-col items-center min-w-[200px] relative cursor-pointer hover:shadow-lg transition"
            >
                <img
                    :src="`https://source.unsplash.com/random/200x200?sig=${index}`"
                    alt="老師照片"
                    class="w-32 h-32 rounded-full object-cover mb-4"
                />
                <div class="font-bold text-xl mb-2 text-center">
                    {{ teacher.name }}
                </div>
                <p class="text-gray-700 mb-3 text-center">
                    我教學的是 {{ teacher.subject }}，歡迎找我學習。
                </p>

                <!-- 星星評價 -->
                <div class="flex space-x-1 mb-4">
                    <img
                        v-for="starIndex in teacher.rating"
                        :key="starIndex + '-' + index"
                        src="../assets/star_icon.png"
                        alt="star"
                        class="w-5 h-5"
                    />
                </div>

                <!-- 預約按鈕 -->
                <!-- .stop 讓按鈕保留自身功能，不被外層點擊攔截 -->
                <button
                    class="bg-[#3F3FF0] text-white px-4 py-2 rounded hover:bg-blue-700 cursor-pointer transition"
                    @click.stop="openModal(index)"
                >
                    預約老師
                </button>

                <!-- Modal 區塊 -->
                <div
                    v-if="activeModalIndex === index"
                    class="fixed inset-0 bg-white/30 backdrop-blur-md flex justify-center items-center z-50"
                >
                    <div
                        v-if="login"
                        class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full relative border border-gray-200"
                    >
                        <button
                            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 cursor-pointer"
                            @click="closeModal"
                        >
                            ✕
                        </button>
                        <h2 class="text-xl font-bold mb-4">
                            預約：{{ teacher.name }}
                        </h2>
                        <p class="mb-4 text-gray-600">您可以選擇以下動作：</p>
                        <div class="flex flex-col space-y-2">
                            <button
                                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 cursor-pointer"
                            >
                                確認預約
                            </button>
                            <button
                                class="bg-gray-300 text-black px-4 py-2 rounded hover:bg-gray-400 cursor-pointer"
                            >
                                發送訊息
                            </button>
                            <button
                                class="bg-red-500 text-white px-4 py-2 rounded hover:bg-red-600 cursor-pointer"
                                @click="closeModal"
                            >
                                取消
                            </button>
                        </div>
                    </div>

                    <!-- 尚未登入視窗 -->
                    <div
                        v-else
                        class="bg-white p-6 rounded-lg shadow-lg max-w-sm w-full text-center relative border border-gray-200"
                    >
                        <button
                            class="absolute top-2 right-2 text-gray-500 hover:text-gray-700 cursor-pointer"
                            @click="closeModal"
                        >
                            ✕
                        </button>
                        <p class="mb-4 text-lg font-semibold text-red-600">
                            您尚未登入，請先登入
                        </p>
                        <RouterLink to="/login">
                            <button
                                class="bg-blue-500 text-white px-4 py-2 rounded hover:bg-blue-600 cursor-pointer"
                            >
                                前往登入
                            </button>
                        </RouterLink>
                    </div>
                </div>
            </div>
        </section>
    </main>

    <Footer />
</template>
