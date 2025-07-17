<script setup>
import { ref } from "vue";
import { RouterLink } from "vue-router";
import { onMounted } from "vue";

// 控制密碼顯示/隱藏
const showPassword = ref(false);
const password = ref("");

// Google 登入回調
function handleCredentialResponse(response) {
    const id_token = response.credential;

    fetch("https://你的API/api/auth/google/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ id_token }),
    })
        .then((res) => res.json())
        .then((data) => {
            localStorage.setItem("jwt", data.token);
        });
}

onMounted(() => {
    // 初始化 SDK
    window.google.accounts.id.initialize({
        client_id: "你的GoogleClientID",
        callback: handleCredentialResponse,
    });

    // 動態生成 Google 登入按鈕
    window.google.accounts.id.renderButton(
        document.getElementById("google-login-btn"),
        { theme: "outline", size: "large" }
    );
});
</script>

<template>
    <div
        class="min-h-screen flex flex-col items-center justify-center bg-gray-100 relative"
    >
        <!-- Logo 區 -->
        <div class="absolute top-4 left-4 flex items-center gap-4">
            <img
                src="../assets/customer-service-headset.png"
                class="w-20 h-20"
            />
            <h2 class="text-2xl font-bold">家教媒合平台</h2>
        </div>

        <!-- 登入卡片 -->
        <div
            class="bg-white shadow-lg rounded-lg p-8 w-[90%] max-w-md space-y-6"
        >
            <form class="space-y-4">
                <div class="text-center space-y-1">
                    <p class="text-xl font-semibold">歡迎回來</p>
                    <p class="text-gray-500 text-sm">請輸入帳號密碼</p>
                </div>

                <!-- 表單欄位 -->
                <div class="grid gap-3">
                    <!-- 帳號 -->
                    <label class="text-sm font-medium">帳號</label>
                    <input
                        type="email"
                        class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <!-- 密碼 -->
                    <label class="text-sm font-medium">密碼</label>
                    <div class="relative">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="password"
                            class="w-full rounded-md border border-gray-300 px-3 py-2 pr-10 focus:outline-none focus:ring-2 focus:ring-blue-500"
                        />
                        <!-- 只有輸入密碼才顯示眼睛 -->
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
                </div>

                <!-- 記住我 / 忘記密碼 -->
                <div class="flex justify-between items-center text-sm">
                    <label class="flex items-center gap-1">
                        <input type="checkbox" />
                        記住我
                    </label>
                    <RouterLink to="/" class="text-blue-600 hover:underline"
                        >忘記帳號密碼？</RouterLink
                    >
                </div>

                <!-- 登入按鈕 -->
                <div class="grid gap-3">
                    <button
                        class="bg-blue-600 text-white py-2 rounded-md text-center hover:bg-blue-700 transition cursor-pointer"
                    >
                        登入
                    </button>

                    <!-- 分隔線 + 或 -->
                    <div
                        class="flex items-center justify-center gap-2 text-gray-500 text-sm"
                    >
                        <hr class="flex-1 border-gray-300" />
                        <span>或</span>
                        <hr class="flex-1 border-gray-300" />
                    </div>

                    <div id="google-login-btn"></div>
                </div>

                <!-- 註冊導引 -->
                <p class="text-center text-sm text-gray-700">
                    還沒有帳戶嗎？
                    <RouterLink
                        to="/register"
                        class="text-blue-600 hover:underline"
                        >註冊一個吧！</RouterLink
                    >
                </p>
            </form>
        </div>
    </div>
</template>

<style></style>
