<script setup>
import { reactive, ref } from "vue";
import Navbar from "../components/Navbar.vue";
import Footer from "../components/Footer.vue";

// 個人資料
const students = reactive({
    name: "Cody",
    email: "cody@test.com",
    country: "臺北 Taipei",
    specialization: "國文",

    gender: "男",
    age: "18",
});

const isEditing = ref(false); // 是否進入編輯模式

const studentForm = reactive({
    email: students.email,
    gender: students.gender,
    age: students.age,
});

// 模擬送出表單的函式（實際請串接 API）
const submitProfileEdit = () => {
    // 你可以用 fetch / axios 呼叫 API 更新後端資料庫
    console.log("送出資料：", studentForm);

    // 假設送出成功，就更新畫面顯示用資料
    students.email = studentForm.email;
    students.gender = studentForm.gender;
    students.age = studentForm.age;

    isEditing.value = false;
};

// 假資料老師
const bookedTeachers = ref([
    {
        name: "老師 A",
        course: "國文",
        time: "09:00 - 10:00",
        status: "可預約",
    },
    {
        name: "老師 B",
        course: "英文",
        time: "10:00 - 11:00",
        status: "不可預約",
    },
    {
        name: "老師 C",
        course: "數學",
        time: "14:00 - 15:00",
        status: "可預約",
    },
    {
        name: "老師 D",
        course: "社會",
        time: "17:00 - 18:00",
        status: "不可預約",
    },
    {
        name: "老師 E",
        course: "自然",
        time: "20:00 - 21:00",
        status: "可預約",
    },
]);

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
