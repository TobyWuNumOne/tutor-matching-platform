<script setup>
    import { ref } from 'vue';
    import { useRouter } from 'vue-router';

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
        user_id: null, // 送出前自動帶入
    });

    const submitted = ref(false);
    const loading = ref(false);
    const errorMsg = ref('');
    const router = useRouter();

    async function submitForm() {
        loading.value = true;
        errorMsg.value = '';
        // 嘗試從 localStorage 取得 user_id
        try {
            const jwt = localStorage.getItem('jwt');
            if (jwt) {
                const payload = JSON.parse(atob(jwt.split('.')[1]));
                console.log('[JWT payload]', payload);
                form.value.user_id = Number(payload.sub);
                console.log('[送出 user_id]', form.value.user_id);
                if (!form.value.user_id) {
                    errorMsg.value =
                        'JWT 內找不到 user_id (sub)，請確認登入流程或後端 JWT payload 格式';
                    loading.value = false;
                    return;
                }
            } else {
                errorMsg.value = '請先登入再申請老師註冊';
                loading.value = false;
                return;
            }
            form.value.age = String(form.value.age);

            // 確保不包含 password 欄位的乾淨數據
            const teacherData = {
                name: form.value.name,
                email: form.value.email,
                phone: form.value.phone,
                gender: form.value.gender,
                age: form.value.age,
                education: form.value.education,
                certifications: form.value.certifications,
                avatar: form.value.avatar,
                intro: form.value.intro,
                teaching_experience: form.value.teaching_experience,
                status: form.value.status,
                blue_premium: form.value.blue_premium,
                user_id: form.value.user_id,
            };

            console.log('[送出的教師資料]', teacherData);

            const res = await fetch(
                'http://127.0.0.1:5000/api/teacher/create',
                {
                    method: 'POST',
                    headers: { 'Content-Type': 'application/json' },
                    body: JSON.stringify(teacherData),
                }
            );
            if (res.ok) {
                submitted.value = true;
                setTimeout(() => router.push('/search'), 1200);
            } else {
                const data = await res.json();
                console.log('[老師註冊API回應]', data);
                console.log('[錯誤詳情]', data.error || data.message);
                // 根據後端 message 判斷是否已是老師
                if (
                    (data.message &&
                        (data.message.includes('已有老師身分') ||
                            data.message.includes('已經是老師'))) ||
                    (data.error &&
                        (data.error.includes('已有老師身分') ||
                            data.error.includes('已經是老師')))
                ) {
                    const errorMessage = '您已經是老師，無法重複申請。';
                    alert(errorMessage);
                    router.push('/');
                } else {
                    const errorMessage =
                        data.error || data.message || '申請失敗，請稍後再試';
                    alert(errorMessage);
                    router.push('/');
                }
            }
        } catch (e) {
            console.error('[提交錯誤]', e);
            const errorMessage = '伺服器錯誤，請稍後再試: ' + e.message;
            alert(errorMessage);
            router.push('/');
        } finally {
            loading.value = false;
        }
    }
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
        <div
            class="max-w-3xl w-full mx-auto p-6 mt-28 bg-white shadow-md rounded-md"
        >
            <h2 class="text-2xl font-semibold text-[#3F3FF0] mb-6">
                註冊成為老師
            </h2>
            <form @submit.prevent="submitForm" class="space-y-4">
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div>
                        <label class="block mb-1 font-medium">姓名</label>
                        <input
                            v-model="form.name"
                            type="text"
                            required
                            class="input"
                        />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">Email</label>
                        <input
                            v-model="form.email"
                            type="email"
                            required
                            class="input"
                        />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">電話</label>
                        <input
                            v-model="form.phone"
                            type="text"
                            required
                            class="input"
                        />
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
                        <input
                            v-model="form.age"
                            type="number"
                            required
                            class="input"
                        />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">學歷</label>
                        <input
                            v-model="form.education"
                            type="text"
                            required
                            class="input"
                        />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">證照</label>
                        <input
                            v-model="form.certifications"
                            type="text"
                            required
                            class="input"
                        />
                    </div>
                    <div>
                        <label class="block mb-1 font-medium">頭像連結</label>
                        <input
                            v-model="form.avatar"
                            type="text"
                            class="input"
                        />
                    </div>
                </div>

                <div>
                    <label class="block mb-1 font-medium">自我介紹</label>
                    <textarea
                        v-model="form.intro"
                        rows="3"
                        required
                        class="input"
                    ></textarea>
                </div>

                <div>
                    <label class="block mb-1 font-medium">教學經驗</label>
                    <textarea
                        v-model="form.teaching_experience"
                        rows="4"
                        required
                        class="input"
                    ></textarea>
                </div>

                <div class="flex items-center justify-between">
                    <button
                        type="submit"
                        :disabled="loading"
                        class="bg-[#3F3FF0] text-white px-6 py-2 rounded hover:bg-[#2f2fd9] transition disabled:opacity-60"
                    >
                        <span v-if="loading">送出中...</span>
                        <span v-else>送出申請</span>
                    </button>
                </div>
                <span v-if="errorMsg" class="text-red-500 text-sm">{{
                    errorMsg
                }}</span>
            </form>
            <p v-if="submitted" class="text-green-600 mt-4">
                申請已送出，我們會盡快審核！
            </p>
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
        border-color: #3f3ff0;
        box-shadow: 0 0 0 1px #3f3ff0;
    }
</style>
