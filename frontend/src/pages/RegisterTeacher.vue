<script setup>
import { ref } from 'vue';

const form = ref({
    name: '',
    email: '',
    phone: '',
    gender: '',
    age: '',
    education: '',
    certifications: '',
    avatar: '',
    intro: '',
    teaching_experience: '',
    status: 'pending', // 預設為審核中
    blue_premium: false,
    user_id: 1, // 你可以根據登入狀態帶入實際的 user_id
});

const submitted = ref(false);

function submitForm() {
    // 可以改成實際發送 POST 到後端 API
    console.log('教師申請資料：', form.value);

    // 模擬送出成功
    submitted.value = true;

    // 清空表單（可選）
    // Object.keys(form.value).forEach((key) => form.value[key] = '');
}
</script>

<template>
    <div class="min-h-screen flex flex-col items-center justify-center bg-gray-100 relative">
        <!-- Logo 區 -->
        <div class="absolute top-4 left-4 flex items-center gap-4">
            <img src="../assets/customer-service-headset.png" class="w-20 h-20" />
            <h2 class="text-2xl font-bold">家教媒合平台</h2>
        </div>
        <div class="max-w-3xl w-full mx-auto p-6 mt-28 bg-white shadow-md rounded-md">
            <h2 class="text-2xl font-semibold text-[#3F3FF0] mb-6">註冊成為老師</h2>
            <form @submit.prevent="submitForm" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block mb-1 font-medium">姓名</label>
                        <input v-model="form.name" type="text" required class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">Email</label>
                        <input v-model="form.email" type="email" required class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">電話</label>
                        <input v-model="form.phone" type="text" required class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">性別</label>
                        <select v-model="form.gender" required class="input">
                            <option value="" disabled>請選擇</option>
                            <option value="男">男</option>
                            <option value="女">女</option>
                            <option value="其他">其他</option>
                        </select>
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">年齡</label>
                        <input v-model="form.age" type="number" required class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">學歷</label>
                        <input v-model="form.education" type="text" class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">證照</label>
                        <input v-model="form.certifications" type="text" class="input" />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">頭像連結</label>
                        <input v-model="form.avatar" type="text" class="input" />
                    </div>
                </div>

                <div>
                    <label class="block mb-1 font-medium">自我介紹</label>
                    <textarea v-model="form.intro" rows="3" class="input"></textarea>
                </div>

                <div>
                    <label class="block mb-1 font-medium">教學經驗</label>
                    <textarea v-model="form.teaching_experience" rows="4" class="input"></textarea>
                </div>

                <div class="flex items-center justify-between">
                    <button type="submit"
                        class="bg-[#3F3FF0] text-white px-6 py-2 rounded hover:bg-[#2f2fd9] transition">
                        送出申請
                    </button>
                </div>
            </form>

            <p v-if="submitted" class="text-green-600 mt-4">申請已送出，我們會盡快審核！</p>
        </div>
    </div>
</template>

<style scoped>
.input {
    width: 100%;
    padding: 0.5rem 0.75rem;
    border: 1px solid #ccc;
    border-radius: 0.375rem;
    transition: border 0.2s;
}

.input:focus {
    outline: none;
    border-color: #3F3FF0;
    box-shadow: 0 0 0 1px #3F3FF0;
}
</style>
