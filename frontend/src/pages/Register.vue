<script setup>
import Navbar from "../components/Navbar.vue";
import { ref, watch } from "vue";
import { RouterLink } from "vue-router";
import axios from "axios"; // 確保已安裝 axios

// 密碼顯示控制
const showPassword = ref(false);
const showConfirmPassword = ref(false);
const password = ref("");
const confirmPassword = ref("");
const passwordError = ref(""); // 新增錯誤訊息狀態
const name = ref(""); // 新增姓名的狀態
const email = ref(""); // 新增電子郵件的狀態
const gender = ref(""); // 新增性別的狀態
const age = ref(""); // 新增年齡的狀態
const ageError = ref(""); // 新增年齡錯誤訊息狀態

// 確認密碼的雙向綁定
watch([password, confirmPassword], ([newPassword, newConfirmPassword]) => {
    if (newConfirmPassword && newPassword !== newConfirmPassword) {
        // 顯示錯誤訊息
        passwordError.value = "密碼不一致";
    } else {
        passwordError.value = ""; // 清除錯誤訊息
    }
});

// 年齡限制檢查
watch(age, (newAge) => {
    if (newAge && newAge < 18) {
        ageError.value = "未滿18歲不得註冊";
    } else {
        ageError.value = ""; // 清除年齡錯誤訊息
    }
});

const handleSubmit = async () => {
    try {
        // 阻擋年齡低於18歲的表單提交
        if (age.value < 18) {
            alert("未滿18歲不得註冊");
            return;
        }
        if (passwordError.value) {
            alert(passwordError.value);
            return;
        }
        // 提交主要註冊資料
        const userData = {
            name: name.value,
            email: email.value,
            password: password.value,
        };
        await axios.post("/api/register", userData);

        // 提交性別和年齡到另一個資料表
        const additionalData = {
            gender: gender.value,
            age: age.value,
        };
        await axios.post("/api/user-details", additionalData);

        //alert('註冊成功！');
        //轉跳回登入頁面
        window.location.href = "/login"; // 或使用 router.push('/login') 進行
    } catch (error) {
        console.error("註冊失敗", error);
        alert("註冊失敗，請稍後再試");
    }
};
</script>

<template>
    <Navbar />
    <div
        class="flex flex-col items-center justify-center bg-gray-100 relative pt-20"
    >
        <!-- 註冊卡片 -->
        <div
            class="bg-white shadow-lg rounded-lg p-8 w-[90%] max-w-md space-y-6"
        >
            <form class="space-y-4" @submit.prevent="handleSubmit">
                <div class="text-center space-y-1">
                    <p class="text-xl font-semibold">立即加入我們</p>
                    <p class="text-gray-500 text-sm">請輸入基本資訊</p>
                </div>

                <!-- 表單欄位 -->
                <div class="grid gap-3">
                    <label class="text-sm font-medium">姓名</label>
                    <input
                        type="text"
                        v-model="name"
                        required
                        class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <label class="text-sm font-medium">帳號（Email）</label>
                    <input
                        type="email"
                        v-model="email"
                        required
                        class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />
                    <!-- 性別欄位 -->
                    <label class="text-sm font-medium">性別</label>
                    <select
                        id="underline_select"
                        v-model="gender"
                        required
                        class="block py-2.5 px-3 w-full text-sm text-gray-500 bg-transparent border-0 border-b-2 border-gray-200 appearance-none focus:outline-none focus:ring-0 focus:border-gray-200 peer"
                    >
                        <option value="" disabled selected>
                            Choose a gender
                        </option>
                        <option value="male">男</option>
                        <option value="female">女</option>
                    </select>
                    <!-- 年紀欄位 -->
                    <label class="text-sm font-medium">年齡</label>
                    <div class="relative">
                        <input
                            type="number"
                            v-model="age"
                            required
                            class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <p v-if="ageError" class="text-red-500 text-sm">
                            {{ ageError }}
                        </p>
                    </div>

                    <!-- 密碼欄位 -->
                    <label class="text-sm font-medium">密碼</label>
                    <div class="relative">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="password"
                            required
                            class="w-full rounded-md border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <span
                            v-if="password.length > 0"
                            class="absolute inset-y-0 right-3 flex items-center cursor-pointer text-gray-500"
                            @click="showPassword = !showPassword"
                        >
                            <i
                                :class="
                                    showPassword
                                        ? 'fa-solid fa-eye'
                                        : 'fa-solid fa-eye-slash'
                                "
                            ></i>
                        </span>
                    </div>

                    <!-- 確認密碼欄位 -->
                    <label class="text-sm font-medium">確認密碼</label>
                    <div class="relative">
                        <input
                            :type="showConfirmPassword ? 'text' : 'password'"
                            v-model="confirmPassword"
                            required
                            class="w-full rounded-md border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <span
                            v-if="confirmPassword.length > 0"
                            class="absolute inset-y-0 right-3 flex items-center cursor-pointer text-gray-500"
                            @click="showConfirmPassword = !showConfirmPassword"
                        >
                            <i
                                :class="
                                    showConfirmPassword
                                        ? 'fa-solid fa-eye'
                                        : 'fa-solid fa-eye-slash'
                                "
                            ></i>
                        </span>
                    </div>
                    <p v-if="passwordError" class="text-red-500 text-sm">
                        {{ passwordError }}
                    </p>
                </div>

                <!-- 註冊按鈕區 -->
                <div class="grid gap-3">
                    <button
                        type="submit"
                        class="bg-blue-600 text-white py-2 rounded-md text-center hover:bg-blue-700 transition cursor-pointer"
                    >
                        註冊
                    </button>

                    <!-- 分隔線 -->
                    <div
                        class="flex items-center justify-center gap-2 text-gray-500 text-sm"
                    >
                        <hr class="flex-1 border-gray-300" />
                        <span>或</span>
                        <hr class="flex-1 border-gray-300" />
                    </div>

                    <button
                        class="bg-red-500 text-white py-2 rounded-md text-center hover:bg-red-600 transition cursor-pointer"
                    >
                        使用 Google 註冊
                    </button>
                </div>

                <!-- 登入導引 -->
                <p class="text-center text-sm text-gray-700">
                    已有帳號？
                    <RouterLink
                        to="/login"
                        class="text-blue-600 hover:underline"
                        >立即登入！</RouterLink
                    >
                </p>
            </form>
        </div>
    </div>
</template>

<style scoped></style>
