<script setup>
    import { ref } from 'vue';
    import { RouterLink } from 'vue-router';

    // 密碼顯示控制
    const showPassword = ref(false);
    const showConfirmPassword = ref(false);
    const password = ref('');
    const confirmPassword = ref('');
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

        <!-- 註冊卡片 -->
        <div
            class="bg-white shadow-lg rounded-lg p-8 w-[90%] max-w-md space-y-6"
        >
            <form class="space-y-4">
                <div class="text-center space-y-1">
                    <p class="text-xl font-semibold">立即加入我們</p>
                    <p class="text-gray-500 text-sm">請輸入基本資訊</p>
                </div>

                <!-- 表單欄位 -->
                <div class="grid gap-3">
                    <label class="text-sm font-medium">姓名</label>
                    <input
                        type="text"
                        class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <label class="text-sm font-medium">帳號（Email）</label>
                    <input
                        type="email"
                        class="rounded-md border border-gray-300 px-3 py-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
                    />

                    <!-- 密碼欄位 -->
                    <label class="text-sm font-medium">密碼</label>
                    <div class="relative">
                        <input
                            :type="showPassword ? 'text' : 'password'"
                            v-model="password"
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
                </div>

                <!-- 註冊按鈕區 -->
                <div class="grid gap-3">
                    <button
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
